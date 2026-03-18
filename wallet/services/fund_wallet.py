from django.conf import settings
from django.contrib.sites import requests


def initiate_paystack_payment(user,amount):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'email': user.email,
        'amount': int(amount * 100),
        'callback_url': 'http://127.0.0.1:8000/wallet/callback',
        'metadata': {
            'user_id': str(user.id),
        }
    }

    response = requests.post(settings.PAYSTACK_URL, headers=headers, json=data)
    return response.json()