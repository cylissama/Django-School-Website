from django.urls import path
from . import views

from personal.views import (
    home_screen_view,
)

urlpatterns = [
    path('quizlist/', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    path('<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('study/', views.study_view, name='study_page'),
    path('math/', views.math_view, name='math_page'),
    path('', home_screen_view, name="home"),
]
