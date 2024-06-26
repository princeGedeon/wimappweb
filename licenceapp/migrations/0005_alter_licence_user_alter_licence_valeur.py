# Generated by Django 5.0.6 on 2024-06-23 22:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenceapp', '0004_licence_type_alter_licence_valeur'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_licences', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='licence',
            name='valeur',
            field=models.CharField(default='e866d37084924209a31b1515aec88ff2', editable=False, max_length=32, unique=True),
        ),
    ]