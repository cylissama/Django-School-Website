from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from account.models import Account


# Create your models here.

class Quiz(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="empty")

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField(default="empty")

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizTaker(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} took {self.quiz.name} on {self.date_taken}"