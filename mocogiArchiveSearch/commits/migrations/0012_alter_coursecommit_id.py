# Generated by Django 5.1.3 on 2024-12-29 08:21

import commits.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commits', '0011_course_recommended_semester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecommit',
            name='id',
            field=models.CharField(default=commits.models.generate_uuid, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
    ]
