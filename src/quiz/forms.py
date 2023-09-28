from django import forms
from quiz.models import Question, Quiz, Choice, QuizTaker
from django.forms import inlineformset_factory

"""class QuizForm(forms.Form):
    def __init__(self, data, questions, *args, **kwargs):
        self.questions = questions
        for question in questions:
            field_name = "question_%d" % question.pk
            choices = []
            for answer in question.answer_set().all():
                choices.append((answer.pk, answer.answer,))
            ## May need to pass some initial data, etc:
            field = forms.ChoiceField(label=question.question, required=True, 
                                      choices=choices, widget=forms.RadioSelect)
        return super(QuizForm, self).__init__(data, *args, **kwargs)

        def save(self):
"""
class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description']

# Create a formset for questions
QuestionFormSet = inlineformset_factory(Quiz, Question, fields=['text'], extra=1, can_delete=False)

# Create a formset for choices
ChoiceFormSet = inlineformset_factory(Question, Choice, fields=['text', 'is_correct'], extra=1, can_delete=False)