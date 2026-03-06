from rest_framework import serializers


class WalletTransferSerializer(serializers.ModelSerializer):
    recipient_wallet = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField(read_only=True)

    def validate_amount(self, value):
        if value < 0:
            raise Exception("Amount cannot be negative")
        return value

