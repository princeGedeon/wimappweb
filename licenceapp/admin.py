# admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Classe, Matiere, Niveau, Source, Licence


class ClasseAdmin(admin.ModelAdmin):
    list_display = ('name',)

class MatiereAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NiveauAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SourceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type')


class LicenceAdmin(admin.ModelAdmin):
    list_display = ('valeur', 'date_exp', 'is_active', 'classe', 'niveau', 'source', 'type', 'user')
    search_fields = ('valeur',)

admin.site.register(Classe, ClasseAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Niveau, NiveauAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Licence,LicenceAdmin)
