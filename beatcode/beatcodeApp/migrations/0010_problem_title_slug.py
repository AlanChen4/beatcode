# Generated by Django 4.1.1 on 2022-12-05 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beatcodeApp", "0009_todo_complete_alter_problem_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="title_slug",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
