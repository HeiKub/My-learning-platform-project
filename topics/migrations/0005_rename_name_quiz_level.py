# Generated by Django 5.0.6 on 2024-09-26 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("topics", "0004_quiz_question_userresult"),
    ]

    operations = [
        migrations.RenameField(
            model_name="quiz",
            old_name="name",
            new_name="level",
        ),
    ]
