# Generated by Django 4.0.2 on 2022-11-04 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beatcodeApp', '0003_remove_category_category_remove_category_last_done_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='problem_set',
            field=models.ManyToManyField(blank=True, to='beatcodeApp.ProblemSet'),
        ),
    ]