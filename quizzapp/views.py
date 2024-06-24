from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from licenceapp import permissions
from licenceapp.permissions import ValidLicencePermission, TeacherLicencePermission
from quizzapp.models import Quiz
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
