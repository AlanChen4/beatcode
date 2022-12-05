# Generated by Django 4.1.1 on 2022-12-05 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beatcodeApp', '0008_remove_todo_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='problem',
            name='category',
            field=models.ManyToManyField(blank=True, to='beatcodeApp.category'),
        ),
    ]
