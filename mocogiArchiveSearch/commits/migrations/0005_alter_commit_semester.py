# Generated by Django 5.1.3 on 2024-12-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commits', '0004_alter_module_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='semester',
            field=models.CharField(default='Winter', max_length=10),
        ),
    ]
