from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Choice, QuizTaker
from account.models import *
from templates import *
from .forms import CreateQuizForm
from .forms import QuestionFormSet, ChoiceFormSet

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
    context['quizzes'] = quizzes
    return render(request, 'math_page.html', context)

def cs_view(request):
    context = {}
    quizzes = Quiz.objects.all()
    context['quizzes'] = quizzes
    return render(request, 'cs_page.html', context)

def ds_view(request):
    context = {}
    quizzes = Quiz.objects.all()
    context['quizzes'] = quizzes
    return render(request, 'ds_page.html', context)

def reading_view(request):
    context = {}
    quizzes = Quiz.objects.all()
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



        for question in quiz.question_set.all():
            choice_id = request.POST.get(f'question_{question.id}', None)
            if choice_id:
                selected_choice = Choice.objects.get(id=choice_id)
                if selected_choice.is_correct:
                    quiz_taker.quiz_score += 1.0
        
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
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')
        choice_formset = ChoiceFormSet(request.POST, prefix='choices')
        
        if form.is_valid() and question_formset.is_valid() and choice_formset.is_valid():
            # Save the quiz
            quiz = form.save()
            
            # Save the questions
            questions = question_formset.save(commit=False)
            for question in questions:
                question.quiz = quiz
                question.save()
                
            # Save the choices
            choices = choice_formset.save(commit=False)
            for choice in choices:
                choice.question = questions[0]  # Assuming all choices are for the first question
                choice.save()
            
            return redirect('quiz_list')  # Redirect to the quiz list page after quiz creation
    else:
        form = CreateQuizForm()
        question_formset = QuestionFormSet(prefix='questions')
        choice_formset = ChoiceFormSet(prefix='choices')
    
    return render(request, 'create_quiz.html', {
        'form': form,
        'question_formset': question_formset,
        'choice_formset': choice_formset,
    })
