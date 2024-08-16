
import django_filters
from musicapp.models import Playlist, Music

class MyPlaylistFilter(django_filters.FilterSet):
    classe = django_filters.CharFilter(field_name='classe__nom', lookup_expr='icontains')  # Assurez-vous que 'classe__nom' est utilisé
    matiere = django_filters.CharFilter(field_name='matiere__nom', lookup_expr='icontains')  # De même pour 'matiere__nom'

    class Meta:
        model = Playlist
        fields = {
            'nom': ['exact', 'icontains'],
            'is_public': ['exact'],
             }

