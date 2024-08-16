from collections import defaultdict

from django.db import models
from django.shortcuts import render
from rest_framework import viewsets, filters, generics, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from licenceapp.permissions import ValidLicencePermission, StudentLicencePermission
from .filters import MyPlaylistFilter
from .mixins import LicenceFilterMixin, LicenceValidationMixin
from .models import Music, Playlist, Favori
from .serializers import (
    MusicSerializer,
    MusicCreateSerializer,
    PlaylistSerializer,
    PlaylistCreateSerializer,
    FavoriSerializer,
    FavoriCreateSerializer,
    FavoriGetSerializer
)

class MusicViewSet(LicenceValidationMixin, LicenceFilterMixin, viewsets.ModelViewSet):
    queryset = Music.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['beatmaker', 'classe__id', 'niveau__id', 'interprete', 'isFree', 'style_enreg__id', 'theme', 'matiere__id']
    search_fields = ['beatmaker', 'interprete', 'lyrics_enreg', 'theme', 'matiere__nom', 'classe__nom', 'niveau__nom']
    ordering_fields = ['date_created', 'duree_enreg', 'ecoutes']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MusicCreateSerializer
        return MusicSerializer

    @swagger_auto_schema(
        operation_description="Get all musics",
        responses={200: MusicSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'licence',
                openapi.IN_QUERY,
                description="Filter musics based on licence value",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'group_by',
                openapi.IN_QUERY,
                description="Grouper les musiques par un champ spécifique (ex: matiere, style_enreg, classe, niveau)",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply licence filter
        licence_value = request.GET.get('licence')
        if licence_value:
            try:
                licence = self.validate_licence(request.user, licence_value)
                queryset = self.filter_by_licence(queryset, licence.valeur)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        group_by = request.GET.get('group_by')
        if group_by:
            grouped_data = defaultdict(list)
            for music in queryset:
                key = getattr(music, group_by, 'Other')
                grouped_data[key].append(MusicSerializer(music).data)
            return Response(grouped_data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CreatePlaylistView(generics.CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistCreateSerializer
    permission_classes = [permissions.IsAuthenticated, ValidLicencePermission]



class GetSchoolPlaylistsView(LicenceValidationMixin, generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, ValidLicencePermission]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = MyPlaylistFilter
    ordering_fields = ['nom', 'classe__nom', 'niveau__nom']
    ordering = ['nom']

    @swagger_auto_schema(
        operation_summary="Retrieve user playlists",
        operation_description="Get playlists filtered by various attributes and ordered as specified.",
        manual_parameters=[
            openapi.Parameter('licence', openapi.IN_QUERY, description="Licence value to filter playlists",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search term for playlist names",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Field to order by", type=openapi.TYPE_STRING),
            openapi.Parameter('group_by', openapi.IN_QUERY, description="Field to group by", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        user = self.request.user
        licence_value = self.request.query_params.get('licence')

        if not licence_value:
            raise ValidationError("Licence value is required")

        # Validate the licence of the requesting user
        licence = self.validate_licence(user, licence_value)

        # Filter playlists created by users who have a licence with the same source as the provided licence
        playlists = Playlist.objects.filter(
            created_by__licences__source=licence.source,
            matiere=licence.source,
            classe=licence.classe,
            niveau=licence.niveau
        ).distinct()

        # Group by attribute (if needed)
        group_by = self.request.query_params.get('group_by')
        if group_by:
            playlists = playlists.values(group_by).annotate(count=models.Count(group_by))

        return playlists


class GetMyPlaylistsView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = MyPlaylistFilter
    ordering_fields = ['nom', 'classe', 'niveau']  # Specify fields to sort by
    ordering = ['nom']  # Default ordering

    @swagger_auto_schema(
        operation_summary="Retrieve user playlists",
        operation_description="Get playlists filtered by various attributes and ordered as specified.",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search term for playlist names", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Field to order by", type=openapi.TYPE_STRING),
            openapi.Parameter('group_by', openapi.IN_QUERY, description="Field to group by", type=openapi.TYPE_STRING),
        ]
    )
    def get_queryset(self):
        user = self.request.user

        # Filter playlists by the current user
        queryset = Playlist.objects.filter(
            created_by=user
        )

        # Group by attribute (if needed)
        group_by = self.request.query_params.get('group_by')
        if group_by:
            queryset = queryset.values(group_by).annotate(count=models.Count(group_by))

        return queryset


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing and editing playlists.
    """
    queryset = Playlist.objects.filter(is_public=True)
    serializer_class = PlaylistSerializer

    @swagger_auto_schema(
        operation_description="Get all playlists",
        responses={200: PlaylistSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AddToFavoritesView(generics.UpdateAPIView):
    serializer_class = FavoriCreateSerializer
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
            ),
            openapi.Parameter(
                'theme',
                openapi.IN_QUERY,
                description="Rechercher les musiques par thème",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'group_by',
                openapi.IN_QUERY,
                description="Grouper les musiques par un champ spécifique (ex: matiere, style_enreg)",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Trier les musiques par un champ spécifique (ex: date_created, -date_created)",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'error': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        musics = playlist.musics.all()

        # Filtrage simple
        theme = request.GET.get('theme')
        if theme:
            musics = musics.filter(theme__icontains=theme)

        # Tri
        ordering = request.GET.get('ordering')
        if ordering:
            musics = musics.order_by(ordering)

        # Regroupement
        group_by = request.GET.get('group_by')
        if group_by:
            grouped_data = defaultdict(list)
            for music in musics:
                key = getattr(music, group_by, 'Other')
                grouped_data[key].append(MusicSerializer(music).data)
            return Response(grouped_data)

        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)


class AddMusicToFavoriView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a music to the user's favori. If the favori does not exist, create one.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'music_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the music to add'),
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the favori'),
            }
        ),
        responses={200: 'Success', 404: 'Music not found'}
    )
    def post(self, request):
        user = request.user
        music_id = request.data.get('music_id')
        title = request.data.get('title', 'My Favori')

        # Get or create favori
        favori, created = Favori.objects.get_or_create(user=user, defaults={'title': title})

        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({'error': 'Music not found'}, status=404)

        favori.musics.add(music)
        favori.save()

        return Response({'success': 'Music added to favori'}, status=200)


class GetMyFavoriView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get the favori of the currently authenticated user.",
        responses={200: FavoriGetSerializer(many=False), 404: 'Favori not found'}
    )
    def get(self, request):
        user = request.user
        try:
            favori = Favori.objects.get(user=user)
        except Favori.DoesNotExist:
            return Response({'error': 'Favori not found'}, status=404)

        serializer = FavoriGetSerializer(favori)
        return Response(serializer.data)


class DeleteFavoriView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Delete the favori of the currently authenticated user.",
        responses={200: 'Success', 404: 'Favori not found'}
    )
    def delete(self, request):
        user = request.user
        try:
            favori = Favori.objects.get(user=user)
        except Favori.DoesNotExist:
            return Response({'error': 'Favori not found'}, status=404)

        favori.delete()
        return Response({'success': 'Favori deleted'}, status=200)


class RemoveMusicFromFavoriView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Remove a music from the user's favori",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'music_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the music to remove'),
            }
        ),
        responses={
            200: openapi.Response('Success', FavoriSerializer),
            400: 'Bad Request',
            404: 'Not Found',
        }
    )
    def delete(self, request):
        user = request.user
        music_id = request.data.get('music_id')

        if not music_id:
            return Response({'error': 'Music ID is required'}, status=400)

        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({'error': 'Music not found'}, status=404)

        try:
            favori = Favori.objects.get(user=user)
        except Favori.DoesNotExist:
            return Response({'error': 'Favori not found'}, status=404)

        if music in favori.musics.all():
            favori.musics.remove(music)
            favori.save()
            return Response({'success': 'Music removed from favori'}, status=200)
        else:
            return Response({'error': 'Music not in favori'}, status=400)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'music_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the music to add'),
    },
))
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_music_to_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, created_by=request.user)
    except Playlist.DoesNotExist:
        return Response({"detail": "Playlist not found or you don't have access to it."}, status=status.HTTP_404_NOT_FOUND)

    music_id = request.data.get('music_id')
    try:
        music = Music.objects.get(id=music_id)
    except Music.DoesNotExist:
        return Response({"detail": "Music not found."}, status=status.HTTP_404_NOT_FOUND)

    playlist.musics.add(music)
    playlist.save()
    return Response(PlaylistSerializer(playlist).data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'music_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the music to remove'),
    },
))
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def remove_music_from_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, created_by=request.user)
    except Playlist.DoesNotExist:
        return Response({"detail": "Playlist not found or you don't have access to it."}, status=status.HTTP_404_NOT_FOUND)

    music_id = request.data.get('music_id')
    try:
        music = Music.objects.get(id=music_id)
    except Music.DoesNotExist:
        return Response({"detail": "Music not found."}, status=status.HTTP_404_NOT_FOUND)

    playlist.musics.remove(music)
    playlist.save()
    return Response(PlaylistSerializer(playlist).data, status=status.HTTP_200_OK)
