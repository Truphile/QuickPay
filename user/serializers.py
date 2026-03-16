from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
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
        wallet.objects.create(owner=user, wallet_name=user.phone[1:])
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message": "Email does not exist"})
        if not user.check_password(password):
            raise serializers.ValidationError({"message": "Invalid password"})
        if not user.is_active:
            raise serializers.ValidationError({"message": "User Account is not active"})

        refresh = RefreshToken.for_user(user)
        return {"user": user.id,"access": str(refresh.access_token),"refresh": str(refresh)}