# Generated by Django 4.0.2 on 2022-10-14 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.TextField(choices=[('AR', 'Array'), ('BI', 'Binary'), ('DP', 'Dynamic Programming'), ('GR', 'Graph'), ('IN', 'Interval'), ('LL', 'Linked List'), ('MX', 'Matrix'), ('ST', 'String'), ('TR', 'Tree'), ('HE', 'Heap')], max_length=255, unique=True)),
                ('last_done', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('cat', models.ManyToManyField(to='beatcodeApp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('psid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.IntegerField(primary_key=True, serialize=False)),
                ('leetcode_username', models.TextField(unique=True)),
                ('password', models.TextField()),
                ('last_login', models.DateField()),
                ('is_active', models.BooleanField()),
                ('is_admin', models.BooleanField()),
                ('is_superuser', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('sid', models.IntegerField(primary_key=True, serialize=False)),
                ('sub_date', models.DateField()),
                ('runtime', models.IntegerField()),
                ('mem_used', models.IntegerField()),
                ('success', models.BooleanField()),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beatcodeApp.problem')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beatcodeApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='InSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beatcodeApp.problem')),
                ('psid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beatcodeApp.problemset')),
            ],
        ),
    ]