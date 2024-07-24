# serializers.py

from rest_framework import serializers
from .models import Music, Playlist, Favori

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'

class FavoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = ['id', 'user', 'musics', 'title']

class FavoriGetSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True)

    class Meta:
        model = Favori
        fields = ['id', 'title', 'musics']