from decimal import Decimal

from django.db import transaction

import wallet
from wallet.models import Wallet, Transaction, Ledger


def deposit(receiver: Wallet, amount: Decimal):
    with transaction.atomic():
        receiver_wallet = Wallet.objects.select_for_update().get(pk=receiver.pk)

        receiver_wallet.balance += amount
        receiver_wallet.save(update_fields=['balance'])

        transaction_info = Transaction.objects.create(sender=sender,
                                                      receiver=receiver,
                                                      amount=amount,
                                                      transaction_type='CREDIT',
                                                      status='CREATED', )
        Ledger.objects.create(
            transaction=transaction_info,
            amount=amount,
            wallet=wallet,
            balance_after= receiver_wallet.balance,
            entry_type='CREDIT',

        )

        return transaction_info