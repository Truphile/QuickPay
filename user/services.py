from user.models import User


def create_user(validated_data):
    user = User.objects.create_user(**validated_data)
    user.save()
    return user

