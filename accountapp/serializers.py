from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

# Djoser Serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers, generics, permissions, status
from rest_framework.response import Response

from licenceapp.models import Licence
from licenceapp.serializers import LicenceSerializer
from .models import CustomUser
User = get_user_model()




from rest_framework import serializers

from django.utils import timezone

class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'password', 'username', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilUrl', 'typeCompte')

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilUrl', 'typeCompte')

class UserCreateSerializer(UserCreateSerializer):

    """Serializer for creating user."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username","password")




class CustomUserSerializer(serializers.ModelSerializer):
    licences = LicenceSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'age', 'genre', 'numTel', 'pays', 'ville','fcm', 'profilUrl', 'typeCompte', 'is_active', 'is_admin', 'is_staff_member', 'is_superuser', 'licences']