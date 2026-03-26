from django.db import transaction
from user.services import create_user
from wallet.services import create_wallet
from notification.services import create_notification
from wallet.services.create_wallet import create_wallet


@transaction.atomic
def create_user_and_wallet(validated_data):
    user = create_user(validated_data)
    wallet = create_wallet(user)
    create_notification(user)
    return user, wallet

