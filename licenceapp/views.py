
from rest_framework import viewsets


from account.models import CustomUser

from licenceapp.serializers import LicenceSerializer

from rest_framework.permissions import IsAuthenticated



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pandas as pd
from django.utils import timezone

from licenceapp.models import Source, Matiere, Niveau,  Licence

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
                'file', openapi.IN_FORM, description="Excel file with user emails, subjects, levels", type=openapi.TYPE_FILE, required=True
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
            400: openapi.Response('Source ID and file are required.'),
            404: openapi.Response('Source not found.')
        }
    )
    @transaction.atomic
    def post(self, request):
        source_id = request.data.get('source_id')
        file = request.FILES.get('file')
        num_licences = request.data.get('num_licences')
        licence_duration = request.data.get('licence_duration')

        if not source_id or not file or not num_licences or not licence_duration:
            return Response({'detail': 'Source ID, file, number of licences, and licence duration are required.'}, status=status.HTTP_400_BAD_REQUEST)

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
            niveau_name = row['niveau']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                continue

            if user.source.id != source.id:
                continue

            matiere, _ = Matiere.objects.get_or_create(name=matiere_name)
            niveau, _ = Niveau.objects.get_or_create(name=niveau_name)

            licence = Licence.objects.create(
                date_exp=timezone.now() + timezone.timedelta(days=int(licence_duration)),
                classe=source.classe,
                niveau=niveau,
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
                'file', openapi.IN_FORM, description="Excel file with user emails, subjects, levels, duration of stay", type=openapi.TYPE_FILE, required=True
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
            400: openapi.Response('Source ID and file are required.'),
            404: openapi.Response('Source not found.')
        }
    )
    @transaction.atomic
    def post(self, request):
        source_id = request.data.get('source_id')
        file = request.FILES.get('file')
        num_licences = request.data.get('num_licences')
        licence_duration = request.data.get('licence_duration')

        if not source_id or not file or not num_licences or not licence_duration:
            return Response({'detail': 'Source ID, file, number of licences, and licence duration are required.'}, status=status.HTTP_400_BAD_REQUEST)

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
            niveau_name = row['niveau']
            duree_sejour = row['duree_sejour']  # Additional information

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                continue

            if user.source.id != source.id:
                continue

            matiere, _ = Matiere.objects.get_or_create(name=matiere_name)
            niveau, _ = Niveau.objects.get_or_create(name=niveau_name)

            licence = Licence.objects.create(
                date_exp=timezone.now() + timezone.timedelta(days=int(licence_duration)),
                classe=source.classe,
                niveau=niveau,
                source=source,
                user=user,
                type='enseignant',
                duree_sejour=duree_sejour
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