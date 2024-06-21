from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

# Djoser Serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import CustomUser
User = get_user_model()





class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'password', 'fullname', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilUrl', 'typeCompte')

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('fullname', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilUrl', 'typeCompte')

class UserCreateSerializer(UserCreateSerializer):

    """Serializer for creating user."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "fullname","password")