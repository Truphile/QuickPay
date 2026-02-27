from wallet.models import Wallet


def create_wallet(user):
    wallet = Wallet.objects.create(user=user, wallet_number=user.phone[1:])
    return wallet