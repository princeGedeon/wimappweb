from django.contrib import admin

from licenceapp.models import Classe,Matiere,Niveau,Licence


# Register your models here.
@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('typeLicence', 'date_exp', 'valeur', 'is_active')
    search_fields = ('valeur',)
    list_filter = ('typeLicence', 'is_active')
