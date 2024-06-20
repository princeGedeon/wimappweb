from django.db import models

from account.models import CustomUser
from licenceapp.models import Classe, Matiere, Niveau
from musicapp.models import Music


# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quizzes')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False)
    background_music = models.ForeignKey(Music, on_delete=models.SET_NULL, null=True, blank=True)

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