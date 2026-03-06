from decimal import Decimal
from uuid import UUID

from wallet.models import Wallet, Transaction


def transfer_wallet_to_wallet(sender: Wallet, recipient: Wallet, amount: Decimal, idempotent_key: UUID, description : str):
    amount = Decimal(amount)


    if sender.pk == recipient.pk:
        raise Exception("Cannot transfer to self")

    if amount > sender.balance:
        raise Exception("Insufficient balance")

    existing_tx = Transaction.objects.filter(idempotent_key=idempotent_key).exists()
    if existing_tx:
        return existing_tx

    recipient_wallet = Wallet.objects.select_for_update(wallet_number=recipient.wallet_number)
    sender_wallet = Wallet.objects.select_for_update(wallet_number=sender.wallet_number)

    sender_wallet.balance -= amount
    recipient_wallet.balance += amount
    sender_wallet.save(update_fields=['balance'])
    recipient_wallet.save(update_fields=['balance'])


