# Generated by Django 4.1.1 on 2022-12-02 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("beatcodeApp", "0007_alter_category_name"),
    ]

    operations = [
        migrations.RemoveField(model_name="todo", name="complete",),
    ]
