# Generated by Django 5.1.11 on 2025-07-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_project_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='level',
            field=models.CharField(default='beginner', max_length=255),
        ),
        migrations.AddField(
            model_name='step',
            name='ordering',
            field=models.IntegerField(default=1),
        ),
    ]
