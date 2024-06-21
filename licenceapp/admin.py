# admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Classe, Matiere, Niveau, Source, Licence
from .forms import BulkLicenceForm
import uuid

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('name',)

class MatiereAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NiveauAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SourceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type')

class LicenceAdmin(admin.ModelAdmin):
    list_display = ('valeur', 'date_exp', 'is_active', 'source')
    list_filter = ('is_active', 'date_exp', 'source')
    search_fields = ('valeur', 'source__nom')

    change_list_template = "admin/licence_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk_add/', self.admin_site.admin_view(self.bulk_add_view), name="bulk_add_licences")
        ]
        return custom_urls + urls

    def bulk_add_view(self, request):
        if request.method == 'POST':
            form = BulkLicenceForm(request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, "Licences successfully created")
                return HttpResponseRedirect("../")
        else:
            form = BulkLicenceForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'add': True,
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_view_permission': True,
            'has_add_permission': True,
            'has_change_permission': True,
            'has_delete_permission': True,
        }

        return render(request, 'admin/bulk_add.html', context)

    def add_default_licence(self, request):
        if request.method == 'POST':
            source = request.POST.get('source')
            date_exp = request.POST.get('date_exp')
            classes = request.POST.getlist('classes')
            niveaux = request.POST.getlist('niveaux')

            licence = Licence.objects.create(
                source_id=source,
                date_exp=date_exp,
                valeur=uuid.uuid4().hex,
                is_active=True
            )
            licence.classes.set(classes)
            licence.niveaux.set(niveaux)
            licence.save()

            self.message_user(request, "Licence successfully created")
            return HttpResponseRedirect("../")

        sources = Source.objects.all()
        classes = Classe.objects.all()
        niveaux = Niveau.objects.all()

        context = {
            'sources': sources,
            'classes': classes,
            'niveaux': niveaux,
            'opts': self.model._meta,
            'add': True,
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_view_permission': True,
            'has_add_permission': True,
            'has_change_permission': True,
            'has_delete_permission': True,
        }

        return render(request, 'admin/add_default_licence.html', context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk_add/', self.admin_site.admin_view(self.bulk_add_view), name='bulk_add_licences'),
            path('add_default/', self.admin_site.admin_view(self.add_default_licence), name='add_default_licence')
        ]
        return custom_urls + urls

admin.site.register(Classe, ClasseAdmin)
admin.site.register(Matiere, MatiereAdmin)
admin.site.register(Niveau, NiveauAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Licence,LicenceAdmin)
