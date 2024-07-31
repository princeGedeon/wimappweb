# urls.py

from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .views import MusicViewSet, PlaylistViewSet, CreatePlaylistView, GetMyPlaylistsView, \
    GetSchoolPlaylistsView, UserFavoritesView, PlaylistMusicsAPIView, GetMyFavoriView, \
    DeleteFavoriView, AddMusicToFavoriView, RemoveMusicFromFavoriView, add_music_to_playlist, remove_music_from_playlist

schema_view = get_schema_view(
   openapi.Info(
      title="Music API",
      default_version='v1',
      description="API for managing music and playlists",
   ),
   public=True,
   permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'musics', MusicViewSet, basename='music')
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('', include(router.urls)),
    path('create-playlist/', CreatePlaylistView.as_view(), name='create_playlist'),
    path('get-school-playlists/', GetSchoolPlaylistsView.as_view(), name='get_school_playlists'),
    path('get-my-playlists/', GetMyPlaylistsView.as_view(), name='get_my_playlists'),
    path('playlists/<int:pk>/musics/', PlaylistMusicsAPIView.as_view(), name='playlist-musics'),

    path('my-favorites/', UserFavoritesView.as_view(), name='my-favorites'),
path('add-music-to-favori/', AddMusicToFavoriView.as_view(), name='add-music-to-favori'),
    path('get-my-favori/', GetMyFavoriView.as_view(), name='get-my-favori'),
    path('delete-favori/', DeleteFavoriView.as_view(), name='delete-favori'),
    path('remove-music-from-favori/', RemoveMusicFromFavoriView.as_view(), name='remove-music-from-favori'),
    path('playlist/<int:playlist_id>/add_music/', add_music_to_playlist, name='add_music_to_playlist'),
    path('playlist/<int:playlist_id>/remove_music/', remove_music_from_playlist, name='remove_music_from_playlist'),

]
