import uuid

from django.db import models

# Create your models here.
from django.db import models
from account.models import CustomUser

class Classe(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Matiere(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Niveau(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Licence(models.Model):
    VALEUR_CHOICES = [
        ('type_perso', 'Type Personnel'),
        ('type_cf', 'Type CF'),
        ('autre', 'Autre')
    ]

    typeLicence = models.CharField(max_length=20, choices=VALEUR_CHOICES)
    date_exp = models.DateField()
    valeur = models.CharField(max_length=32, unique=True, editable=False, default=uuid.uuid4().hex)
    is_active=models.BooleanField(default=True)

    def disable(self):
        # Logic to disable the licence
        pass

    def enable(self):
        # Logic to enable the licence
        pass

    def __str__(self):
        return f'{self.valeur} - {self.date_exp}'
