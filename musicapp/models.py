import uuid

from django.db import models

from account.models import CustomUser
from licenceapp.models import Classe, Matiere


# Create your models here.
class Music(models.Model):
    beatmaker = models.CharField(max_length=255)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    duree_enreg = models.IntegerField(help_text="Duration in seconds")
    ecoutes = models.IntegerField(default=0)
    interprete = models.CharField(max_length=255)
    isFree = models.BooleanField(default=True)
    lyrics_enreg = models.TextField(null=True, blank=True)
    style_enreg = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)
    url_enreg = models.URLField()
    url_img = models.URLField(null=True, blank=True)
    url_mp3 = models.URLField()

    def __str__(self):
        return self.theme

class Playlist(models.Model):
    nom = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    musics = models.ManyToManyField(Music, related_name='playlists')

    def __str__(self):
        return self.nom



class Favori(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favoris')
    musics = models.ManyToManyField(Music, related_name='favoris')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
