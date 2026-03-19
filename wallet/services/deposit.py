from decimal import Decimal

from django.db import transaction

import wallet
from wallet.models import Wallet, Transaction, Ledger


def deposit(recipient: Wallet, amount: Decimal):
    with transaction.atomic():
        recipient_wallet = Wallet.objects.select_for_update().get(pk=recipient.pk)

        recipient_wallet.balance += amount
        recipient_wallet.save(update_fields=['balance'])

        transaction_info = Transaction.objects.create(sender=sender,
                                                      recipient=recipient,
                                                      amount=amount,
                                                      transaction_type='CREDIT',
                                                      status='CREATED',)
        Ledger.objects.create(
            transaction=transaction_info,
            amount=amount,
            wallet=wallet,
            balance_after= recipient_wallet.balance,
            entry_type='CREDIT',

        )

        return transaction_info