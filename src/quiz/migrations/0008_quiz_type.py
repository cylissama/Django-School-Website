# Generated by Django 4.2.4 on 2023-10-17 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_alter_quiztaker_quiz_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='type',
            field=models.CharField(default='none', max_length=255),
        ),
    ]