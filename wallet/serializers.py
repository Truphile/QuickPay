from rest_framework import serializers


class WalletTransferSerializer(serializers.ModelSerializer):
    recipient = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    idempotency_key = serializers.UUIDField(read_only=True)