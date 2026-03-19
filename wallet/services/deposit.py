from django.db import transaction

from wallet.models import Wallet, Transaction


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