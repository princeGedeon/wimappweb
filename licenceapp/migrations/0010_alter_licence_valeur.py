# Generated by Django 5.0.6 on 2024-06-26 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenceapp', '0009_alter_licence_valeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='valeur',
            field=models.CharField(default='e00d9f7bb76543eb97f262dbe15eeb32', editable=False, max_length=32, unique=True),
        ),
    ]