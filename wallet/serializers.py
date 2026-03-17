from rest_framework import serializers

from wallet.models import Wallet, Transaction


class WalletTransferSerializer(serializers.ModelSerializer):
    recipient_wallet = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField(read_only=True)
    description = serializers.CharField(max_length=200, required=False)

    def validate_amount(self, value):
        if value < 0:
            raise Exception("Amount cannot be negative")
        return value

    def validate_recipient_wallet(self, value):
        try:
            recipient_wallet = Wallet.objects.get(wallet_number=value)
        except Wallet.DoesNotExist:
            raise Exception("Wallet does not exist")

        return recipient_wallet

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    def validate_amount(self, value):
        if value < 0:
            raise Exception("Invalid amount. Amount cannot be greater than zero.")
        return value

class FundWalletSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value < 0:
            raise Exception("Invalid amount. Amount cannot be lesser than zero.")
        return value

class RecentTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = {'receiver','amount','reference', 'status', 'created_at', 'transaction'}

class DashboardSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=55)
    wallet = serializers.CharField(max_length=10)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    status = serializers.CharField(max_length=10)
    transactions = RecentTransactionsSerializer(many=True)
