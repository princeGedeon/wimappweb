import uuid

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.widgets import ForeignKeyWidget

from licenceapp.models import Classe
from .models import Music, Playlist, Favori
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Music

class ClasseWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return None
        classe, created = Classe.objects.get_or_create(name=value)
        return classe

class MusicResource(resources.ModelResource):
    classe = fields.Field(
        column_name='classe',
        attribute='classe',
        widget=ClasseWidget(Classe, 'name')
    )
    enreg_ID = fields.Field(
        column_name='enreg_ID',
        attribute='id'
    )

    class Meta:
        model = Music
        import_id_fields = ['id']
        fields = ('id', 'beatmaker', 'classe', 'date_created', 'duree_enreg', 'ecoutes', 'interprete', 'isFree', 'lyrics_enreg', 'style_enreg', 'theme', 'url_enreg', 'url_img', 'url_mp3')

    def before_import_row(self, row, **kwargs):
        # Generate enreg_ID if not present
        if 'enreg_ID' not in row or not row['enreg_ID']:
            row['enreg_ID'] = str(uuid.uuid4())
@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    resource_class = MusicResource
    list_display = ('theme', 'beatmaker', 'interprete', 'date_created', 'isFree')
    search_fields = ('theme', 'beatmaker', 'interprete')
    list_filter = ('isFree', 'classe', 'style_enreg')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nom', 'is_public', 'classe', 'matiere', 'created_by')
    search_fields = ('nom', 'created_by__email')
    list_filter = ('is_public', 'classe', 'matiere')
    filter_horizontal = ('musics',)

@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'display_musics')
    search_fields = ('title', 'user__email', 'musics__theme')
    list_filter = ('user', 'musics__theme')

    def display_musics(self, obj):
        return ", ".join([music.title for music in obj.musics.all()])

    display_musics.short_description = 'Musics'

