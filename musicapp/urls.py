# urls.py

from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .views import MusicViewSet, PlaylistViewSet, CreatePlaylistView, GetMyPlaylistsView, \
    GetMyFavorisView, GetSchoolPlaylistsView, UserFavoritesView

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
    path('get-my-favoris/', GetMyFavorisView.as_view(), name='get_my_favoris'),

 path('my-favorites/', UserFavoritesView.as_view(), name='my-favorites'),

]
