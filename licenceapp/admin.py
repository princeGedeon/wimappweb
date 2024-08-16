# admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Matiere, Source, Licence, Classe, Niveau


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'color']
    search_fields = ['nom', 'color']

class SourceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type')


class LicenceAdmin(admin.ModelAdmin):
    list_display = ('valeur', 'date_exp', 'is_active', 'classe', 'niveau', 'source', 'type', 'user')
    search_fields = ('valeur',)


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

admin.site.register(Source, SourceAdmin)
admin.site.register(Licence,LicenceAdmin)
