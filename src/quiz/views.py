from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Choice, QuizTaker
from account.models import *
from templates import *
from .forms import CreateQuizForm
from .forms import QuestionFormSet, ChoiceFormSet

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'start_quiz.html', {'quiz': quiz, 'questions': questions})

def submit_quiz(request, quiz_id):
    context = {}
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        user = request.user  # Assuming user is authenticated
        quiz_taker = QuizTaker.objects.create(user=user, quiz=quiz)
        
        quiz_score = 0
        for question in quiz.question_set.all():
            choice_id = request.POST.get(f'question_{question.id}', None)
            if choice_id:
                selected_choice = Choice.objects.get(id=choice_id)
                if selected_choice.is_correct:
                    quiz_score += 1

        user.quiz_score = quiz_score
        user.save()
        
        return redirect('quiz_result', quiz_id=quiz.id)

def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    user = request.user  # Assuming user is authenticated
    quiz_taker = QuizTaker.objects.filter(user=user, quiz=quiz).first()
    return render(request, 'quiz_result.html', {'quiz_taker': quiz_taker})


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
