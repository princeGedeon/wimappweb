
import uuid
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

class Source(models.Model):
    TYPE_CHOICES = [
        ('centre_formation', 'Centre de Formation'),
        ('personnel', 'Personnel'),
        ('Autre','Autre')
        # Ajoutez d'autres types selon vos besoins
    ]

    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.nom} ({self.type})'

class Licence(models.Model):
    date_exp = models.DateField()
    valeur = models.CharField(max_length=32, unique=True, editable=False, default=uuid.uuid4().hex)
    is_active = models.BooleanField(default=True)
    classes = models.ManyToManyField(Classe, related_name='licences')
    niveaux = models.ManyToManyField(Niveau, related_name='licences')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='licences')

    def disable(self):
        self.is_active = False
        self.save()

    def enable(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return f'{self.valeur} - {self.date_exp}'