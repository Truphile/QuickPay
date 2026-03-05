from rest_framework import serializers

import wallet
from user.models import User
from wallet.models import Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        wallet.objects.create(user=user, wallet_name=user.phone[1:])
        return user