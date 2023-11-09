from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect 
from .models import Quiz, Question, Choice, QuizTaker, SubmissionAttempts
from account.models import *
from templates import *
from .forms import CreateQuizForm, QuizForm
from .forms import QuestionFormSet, ChoiceFormSet
from mysite.urls import *

def display_score(request, quiz_taker):
    context = {}
    context['quiz_taker'] = quiz_taker

    return render(request, 'disp_score.html', context)

def study_view(request):
    context = {}
    return render(request, 'study_page.html', context)

def math_view(request):
    context = {}
    quizzes = Quiz.objects.all()
    user = request.user
    quiz_takers = QuizTaker.objects.all()
    context['quiz_takers'] = quiz_takers
    context['user'] = user
    context['quizzes'] = quizzes
    return render(request, 'math_page.html', context)

def cs_view(request):
    context = {}
    quizzes = Quiz.objects.all()
    user = request.user
    quiz_takers = QuizTaker.objects.all()
    context['quiz_takers'] = quiz_takers
    context['user'] = user
    context['quizzes'] = quizzes
    return render(request, 'cs_page.html', context)

def ds_view(request):
    context = {}
    quizzes = Quiz.objects.all()
    user = request.user
    quiz_takers = QuizTaker.objects.all()
    context['quiz_takers'] = quiz_takers
    context['user'] = user
    context['quizzes'] = quizzes
    return render(request, 'ds_page.html', context)

def reading_view(request):
    context = {}
    quizzes = Quiz.objects.all()
    user = request.user
    quiz_takers = QuizTaker.objects.all()
    context['quiz_takers'] = quiz_takers
    context['user'] = user
    context['quizzes'] = quizzes
    return render(request, 'reading_page.html', context)

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def start_quiz(request, quiz_id):
    context = {}
    taken = 0
    user = request.user  # Assuming user is authenticated
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if QuizTaker.objects.filter(user=user, quiz=quiz).exists():
        quiz_taker = QuizTaker.objects.get(user=user, quiz=quiz)
        print("getting user")
    else:
        quiz_taker = QuizTaker.objects.create(user=user, quiz=quiz)
        print("creating user")

    if quiz_taker.attempts >= 3:
        taken = 1
    else:
        print(quiz_taker.attempts)
        quiz_taker.attempts += 1
        quiz_taker.save()


    return render(request, 'start_quiz.html', {'taken': taken, 'quiz': quiz, 'questions': questions, 'quiz_taker': quiz_taker})

def submit_quiz(request, quiz_id):
    context = {}

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user  # Assuming user is authenticated
 
    if request.method == 'POST':

        if QuizTaker.objects.filter(user=user, quiz=quiz).exists():
            quiz_taker = QuizTaker.objects.get(user=user, quiz=quiz)
            print("getting user")
        else:
            quiz_taker = QuizTaker.objects.create(user=user, quiz=quiz)
            print("creating user")

        #reset score on next attempt
        quiz_taker.quiz_score = 0

        totQ = 0.00
        for question in quiz.question_set.all():
            totQ = totQ + 1
            choice_id = request.POST.get(f'question_{question.id}', None)
            if choice_id:
                selected_choice = Choice.objects.get(id=choice_id)
                SubmissionAttempts.objects.create(quiz=quiz, taker=quiz_taker, chosen=selected_choice)
                if selected_choice.is_correct:
                    quiz_taker.quiz_score += 1.0

        quiz_taker.quiz_score = (quiz_taker.quiz_score / totQ) * 100.00

        quiz_taker.save()
        
        return redirect('quiz_result', quiz_id=quiz.id)

def quiz_result(request, quiz_id):
    context = {}
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user  # Assuming user is authenticated
    quiz_taker = QuizTaker.objects.get(user=user, quiz=quiz)
    context['quiz_taker'] = quiz_taker
    return render(request, 'quiz_result.html', context)


def create_quiz(request):
    if request.method == "POST":
        form=QuizForm(request.POST)
        if form.is_valid():
            return redirect(request,"create_quiz.html")
    else:
        form=QuizForm()
    
    return render(request, "create_quiz.html", {"form": form})
