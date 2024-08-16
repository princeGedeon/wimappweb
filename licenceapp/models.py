from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    image=models.ImageField(null=True,blank=True,upload_to="matiere_img/")
    color=models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.nom

class Classe(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Niveau(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Source(models.Model):
    TYPE_CHOICES = [
        ('centre_formation', 'Centre de Formation'),
        ('personnel', 'Personnel'),
        ('Autre', 'Autre'),
        ('ecole', 'Ecole')
    ]
    nom = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.nom} ({self.type})'

class Licence(models.Model):
    TYPE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant')
    ]

    date_exp = models.DateField()
    valeur = models.CharField(max_length=32, unique=True, editable=False, default=uuid.uuid4().hex)
    is_active = models.BooleanField(default=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='licences')
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True, related_name='licences')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='licences')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='user_licences')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    createdAt = models.DateTimeField(auto_created=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def disable(self):
        self.is_active = False
        self.save()

    def enable(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return f'{self.valeur} - {self.date_exp}'

    def is_assignable(self):
        return self.is_active and self.date_exp >= timezone.now().date() and self.user is None
