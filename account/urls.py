
from django.urls import include, path


from account.views import UpdateUserInfoView, CustomUserCreateView, GoogleLoginAPIView

urlpatterns = [
    path(r'', include('djoser.urls')),
    path(r'', include('djoser.urls.jwt')),
    path('updateInfosUser/', UpdateUserInfoView.as_view(), name='update_user_info'),
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('auth/google/', GoogleLoginAPIView.as_view(), name='google-login'),

]