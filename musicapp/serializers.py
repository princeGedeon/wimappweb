from rest_framework import serializers
from .models import Music, Playlist, Favori

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'id', 'beatmaker', 'classe', 'date_created', 'duree_enreg', 'ecoutes',
            'interprete', 'isFree', 'lyrics_enreg', 'style_enreg', 'matiere', 'theme',
            'url_enreg', 'url_img', 'url_mp3', 'file_enreg', 'file_img', 'file_mp3'
        ]

class MusicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = [
            'beatmaker', 'classe', 'duree_enreg', 'ecoutes', 'interprete', 'isFree',
            'lyrics_enreg', 'style_enreg', 'matiere', 'theme', 'url_enreg', 'url_img',
            'url_mp3', 'file_enreg', 'file_img', 'file_mp3'
        ]

class PlaylistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = [
            'id', 'nom', 'is_public', 'classe', 'matiere', 'created_by', 'musics'
        ]

class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            'nom', 'is_public', 'classe', 'matiere', 'created_by'
        ]

class FavoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = [
            'id', 'user', 'musics', 'title'
        ]

class FavoriCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favori
        fields = [
            'user', 'musics', 'title'
        ]

class FavoriGetSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True)

    class Meta:
        model = Favori
        fields = [
            'id', 'title', 'musics'
        ]
