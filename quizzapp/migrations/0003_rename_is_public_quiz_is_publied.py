# Generated by Django 5.0.6 on 2024-06-24 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzapp', '0002_remove_quiz_background_music'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='is_public',
            new_name='is_publied',
        ),
    ]