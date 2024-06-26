from django.urls import path

from quizzapp.views import MyQuizListView, PublicQuizListView, QuizDetailView, QuizDeleteView, CreatedQuizListView, \
    CreateQuizView, ImportCreateQuizView

urlpatterns = [
    path('quizzes/my/', MyQuizListView.as_view(), name='get-my-quizzes'),
    path('quizzes/publied/', PublicQuizListView.as_view(), name='get-publied-quizzes'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz-delete'),
    path('quizzes/created/', CreatedQuizListView.as_view(), name='get-created-quizzes'),
    path('create-quiz/', CreateQuizView.as_view(), name='create-quiz'),
    path('import-quiz-from-excel/', ImportCreateQuizView.as_view(), name='import-quiz'),
]
