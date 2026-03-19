from rest_framework import status
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from wallet.services.deposit import deposit
from wallet.services.fund_wallet import initiate_paystack_payment
from notification.services import create_transfer_notification
from .models import Wallet
from .serializers import WalletTransferSerializer, DepositSerializer, FundWalletSerializer
from wallet.services.intra_transfer_service import transfer_wallet_to_wallet
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_wallet(request):
    sender = request.user.wallet
    serializer = WalletTransferSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    idempotency_key = serializer.validated_data['idempotency_key']
    description = serializer.validated_data['description']
    recipient = get_object_or_404(Wallet, wallet_number=serializer.validated_data['recipient_wallet'])
    tx = transfer_wallet_to_wallet(sender, recipient,amount, idempotency_key, description)

    return Response(
        {
            "reference": tx.reference,
            "amount": tx.amount,
            "status": tx.status,
            "description": tx.description,
            "created_at": tx.created_at
        }, status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_wallet(request):
    recipient = request.user.wallet

    serializer = DepositSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    amount = serializer.validated_data['amount']

    transaction = deposit(recipient, amount)

    create_transfer_notification(recipient.user, amount)

    return Response(
        {
            "reference": transaction.reference,
            "amount": transaction.amount,
            "status": transaction.status,
            "description": transaction.description,
            "created_at": transaction.created_at
        }, status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def funded_wallet(request):
    serializer = FundWalletSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    amount = serializer.validated_data['amount']

    payment_response = initiate_paystack_payment(user, amount)

    return Response(payment_response, status= status.HTTP_200_Ok)






