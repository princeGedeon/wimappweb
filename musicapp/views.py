from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import viewsets, filters, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from licenceapp.permissions import ValidLicencePermission, StudentLicencePermission
from .filters import MusicFilter
from .models import Music, Playlist, Favori
from .serializers import MusicSerializer, PlaylistSerializer, FavoriSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from quizzapp.models import  Music


class MusicViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing musics.
    """
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['beatmaker', 'classe', 'interprete', 'isFree', 'style_enreg', 'theme','matiere']
    search_fields = ['beatmaker', 'interprete', 'lyrics_enreg', 'theme','matiere']
    ordering_fields = ['date_created', 'duree_enreg', 'ecoutes']

    @swagger_auto_schema(
        operation_description="Get all musics",
        responses={200: MusicSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get a music by ID",
        responses={200: MusicSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class CreatePlaylistView(generics.CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, ValidLicencePermission]

class GetSchoolPlaylistsView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, ValidLicencePermission]

    def get_queryset(self):
        user = self.request.user
        licence_source = user.licence.source
        return Playlist.objects.filter(created_by__licence__source=licence_source, created_by__licence__type='enseignant')



class GetMyPlaylistsView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, ValidLicencePermission]

    def get_queryset(self):
        return Playlist.objects.filter(created_by=self.request.user)

class GetMyFavorisView(generics.ListAPIView):
    serializer_class = FavoriSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favori.objects.filter(user=self.request.user)


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and editing playlists.
    """
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    #permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all playlists",
        responses={200: PlaylistSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AddToFavoritesView(generics.UpdateAPIView):
    serializer_class = FavoriSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a music to favorites",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'music_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the music to add to favorites')
            }
        ),
        responses={200: FavoriSerializer()}
    )
    def update(self, request, *args, **kwargs):
        music_id = request.data.get('music_id')
        user = request.user

        if not Music.objects.filter(id=music_id).exists():
            return Response({'detail': 'Music not found.'}, status=status.HTTP_404_NOT_FOUND)

        favori, created = Favori.objects.get_or_create(user=user, title="My Favorites")

        if music_id in favori.musics.values_list('id', flat=True):
            return Response({'detail': 'Music already in favorites.'}, status=status.HTTP_400_BAD_REQUEST)

        favori.musics.add(music_id)
        favori.save()
        serializer = self.get_serializer(favori)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserFavoritesView(generics.ListAPIView):
    serializer_class = MusicSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all favorite musics of the authenticated user",
        responses={200: MusicSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            favori = Favori.objects.get(user=user)
            musics = favori.musics.all()
            serializer = MusicSerializer(musics, many=True)
            return Response(serializer.data)
        except Favori.DoesNotExist:
            return Response({'detail': 'No favorites found.'}, status=404)


class PlaylistMusicsAPIView(APIView):
    """
    Récupère toutes les musiques d'une playlist spécifique.
    """

    @swagger_auto_schema(
        operation_description="Récupère toutes les musiques d'une playlist spécifique.",
        responses={200: MusicSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'pk',
                openapi.IN_PATH,
                description="ID de la playlist",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        musics = playlist.musics.all()
        filterset = MusicFilter(request.GET, queryset=musics)
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = MusicSerializer(filterset.qs, many=True)
        return Response(serializer.data)