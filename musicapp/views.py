from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import viewsets, filters, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from licenceapp.permissions import ValidLicencePermission, StudentLicencePermission
from .models import Music, Playlist, Favori
from .serializers import MusicSerializer, PlaylistSerializer, FavoriSerializer
from drf_yasg.utils import swagger_auto_schema

class MusicViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing musics.
    """
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['beatmaker', 'classe', 'interprete', 'isFree', 'style_enreg', 'theme']
    search_fields = ['beatmaker', 'interprete', 'lyrics_enreg', 'theme']
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
    permission_classes = [permissions.IsAuthenticated, StudentLicencePermission]

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
    permission_classes = [permissions.IsAuthenticated, ValidLicencePermission]

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


class FavoriViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing favoris.
    """
    queryset = Favori.objects.all()
    serializer_class = FavoriSerializer

    @swagger_auto_schema(
        operation_description="Get all favoris",
        responses={200: FavoriSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
