import pandas as pd
from django.db import models, transaction
from rest_framework import status
from rest_framework.response import Response

from accountapp.models import CustomUser
from licenceapp.constants import CLASSE_CHOICES, NIVEAU_CHOICES
from licenceapp.models import  Matiere
from musicapp.models import Music


# Create your models here.

class Quiz(models.Model):
    STATUS_CHOICES = [
        ('IS_PENDING', 'Pending'),
        ('IS_PLAYED', 'Played'),
        ('IS_FINISHED', 'Finished'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quizzes')
    classe = models.CharField(max_length=10, choices=CLASSE_CHOICES)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=10, choices=NIVEAU_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    is_publied = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IS_PENDING')


    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class StudentAnswer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.email} - {self.question.text}"

class QuizScore(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_scores')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_scores')
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.email} - {self.quiz.title} - {self.score}"

