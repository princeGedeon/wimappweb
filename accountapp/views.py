# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CustomUser, OTP
from .serializers import CustomUserUpdateSerializer, CustomUserCreateSerializer, AssignTuteurSerializer, \
    ProfileImageUpdateSerializer, CustomLoginSerializer
from django.conf import settings
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from accountapp.models import CustomUser
from accountapp.serializers import CustomUserCreateSerializer
from firebase_admin import auth as firebase_auth
import random

from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
import firebase
class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        id_token = request.data.get('id_token')
        print("ID Token:", id_token)  # Debugging: Print the id_token to verify
        return super().post(request, *args, **kwargs)



class GoogleLoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Authentifier un utilisateur avec le jeton d'identification Google",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_token': openapi.Schema(type=openapi.TYPE_STRING, description='Jeton d\'identification Google')
            },
            required=['id_token']
        ),
        responses={
            200: openapi.Response(
                description="Authentification réussie",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string"
                    }
                }
            ),
            400: openapi.Response(
                description="Requête invalide",
                examples={
                    "application/json": {
                        "detail": "Jeton d'identification requis."
                    }
                }
            ),
            404: openapi.Response(
                description="Utilisateur non trouvé",
                examples={
                    "application/json": {
                        "detail": "Utilisateur non trouvé."
                    }
                }
            ),
            500: openapi.Response(
                description="Erreur interne du serveur",
                examples={
                    "application/json": {
                        "detail": "Erreur lors de la vérification du jeton."
                    }
                }
            ),
        }
    )
    def post(self, request):
        id_token = request.data.get("id_token")
        if not id_token:
            return Response({"detail": "Jeton d'identification requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Vérifier le jeton avec Firebase Admin SDK
            decoded_token = firebase_auth.verify_id_token(id_token)
            email = decoded_token.get('email')
            google_user_id = decoded_token.get('uid')

            if not email:
                return Response({"detail": "Impossible de récupérer l'email à partir du jeton."}, status=status.HTTP_400_BAD_REQUEST)

            # Vérifier si l'utilisateur existe déjà dans la base de données
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Créer un nouvel utilisateur s'il n'existe pas
                user_data = {
                    "email": email,
                    "password": None,  # Vous pouvez générer un mot de passe aléatoire si nécessaire
                    "username": decoded_token.get('name', ''),
                    'age': None,
                    'genre': None,
                    'numTel': "",
                    'pays': "",
                    'ville': "",
                    'typeCompte': "STANDARD"
                }
                serializer = CustomUserCreateSerializer(data=user_data)
                if serializer.is_valid():
                    user = serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Générer un jeton JWT pour l'utilisateur
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except firebase_auth.InvalidIdTokenError:
            return Response({"detail": "Jeton d'identification invalide."}, status=status.HTTP_400_BAD_REQUEST)
        except firebase_auth.ExpiredIdTokenError:
            return Response({"detail": "Jeton d'identification expiré."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Erreur lors de la vérification du jeton."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateUserInfoView(generics.UpdateAPIView):
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class CustomUserCreateView(generics.CreateAPIView):
    serializer_class = CustomUserCreateSerializer
    permission_classes = [AllowAny]


class GenerateOTPAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Générer et envoyer un OTP par email",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Adresse email de l\'utilisateur')
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(
                description="OTP envoyé par email",
                examples={
                    "application/json": {
                        "detail": "OTP envoyé par email."
                    }
                }
            ),
            400: openapi.Response(
                description="Requête invalide",
                examples={
                    "application/json": {
                        "detail": "Email requis."
                    }
                }
            ),
            404: openapi.Response(
                description="Utilisateur non trouvé",
                examples={
                    "application/json": {
                        "detail": "Utilisateur non trouvé."
                    }
                }
            ),
        }
    )
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        otp_code = str(random.randint(1000, 9999))
        OTP.objects.create(user=user, code=otp_code)

        send_mail(
            "Votre code de vérification",
            f"Votre code de vérification est {otp_code}",
            "from@example.com",
            [email],
        )

        return Response({"detail": "OTP envoyé par email."}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Vérifier l'OTP et activer le compte utilisateur",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Adresse email de l\'utilisateur'),
                'otp_code': openapi.Schema(type=openapi.TYPE_STRING, description='Code OTP reçu par email')
            },
            required=['email', 'otp_code']
        ),
        responses={
            200: openapi.Response(
                description="Compte activé avec succès",
                examples={
                    "application/json": {
                        "detail": "Compte activé avec succès."
                    }
                }
            ),
            400: openapi.Response(
                description="Requête invalide",
                examples={
                    "application/json": {
                        "detail": "Email et OTP requis.",
                        "detail": "OTP invalide.",
                        "detail": "OTP expiré."
                    }
                }
            ),
            404: openapi.Response(
                description="Utilisateur non trouvé",
                examples={
                    "application/json": {
                        "detail": "Utilisateur non trouvé."
                    }
                }
            ),
        }
    )
    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        if not email or not otp_code:
            return Response({"detail": "Email et OTP requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp = OTP.objects.get(user=user, code=otp_code)
        except OTP.DoesNotExist:
            return Response({"detail": "OTP invalide."}, status=status.HTTP_400_BAD_REQUEST)

        if not otp.is_valid():
            return Response({"detail": "OTP expiré."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        otp.delete()

        return Response({"detail": "Compte activé avec succès."}, status=status.HTTP_200_OK)



"""class AppleLogin(SocialLoginView):
    adapter_class = AppleOAuth2Adapter
"""



class ProfileImageUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Upload and update the profile image for the logged-in user",
        manual_parameters=[
            openapi.Parameter(
                'profilImg',
                openapi.IN_FORM,
                description="Image file to upload",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Profile image updated successfully",
                examples={"application/json": {"detail": "Profile image updated successfully"}}
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={"application/json": {"profilImg": ["A valid image is required."]}}
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileImageUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Profile image updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssignTuteurView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Assigner un tuteur à un utilisateur",
        request_body=AssignTuteurSerializer,
        responses={
            200: openapi.Response("Tuteur assigné avec succès."),
            400: openapi.Response("Requête invalide."),
            500: openapi.Response("Erreur interne du serveur.")
        }
    )
    def post(self, request):
        try:
            email = request.data.get('email')

            if not email:
                return Response({'error': 'email du parent est requis est requis.'}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user

            if user.age is not None and user.age <= 15:
                user.secondary_email=user.email
                user.email = email
                user.save()
                return Response({'success': 'Email du tuteur assigné avec succès.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'L\'âge de l\'utilisateur doit être de 15 ans ou moins pour assigner un tuteur.'}, status=status.HTTP_400_BAD_REQUEST)

        except (ObjectDoesNotExist, KeyError):
            return Response({'error': 'Email du  tuteur fourni invalide.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomLoginView(APIView):
    @swagger_auto_schema(
        request_body=CustomLoginSerializer,
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    'application/json': {
                        'refresh': 'string',
                        'access': 'string',
                        'user': {
                            'id': 'integer',
                            'email': 'string'
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    'application/json': {
                        'email': [
                            'This field is required.'
                        ],
                        'password': [
                            'This field is required.'
                        ],
                        'non_field_errors': [
                            'Invalid email or password.',
                            'Compte non validé.'
                        ]
                    }
                }
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)