# Generated by Django 5.1.3 on 2024-12-25 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('semester', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ModuleCommit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FileField(upload_to='module_commit_files/')),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commits.commit')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commits.module')),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='commits',
            field=models.ManyToManyField(related_name='modules', through='commits.ModuleCommit', to='commits.commit'),
        ),
    ]
