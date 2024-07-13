import uuid

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.widgets import ForeignKeyWidget


from .models import Music, Playlist, Favori
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Music



class MusicResource(resources.ModelResource):


    enreg_ID = fields.Field(
        column_name='enreg_ID',
        attribute='id'
    )

    class Meta:
        model = Music
        import_id_fields = ['id']
        fields = ('id', 'beatmaker', 'classe', 'date_created', 'duree_enreg', 'ecoutes', 'interprete', 'isFree', 'lyrics_enreg', 'style_enreg',"matiere", 'theme', 'url_enreg', 'url_img', 'url_mp3')

    def before_import_row(self, row, **kwargs):
        # Generate enreg_ID if not present
        if 'enreg_ID' not in row or not row['enreg_ID']:
            row['enreg_ID'] = str(uuid.uuid4())

@admin.register(Music)
class MusicAdmin(ImportExportModelAdmin):
    resource_class = MusicResource
    list_display = ('theme', 'beatmaker', 'interprete', 'date_created', 'isFree','matiere')
    search_fields = ('theme', 'beatmaker', 'interprete')
    list_filter = ('isFree', 'classe', 'style_enreg',"matiere")
    actions = ['download_files_from_urls']

    def download_files_from_urls(self, request, queryset):
        for music in queryset:
            music.download_files()
        self.message_user(request, "Files downloaded successfully from URLs.")
    download_files_from_urls.short_description = "Download files from URLs"

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nom', 'is_public', 'classe', 'matiere',)
    search_fields = ('nom', )
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

