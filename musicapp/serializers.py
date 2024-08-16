from rest_framework import serializers
from .models import Music, Playlist, Favori, Classe, Niveau, Matiere, StyleMusique

class MusicSerializer(serializers.ModelSerializer):
    classe_name = serializers.CharField(source='classe.nom', read_only=True)
    niveau_name = serializers.CharField(source='niveau.nom', read_only=True)
    matiere_name = serializers.CharField(source='matiere.nom', read_only=True)  # Modification ici
    style_name = serializers.CharField(source='style_enreg.nom', read_only=True)

    class Meta:
        model = Music
        fields = [
            'id', 'beatmaker', 'classe_name', 'niveau_name', 'date_created', 'duree_enreg', 'ecoutes',
            'interprete', 'isFree', 'lyrics_enreg', 'style_name', 'matiere_name', 'theme',
            'url_enreg', 'url_img', 'url_mp3', 'file_enreg', 'file_img', 'file_mp3'
        ]

class MusicCreateSerializer(serializers.ModelSerializer):
    classe_name = serializers.CharField(write_only=True, required=False)
    niveau_name = serializers.CharField(write_only=True, required=False)
    matiere_name = serializers.CharField(write_only=True)
    style_name = serializers.CharField(write_only=True)

    class Meta:
        model = Music
        fields = [
            'beatmaker', 'classe_name', 'niveau_name', 'duree_enreg', 'ecoutes', 'interprete', 'isFree',
            'lyrics_enreg', 'style_name', 'matiere_name', 'theme', 'url_enreg', 'url_img',
            'url_mp3', 'file_enreg', 'file_img', 'file_mp3'
        ]

    def create(self, validated_data):
        classe_name = validated_data.pop('classe_name', None)
        niveau_name = validated_data.pop('niveau_name', None)
        matiere_name = validated_data.pop('matiere_name')
        style_name = validated_data.pop('style_name')

        classe = None
        niveau = None

        if classe_name:
            classe, _ = Classe.objects.get_or_create(nom=classe_name)
        if niveau_name:
            niveau, _ = Niveau.objects.get_or_create(nom=niveau_name)

        matiere, _ = Matiere.objects.get_or_create(nom=matiere_name)  # Modification ici
        style, _ = StyleMusique.objects.get_or_create(nom=style_name)

        music = Music.objects.create(
            classe=classe,
            niveau=niveau,
            matiere=matiere,
            style_enreg=style,
            **validated_data
        )
        return music

class PlaylistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, read_only=True)
    classe_name = serializers.CharField(source='classe.nom', read_only=True)
    niveau_name = serializers.CharField(source='niveau.nom', read_only=True)
    matiere_name = serializers.CharField(source='matiere.nom', read_only=True)  # Modification ici

    class Meta:
        model = Playlist
        fields = [
            'id', 'nom', 'is_public', 'classe_name', 'niveau_name', 'matiere_name', 'created_by', 'musics'
        ]

class PlaylistCreateSerializer(serializers.ModelSerializer):
    classe_name = serializers.CharField(write_only=True, required=False)
    niveau_name = serializers.CharField(write_only=True, required=False)
    matiere_name = serializers.CharField(write_only=True)

    class Meta:
        model = Playlist
        fields = [
            'nom', 'is_public', 'classe_name', 'niveau_name', 'matiere_name', 'created_by'
        ]

    def create(self, validated_data):
        classe_name = validated_data.pop('classe_name', None)
        niveau_name = validated_data.pop('niveau_name', None)
        matiere_name = validated_data.pop('matiere_name')

        classe = None
        niveau = None

        if classe_name:
            classe, _ = Classe.objects.get_or_create(nom=classe_name)
        if niveau_name:
            niveau, _ = Niveau.objects.get_or_create(nom=niveau_name)

        matiere, _ = Matiere.objects.get_or_create(nom=matiere_name)  # Modification ici

        playlist = Playlist.objects.create(
            classe=classe,
            niveau=niveau,
            matiere=matiere,
            **validated_data
        )
        return playlist

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
