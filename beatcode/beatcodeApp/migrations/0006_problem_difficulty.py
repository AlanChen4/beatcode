# Generated by Django 4.1.1 on 2022-11-11 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beatcodeApp", "0005_remove_todo_progress_todo_complete"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="difficulty",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
