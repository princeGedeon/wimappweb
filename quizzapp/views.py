import pandas as pd
from django.db import transaction
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from licenceapp import permissions
from licenceapp.models import Niveau, Classe, Matiere
from licenceapp.permissions import ValidLicencePermission, TeacherLicencePermission
from quizzapp.models import Quiz, Choice, Question
from quizzapp.serializers import QuizDetailSerializer, QuizCreateSerializer


# Create your views here.
class MyQuizListView(generics.ListAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated,ValidLicencePermission]

    def get_queryset(self):
        user = self.request.user
        return Quiz.objects.filter(
            classe__in=user.licences.values_list('classe', flat=True),
            matiere__in=user.licences.values_list('matiere', flat=True),
            niveau__in=user.licences.values_list('niveau', flat=True),
            is_active=True
        )

class CreateQuizView(generics.CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated, TeacherLicencePermission]

    @swagger_auto_schema(
        operation_description="Create a new quiz.",
        request_body=QuizCreateSerializer,
        responses={201: QuizDetailSerializer()}
    )
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PublicQuizListView(generics.ListAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Quiz.objects.filter(is_publied=True, is_active=True)
        classe = self.request.query_params.get('classe')
        matiere = self.request.query_params.get('matiere')
        niveau = self.request.query_params.get('niveau')

        if classe:
            queryset = queryset.filter(classe=classe)
        if matiere:
            queryset = queryset.filter(matiere=matiere)
        if niveau:
            queryset = queryset.filter(niveau=niveau)

        return queryset

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated]

class QuizDeleteView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated, TeacherLicencePermission]

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)



class CreatedQuizListView(generics.ListAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [IsAuthenticated, TeacherLicencePermission]

    def get_queryset(self):
        return Quiz.objects.filter(created_by=self.request.user)



class ImportCreateQuizView(APIView):
    permission_classes = [IsAuthenticated, TeacherLicencePermission]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Import questions and choices for a quiz from an Excel file",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, description="Title of the quiz", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description', openapi.IN_FORM, description="Description of the quiz", type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('classe', openapi.IN_FORM, description="Class of the quiz", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('matiere', openapi.IN_FORM, description="Subject of the quiz", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('niveau', openapi.IN_FORM, description="Level of the quiz", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('start_time', openapi.IN_FORM, description="Start time of the quiz", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, required=True),
            openapi.Parameter('end_time', openapi.IN_FORM, description="End time of the quiz", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, required=True),
            openapi.Parameter('duration', openapi.IN_FORM, description="Duration of the quiz in minutes", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('file', openapi.IN_FORM, description="Excel file with questions and choices", type=openapi.TYPE_FILE, required=True)
        ],
        responses={
            201: openapi.Response('Quiz created successfully.'),
            400: openapi.Response('Invalid request.'),
        }
    )
    @transaction.atomic
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        classe_name = request.data.get('classe')
        matiere_name = request.data.get('matiere')
        niveau_name = request.data.get('niveau')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        duration = request.data.get('duration')
        file = request.FILES.get('file')

        if not all([title, classe_name, matiere_name, niveau_name, start_time, end_time, duration, file]):
            return Response({'detail': 'All parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            classe = Classe.objects.get(name=classe_name)
        except Classe.DoesNotExist:
            return Response({'detail': 'Class not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            matiere = Matiere.objects.get(name=matiere_name)
        except Matiere.DoesNotExist:
            return Response({'detail': 'Subject not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            niveau = Niveau.objects.get(name=niveau_name)
        except Niveau.DoesNotExist:
            return Response({'detail': 'Level not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            data = pd.read_excel(file)
        except Exception as e:
            return Response({'detail': f'Invalid file format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            quiz = Quiz.objects.create(
                title=title,
                description=description,
                created_by=user,
                classe=classe,
                matiere=matiere,
                niveau=niveau,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                is_active=True,
                is_publied=False
            )

            for index, row in data.iterrows():
                question_text = row['question']
                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text
                )

                for choice_num in range(1, 5):
                    choice_text = row.get(f'choice{choice_num}')
                    if choice_text and not pd.isna(choice_text):
                        is_correct = (choice_text == row['correct_choice'])
                        Choice.objects.create(
                            question=question,
                            text=choice_text,
                            is_correct=is_correct
                        )

        except Exception as e:
            transaction.set_rollback(True)
            return Response({'detail': f'Error creating quiz: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Quiz created successfully.'}, status=status.HTTP_201_CREATED)