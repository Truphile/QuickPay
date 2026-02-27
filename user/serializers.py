from django.contrib.gis import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password']

        extra_kwargs = {'password': {'write_only': True}}