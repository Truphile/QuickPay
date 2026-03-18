from notification.services import create_transfer_notification
from wallet.services.intra_transfer_service import transfer_wallet_to_wallet


def create_transfer(sender, recipient, amount, idempotency_key, description=None)
    transaction = transfer_wallet_to_wallet(sender, recipient, amount, idempotency_key, description)
    create_transfer_notification(recipient.user, amount)
    return transaction