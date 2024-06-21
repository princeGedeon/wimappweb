# urls.py

from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .views import MusicViewSet, PlaylistViewSet, FavoriViewSet

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
router.register(r'favoris', FavoriViewSet, basename='favori')

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
