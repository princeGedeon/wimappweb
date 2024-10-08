"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.schemagen import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
   openapi.Info(
      title="WorkInMusic API",
      default_version='v2',
      description="Nouvelle version de l'API workinmusic",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
    generator_class=BothHttpAndHttpsSchemaGenerator,  # Here
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
path('quizz/', include('quizzapp.urls')),
path('licence/', include('licenceapp.urls')),
path('music/', include('musicapp.urls')),
    path('auths/', include('accountapp.urls')),
    path(r'social/', include('rest_framework_social_oauth2.urls',namespace='auth-api')),
path('social_auth/', include(('social_auth.urls', 'social_auth'),
                                 namespace="social_auth")),

    path("paiement/",include('paiementapp.urls')),
]
