import uuid

from django.conf import settings
from django.db import models

from wallet.utility import generate_reference_id, generate_account_number


# Create your models here.

class Wallet(models.Model):
    CURRENCY_CHOICES = (
        ('NGN', 'Naira'),
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    wallet_number = models.CharField(max_length=10, unique=True, primary_key=True)
    account_number = models.CharField(max_length=10, unique=True,blank=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
        TRANSACTION_TYPE = (
            ('DEBIT','Debit'),
            ('CREDIT','Credit'),
        )

        STATUS_CHOICES = (
            ('SUCCESSFUL','Successful'),
            ('FAILED','Failed'),
            ('PENDING','Pending'),
        )

        reference = models.CharField(max_length=20,default=generate_reference_id())
        transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        sender = models.ForeignKey(Wallet, on_delete=models.PROTECT,related_name='sender')
        receiver = models.ForeignKey(Wallet, on_delete=models.PROTECT,related_name='receiver')
        status = models.CharField(max_length=10, choices=STATUS_CHOICES)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        idempotency = models.UUIDField(null=False,editable=False, blank=True,unique=True)

class Ledger(models.Model):
    TRANSACTION_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT,related_name='ledger')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)





