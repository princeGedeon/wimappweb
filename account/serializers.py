from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

User = get_user_model()




# Djoser Serializers

class UserCreateSerializer(UserCreateSerializer):

    """Serializer for creating user."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "fullname","password")