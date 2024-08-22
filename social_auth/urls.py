from django.urls import path

from social_auth.views import GoogleSocialAuthView, FacebookSocialAuthView

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),

]