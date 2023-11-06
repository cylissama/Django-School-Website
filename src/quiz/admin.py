
from django.contrib import admin
from .models import Quiz, Question, Choice, QuizTaker, SubmissionAttempts

#registered in the admin page
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuizTaker)
admin.site.register(SubmissionAttempts)