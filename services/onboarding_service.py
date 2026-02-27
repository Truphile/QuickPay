from django.db import transaction
from user.services import create_user
from wallet.services import create_wallet



def create_user_and_wallet(validated_data):
    user = create_user(validated_data)
    wallet = create_wallet(user)

    return user, wallet