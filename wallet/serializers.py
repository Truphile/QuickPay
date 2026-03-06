from rest_framework import serializers

from wallet.models import Wallet


class WalletTransferSerializer(serializers.ModelSerializer):
    recipient_wallet = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField(read_only=True)

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

