from django.contrib.auth import get_user_model, authenticate, login
from djoser.serializers import UserCreateSerializer

# Djoser Serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from requests import HTTPError
from rest_framework import serializers, generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import AuthForbidden, AuthTokenError, MissingBackend
from social_django.utils import load_backend, load_strategy
from licenceapp.models import Licence, Matiere
from licenceapp.serializers import LicenceSerializer
from .models import CustomUser
User = get_user_model()
from rest_framework import serializers
from django.utils import timezone
from rest_framework import serializers


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = serializers.SocialSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return Response({
                'error': 'Please provide a valid provider'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')

            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)
        except HTTPError as error:
            return Response({
                "error": "Invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "Invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            # generate JWT token
            login(request, authenticated_user)
            data = {
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            # customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token')
            }
            return Response(status=status.HTTP_200_OK, data=response)

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)


class AssignTuteurSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id','is_auto','email', 'password', 'username','secondary_email', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilImg', 'typeCompte')

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilImg', 'typeCompte')

class UserCreateSerializer(UserCreateSerializer):
    """Serializer for creating user."""
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username","password")

class ProfileImageUpdateSerializer(serializers.ModelSerializer):
    profilImg = serializers.ImageField(required=True)
    class Meta:
        model = CustomUser
        fields = ['profilImg']

    def update(self, instance, validated_data):
        instance.profilImg = validated_data.get('profilImg', instance.profilImg)
        instance.save()
        return instance


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('Compte non validé.')
            if user.is_auto:
                raise serializers.ValidationError('Vous devez changer de mot de passe.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data
class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

class CustomUserSerializer(serializers.ModelSerializer):
    licences = LicenceSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id','email', 'username', "is_auto",'age', 'genre', 'numTel', 'pays', 'ville','fcm', 'profilImg', 'typeCompte', 'is_active', 'is_admin', 'is_staff_member', 'is_superuser', 'licences']