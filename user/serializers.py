from rest_framework import serializers


from user.models import User
from wallet.models import Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user=User.objects.create_user(**validated_data)
        Wallet.objects.create(
            user=user,
            wallet_number=user.phone[1:]
        )
        return user