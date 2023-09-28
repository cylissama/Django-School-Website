# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('create/', views.create_quiz, name='create_quiz'),
]
