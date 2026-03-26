import uuid

from django.conf import settings
from django.db import models
from django.db.models import PROTECT

from wallet.utility import generate_reference_id, generate_account_number
user = settings.AUTH_USER_MODEL

# Create your models here.

class Wallet(models.Model):
    CURRENCY_CHOICES = (
        ('NGN', 'Naira'),
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),
    )

    WALLET_STATUS=(
        ('ACTIVE','Active'),
        ('INACTIVE','Inactive'),
        ('SUSPENDED','Suspended'),
        ('CLOSED','Closed'),
        ('FROZEN','Frozen'),
    )



    wallet_number = models.CharField(max_length=10, unique=True, primary_key=True)
    account_number = models.CharField(max_length=20, unique=True,blank=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    status = models.CharField(max_length=15, default=True, choices=WALLET_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(user, on_delete=PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.wallet_number}"


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

        reference = models.CharField(max_length=100,default=generate_reference_id, unique=True)
        transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        sender = models.ForeignKey(Wallet, on_delete=models.PROTECT,related_name='sender')
        receiver = models.ForeignKey(Wallet, on_delete=models.PROTECT,related_name='receiver')
        status = models.CharField(max_length=15, choices=STATUS_CHOICES)
        description = models.TextField(blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        idempotency_key = models.UUIDField(null=True,editable=False, blank=True,unique=True)

        def __str__(self):
            return f"{self.id}"

class Ledger(models.Model):
    TRANSACTION_TYPE = (
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction} {self.entry_type} {self.amount}"





