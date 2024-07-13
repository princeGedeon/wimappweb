import django_filters

from musicapp.models import Playlist, Music


class MyPlaylistFilter(django_filters.FilterSet):
    classe = django_filters.CharFilter(field_name='classe__name', lookup_expr='icontains')
    matiere = django_filters.CharFilter(field_name='matiere__name', lookup_expr='icontains')

    class Meta:
        model = Playlist
        fields = {
            'nom': ['exact', 'icontains'],
            'is_public': ['exact'],
            'classe': ['exact', 'icontains'],
            'matiere': ['exact', 'icontains']
        }
# filters.py


class MusicFilter(django_filters.FilterSet):
    class Meta:
        model = Music
        fields = {
            'beatmaker': ['exact', 'icontains'],
            'classe': ['exact'],
            'date_created': ['exact', 'year__gt'],
            'interprete': ['exact', 'icontains'],
            'isFree': ['exact'],
            'style_enreg': ['exact'],
            'theme': ['exact', 'icontains'],
        }
