# Generated by Django 4.0.2 on 2022-10-21 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beatcodeApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='category',
        ),
        migrations.AddField(
            model_name='problem',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='beatcodeApp.category'),
        ),
    ]