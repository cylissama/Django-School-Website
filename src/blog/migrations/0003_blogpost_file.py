# Generated by Django 4.2.4 on 2023-09-25 18:28

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='file',
            field=models.FileField(default='static/gov.png', upload_to=blog.models.upload_location),
        ),
    ]