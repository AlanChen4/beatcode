# Generated by Django 4.0.2 on 2022-11-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beatcodeApp', '0002_remove_problem_category_remove_todo_problem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category',
        ),
        migrations.RemoveField(
            model_name='category',
            name='last_done',
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('AR', 'Array'), ('BI', 'Binary'), ('DP', 'Dynamic Programming'), ('GR', 'Graph'), ('IN', 'Interval'), ('LL', 'Linked List'), ('MX', 'Matrix'), ('ST', 'String'), ('TR', 'Tree'), ('HE', 'Heap')], default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='problem_set',
            field=models.ManyToManyField(to='beatcodeApp.ProblemSet'),
        ),
        migrations.RemoveField(
            model_name='problem',
            name='category',
        ),
        migrations.AddField(
            model_name='problem',
            name='category',
            field=models.ManyToManyField(to='beatcodeApp.Category'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='problemset',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='todo',
            name='progress',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='ProblemToProblemSet',
        ),
    ]
