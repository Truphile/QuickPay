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

    # select_for_update() method is used to do pessmistic locking
    # at the same you may be trying to do transfer out
    # and an incoming transfer is entering your wallet
    # These are two actions that will affect the balance.
    # The method ensures that the incoming action is placed on hold
    # till your transfer action has been fully processed.

    with transaction.atomic():
        recipient_wallet = Wallet.objects.select_for_update().get(pk=recipient.pk)
        sender_wallet = Wallet.objects.select_for_update().get(pk=sender.pk)

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount
        sender_wallet.save(update_fields=['balance'])
        recipient_wallet.save(update_fields=['balance'])

    transaction_info = Transaction.objects.create(
        sender=sender,
        recipient=recipient,
        amount=amount,
        idempotent_key=idempotent_key,
        transaction_type='CREDIT',
        status='CREATED',
        description=description,
    )

    Ledger.objects.create(
        transaction=transaction_info,
        amount=amount,
        wallet=sender_wallet,
        balance_after=sender_wallet.balance,
        entry_type='DEBIT',
    )

    Ledger.objects.create(
        transaction=transaction_info,
        amount=amount,
        wallet=recipient_wallet,
        balance_after=recipient_wallet.balance,
        entry_type='CREDIT',
    )

    return transaction_info




