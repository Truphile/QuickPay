from decimal import Decimal


from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites import requests
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from user.models import User
from wallet.models import Transaction, Ledger, Wallet



user = get_user_model()

def initiate_paystack_payment(user,amount):
    headers = {
        'Authorization': f'Bearer{settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'email': user.email,
        'amount': int(amount * 100),
        'callback_url': 'http://localhost:8000/wallet/callback',
        'metadata': {
            'user_id': str(user.id),
        }
    }

    response = requests.post(settings.PAYSTACK_URL, headers=headers, json=data)
    return response.json()

def verify_paystack_payment(reference):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }---
    url = f'{settings.PAYSTACK_VERIFY_URL}{reference}'
    response = requests.get(url, headers=headers)
    return response.json()

def credit_wallet(wallet, amount: Decimal, reference: str):
    amount = Decimal(amount)
    with transaction.atomic():
        wallet_obj = Wallet.objects.select_for_update().get(pk=wallet.pk)
        wallet_obj.balance += amount
        wallet_obj.save(update_fields=['balance'])

        tx = Transaction.objects.create(
            amount=amount,
            sender=wallet,
            reference=reference,
            recipient=wallet,
            transaction_type='CREDIT',
            status='SUCCESS'
        )

        Ledger.objects.create(
            transaction=tx,
            amount=amount,
            wallet=wallet,
            entry_type='CREDIT',
            balance_after=wallet.balance
        )

        return tx
@api_view(['GET'])
def paystack_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        return Response({'error': 'reference is required'},status=status.HTTP_400_BAD_REQUEST)

    payment_data = verify_paystack_payment(reference)

    if not payment_data.get('status'):
        return Response(
            {'error': 'Payment verification failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


    amount = payment_data['data']['amount']/100
    email = payment_data['data']['customer']['email']
    user = User.objects.get(email=email)
    wallet = user.wallet


    tx = credit_wallet(wallet, amount, reference)
    data = {
        'reference': tx.reference,
        'amount': tx.amount,
        'status': tx.status,
        'created_at': tx.created_at,
    }

    return Response(data, status=status.HTTP_200_OK)

