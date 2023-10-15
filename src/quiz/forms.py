from django import forms
from quiz.models import Question, Quiz, Choice, QuizTaker
from django.forms import inlineformset_factory

class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description']

# Create a formset for questions
QuestionFormSet = inlineformset_factory(Quiz, Question, fields=['text'], extra=1, can_delete=False)

# Create a formset for choices
ChoiceFormSet = inlineformset_factory(Question, Choice, fields=['text', 'is_correct'], extra=1, can_delete=False)