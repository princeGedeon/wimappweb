import pandas as pd
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accountapp.models import CustomUser
from licenceapp.models import Source, Matiere, Licence
from licenceapp.constants import NIVEAU_CHOICES, CLASSE_CHOICES
from licenceapp.serializers import LicenceSerializer



class UploadLicencesForStudentsView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Upload a file to create licences for students and assign them to users",
        manual_parameters=[
            openapi.Parameter(
                'source_id', openapi.IN_FORM, description="ID of the source", type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                'classe', openapi.IN_FORM, description="Class of the licence", type=openapi.TYPE_STRING, required=False, enum=[choice[0] for choice in CLASSE_CHOICES]
            ),
            openapi.Parameter(
                'niveau', openapi.IN_FORM, description="Level of the licence", type=openapi.TYPE_STRING, required=False, enum=[choice[0] for choice in NIVEAU_CHOICES]
            ),
            openapi.Parameter(
                'file', openapi.IN_FORM, description="Excel file with user emails and subjects", type=openapi.TYPE_FILE, required=True
            ),
            openapi.Parameter(
                'num_licences', openapi.IN_FORM, description="Number of licences", type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                'licence_duration', openapi.IN_FORM, description="Duration of the licence in days", type=openapi.TYPE_INTEGER, required=True
            ),
        ],
        responses={
            201: openapi.Response('Licences created and users notified.'),
            400: openapi.Response('Source ID, classe/niveau, and file are required.'),
            404: openapi.Response('Source not found.')
        }
    )
    @transaction.atomic
    def post(self, request):
        source_id = request.data.get('source_id')
        classe = request.data.get('classe')
        niveau = request.data.get('niveau')
        file = request.FILES.get('file')
        num_licences = request.data.get('num_licences')
        licence_duration = request.data.get('licence_duration')

        if not source_id or not (classe or niveau) or not file or not num_licences or not licence_duration:
            return Response({'detail': 'Source ID, classe or niveau, file, number of licences, and licence duration are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if classe and niveau:
            return Response({'detail': 'Only one of classe or niveau can be set.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source = Source.objects.get(id=source_id)
        except Source.DoesNotExist:
            return Response({'detail': 'Source not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = pd.read_excel(file)
        except Exception as e:
            return Response({'detail': f'Invalid file format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        users_notified = 0

        for index, row in data.iterrows():
            email = row['email']
            matiere_name = row['matiere']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                continue

            if user.source.id != source.id:
                continue

            matiere, _ = Matiere.objects.get_or_create(name=matiere_name)

            licence = Licence.objects.create(
                date_exp=timezone.now() + timezone.timedelta(days=int(licence_duration)),
                classe=classe if classe else None,
                niveau=niveau if niveau else None,
                source=source,
                user=user,
                type='etudiant'
            )

            user.licences.add(licence)
            self.send_notification_email(user.email, licence)
            users_notified += 1

        return Response({'detail': f'Licences created and {users_notified} users notified.'}, status=status.HTTP_201_CREATED)

    def send_notification_email(self, email, licence):
        subject = 'Nouvelle Licence Assignée'
        message = f'Vous avez reçu une nouvelle licence avec la valeur {licence.valeur}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)


class UploadLicencesForTeachersView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Upload a file to create licences for teachers and assign them to users",
        manual_parameters=[
            openapi.Parameter(
                'source_id', openapi.IN_FORM, description="ID of the source", type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                'classe', openapi.IN_FORM, description="Class of the licence", type=openapi.TYPE_STRING, required=False, enum=[choice[0] for choice in CLASSE_CHOICES]
            ),
            openapi.Parameter(
                'niveau', openapi.IN_FORM, description="Level of the licence", type=openapi.TYPE_STRING, required=False, enum=[choice[0] for choice in NIVEAU_CHOICES]
            ),
            openapi.Parameter(
                'file', openapi.IN_FORM, description="Excel file with user emails, subjects, and duration of stay", type=openapi.TYPE_FILE, required=True
            ),
            openapi.Parameter(
                'num_licences', openapi.IN_FORM, description="Number of licences", type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                'licence_duration', openapi.IN_FORM, description="Duration of the licence in days", type=openapi.TYPE_INTEGER, required=True
            ),
        ],
        responses={
            201: openapi.Response('Licences created and users notified.'),
            400: openapi.Response('Source ID, classe/niveau, and file are required.'),
            404: openapi.Response('Source not found.')
        }
    )
    @transaction.atomic
    def post(self, request):
        source_id = request.data.get('source_id')
        classe = request.data.get('classe')
        niveau = request.data.get('niveau')
        file = request.FILES.get('file')
        num_licences = request.data.get('num_licences')
        licence_duration = request.data.get('licence_duration')

        if not source_id or not (classe or niveau) or not file or not num_licences or not licence_duration:
            return Response({'detail': 'Source ID, classe or niveau, file, number of licences, and licence duration are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if classe and niveau:
            return Response({'detail': 'Only one of classe or niveau can be set.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source = Source.objects.get(id=source_id)
        except Source.DoesNotExist:
            return Response({'detail': 'Source not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = pd.read_excel(file)
        except Exception as e:
            return Response({'detail': f'Invalid file format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        users_notified = 0

        for index, row in data.iterrows():
            email = row['email']
            matiere_name = row['matiere']
            duree_sejour = row['duree_sejour']  # Additional information

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                continue

            if user.source.id != source.id:
                continue

            matiere, _ = Matiere.objects.get_or_create(name=matiere_name)

            licence = Licence.objects.create(
                date_exp=timezone.now() + timezone.timedelta(days=int(licence_duration)),
                classe=classe if classe else None,
                niveau=niveau if niveau else None,
                source=source,
                user=user,
                type='enseignant'
            )

            user.licences.add(licence)
            self.send_notification_email(user.email, licence)
            users_notified += 1

        return Response({'detail': f'Licences created and {users_notified} users notified.'}, status=status.HTTP_201_CREATED)

    def send_notification_email(self, email, licence):
        subject = 'Nouvelle Licence Assignée'
        message = f'Vous avez reçu une nouvelle licence avec la valeur {licence.valeur}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

class AddLicenceKey(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a licence to the user's profile",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'licence_key': openapi.Schema(type=openapi.TYPE_STRING, description='Licence key to add'),
            },
            required=['licence_key']
        ),
        responses={
            200: openapi.Response('Licence added successfully'),
            400: openapi.Response('Licence non assignable'),
            404: openapi.Response('Licence non trouvée')
        }
    )
    def post(self, request, format=None):
        user = request.user
        licence_key = request.data.get('licence_key')

        try:
            licence = Licence.objects.get(valeur=licence_key)
        except Licence.DoesNotExist:
            return Response({'detail': 'Licence non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

        if licence.is_assignable():
            user.licences.add(licence)
            licence.user = user
            licence.save()
            return Response({'detail': 'Licence ajoutée avec succès.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Licence non assignable.'}, status=status.HTTP_400_BAD_REQUEST)


class LicenceViewSet(viewsets.ModelViewSet):
    queryset = Licence.objects.all()
    serializer_class = LicenceSerializer
    permission_classes = [IsAdminUser]

class UpdateLevelLicencesView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Update licences for users from an Excel file",
        manual_parameters=[
            openapi.Parameter('source_id', openapi.IN_FORM, description="ID of the source", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('expiry_duration', openapi.IN_FORM, description="Duration of the licence in days", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('classe', openapi.IN_FORM, description="Name of the class", type=openapi.TYPE_STRING, required=False, enum=[choice[0] for choice in CLASSE_CHOICES]),
            openapi.Parameter('niveau', openapi.IN_FORM, description="Name of the level", type=openapi.TYPE_STRING, required=False, enum=[choice[0] for choice in NIVEAU_CHOICES]),
            openapi.Parameter('user_type', openapi.IN_FORM, description="Type of the user (enseignant/etudiant)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('file', openapi.IN_FORM, description="Excel file with user emails", type=openapi.TYPE_FILE, required=True),
        ],
        responses={
            200: openapi.Response('Licences updated successfully.'),
            400: openapi.Response('Invalid request.'),
            404: openapi.Response('Source not found.'),
            500: openapi.Response('Internal server error.')
        }
    )
    @transaction.atomic
    def post(self, request):
        source_id = request.data.get('source_id')
        expiry_duration = request.data.get('expiry_duration')
        classe = request.data.get('classe')
        niveau = request.data.get('niveau')
        user_type = request.data.get('user_type')
        file = request.FILES.get('file')

        if not source_id or not expiry_duration or not user_type or not file or not (classe or niveau):
            return Response({'detail': 'Source ID, expiry duration, user type, and file are required. One of classe or niveau must be set.'}, status=status.HTTP_400_BAD_REQUEST)

        if classe and niveau:
            return Response({'detail': 'Only one of classe or niveau can be set.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source = Source.objects.get(id=source_id)
        except Source.DoesNotExist:
            return Response({'detail': 'Source not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = pd.read_excel(file)
        except Exception as e:
            return Response({'detail': f'Invalid file format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        licences_updated = 0
        licences_created = 0

        for index, row in data.iterrows():
            email = row['email']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                continue

            if user.source.id != source.id:
                continue

            licence = user.licences.filter(type=user_type).first()
            if licence:
                if classe:
                    licence.classe = classe
                if niveau:
                    licence.niveau = niveau
                licence.date_exp = timezone.now() + timezone.timedelta(days=int(expiry_duration))
                licence.save()
                licences_updated += 1
            else:
                licence = Licence.objects.create(
                    date_exp=timezone.now() + timezone.timedelta(days=int(expiry_duration)),
                    classe=classe if classe else None,
                    niveau=niveau if niveau else None,
                    source=source,
                    user=user,
                    type=user_type
                )
                user.licences.add(licence)
                licences_created += 1

        return Response({'detail': f'{licences_updated} licences updated and {licences_created} licences created successfully.'}, status=status.HTTP_200_OK)
