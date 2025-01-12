# Generated by Django 5.1.3 on 2024-12-28 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commits', '0009_studyprogram_course_programs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='department',
        ),
        migrations.AddField(
            model_name='course',
            name='abbrev',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(default='', max_length=150),
        ),
    ]
