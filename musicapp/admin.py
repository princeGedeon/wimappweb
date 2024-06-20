from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Music, Playlist, Favori

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
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
    list_display = ('title', 'user', 'music')
    search_fields = ('title', 'user__email', 'music__theme')
    list_filter = ('user',)

