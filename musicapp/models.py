import uuid
import os
from urllib.parse import urlparse
import requests
from django.db import models
from django.core.files.base import ContentFile
from accountapp.models import CustomUser
from licenceapp.models import Matiere, Classe, Niveau


class StyleMusique(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


class Music(models.Model):
    beatmaker = models.CharField(max_length=255)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='musics')
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True, related_name='musics')
    date_created = models.DateTimeField(auto_now_add=True)
    duree_enreg = models.CharField(help_text="Duration in seconds", max_length=100, null=True, blank=True)
    ecoutes = models.IntegerField(default=0, null=True, blank=True)
    interprete = models.CharField(max_length=255)
    isFree = models.BooleanField(default=True)
    lyrics_enreg = models.TextField(null=True, blank=True)
    style_enreg = models.ForeignKey(StyleMusique, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='musics')
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True, blank=True, related_name='musics')
    theme = models.CharField(max_length=255)
    url_enreg = models.URLField()
    url_img = models.URLField(null=True, blank=True)
    url_mp3 = models.URLField()
    file_enreg = models.FileField(upload_to='enreg/', null=True, blank=True)
    file_img = models.FileField(upload_to='images/', null=True, blank=True)
    file_mp3 = models.FileField(upload_to='mp3/', null=True, blank=True)

    def __str__(self):
        return self.theme

    def download_files(self):
        # Validation des URL avant téléchargement
        if self.url_img and not self.file_img:
            response = requests.get(self.url_img)
            if response.status_code == 200:
                img_name = os.path.basename(urlparse(self.url_img).path)
                self.file_img.save(img_name, ContentFile(response.content), save=True)

        if self.url_enreg and not self.file_enreg:
            response = requests.get(self.url_enreg)
            if response.status_code == 200:
                enreg_name = os.path.basename(urlparse(self.url_enreg).path)
                self.file_enreg.save(enreg_name, ContentFile(response.content), save=True)

        if self.url_mp3 and not self.file_mp3:
            response = requests.get(self.url_mp3)
            if response.status_code == 200:
                mp3_name = os.path.basename(urlparse(self.url_mp3).path)
                self.file_mp3.save(mp3_name, ContentFile(response.content), save=True)


class Playlist(models.Model):
    nom = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')
    niveau = models.ForeignKey(Niveau, on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True, blank=True, related_name='playlists')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    musics = models.ManyToManyField(Music, related_name='playlists')

    def __str__(self):
        return f'{self.nom} (Public: {self.is_public})'


class Favori(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favoris')
    musics = models.ManyToManyField(Music, related_name='favoris')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} - {self.user.username}'
