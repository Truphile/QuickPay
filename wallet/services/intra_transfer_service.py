from decimal import Decimal
from uuid import UUID

from django.db import transaction

from wallet.models import Wallet, Transaction, Ledger


def transfer_wallet_to_wallet(sender: Wallet, recipient: Wallet, amount: Decimal, idempotent_key: UUID, description : str):
    amount = Decimal(amount)


    if sender.pk == recipient.pk:
        raise Exception("Cannot transfer to self")

    if amount > sender.balance:
        raise Exception("Insufficient balance")

    existing_tx = Transaction.objects.filter(idempotent_key=idempotent_key).first()
    if existing_tx:
        return existing_tx

    with transaction.atomic():

        recipient_wallet = Wallet.objects.select_for_update().get(pk=recipient.pk)
        sender_wallet = Wallet.objects.select_for_update().get(pk=sender.pk)

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount
        sender_wallet.save(update_fields=['balance'])
        recipient_wallet.save(update_fields=['balance'])

    tx = Transaction.objects.create(
        sender=sender,
        recipient=recipient,
        amount=amount,
        idempotent_key=idempotent_key,
        transaction_type='CREDIT',
        transaction_status='SUCCESSFUL',
        description=description,
    )

    Ledger.objects.create(
        transaction=tx,
        amount=amount,
        wallet=sender_wallet,
        balance=sender_wallet.balance,
        transaction_type='CREDIT',
    )

    Ledger.objects.create(
        transaction=tx,
        amount=amount,
        wallet=recipient_wallet,
        balance=recipient_wallet.balance,
        transaction_type='CREDIT',
    )

    return tx




