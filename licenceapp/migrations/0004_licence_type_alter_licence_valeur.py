# Generated by Django 5.0.6 on 2024-06-22 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenceapp', '0003_remove_licence_classes_remove_licence_niveaux_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='licence',
            name='type',
            field=models.CharField(choices=[('etudiant', 'Étudiant'), ('enseignant', 'Enseignant')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='licence',
            name='valeur',
            field=models.CharField(default='d675bfdceb8a47399f8a6f37c2d22e13', editable=False, max_length=32, unique=True),
        ),
    ]