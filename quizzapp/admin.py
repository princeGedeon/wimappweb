from django.contrib import admin

from quizzapp.models import QuizScore, StudentAnswer, Choice, Question, Quiz


# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'classe', 'matiere', 'niveau', 'start_time', 'end_time', 'duration', 'is_active', 'is_publied')
    search_fields = ('title', 'created_by__email', 'classe__name', 'matiere__name', 'niveau__name')
    list_filter = ('is_active', 'is_publied', 'classe', 'matiere', 'niveau')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text', 'quiz__title')
    list_filter = ('quiz',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text', 'question__text')
    list_filter = ('is_correct', 'question')

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'choice', 'answered_at')
    search_fields = ('student__email', 'question__text', 'choice__text')
    list_filter = ('answered_at',)

@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'quiz', 'score')
    search_fields = ('student__email', 'quiz__title')
    list_filter = ('score',)