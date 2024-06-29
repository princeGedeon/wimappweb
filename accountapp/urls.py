
from django.urls import include, path


from accountapp.views import UpdateUserInfoView, CustomUserCreateView, GoogleLoginAPIView, GenerateOTPAPIView, \
    VerifyOTPAPIView, AppleLogin

urlpatterns = [
    path(r'rauth/social', include('rest_framework_social_oauth2.urls')),
    path('auth/apple/', AppleLogin.as_view(), name='apple_login'),
    path('auth/social/', include('allauth.urls')),
    path(r'', include('djoser.urls')),
    path(r'', include('djoser.urls.jwt')),
    path('updateInfosUser/', UpdateUserInfoView.as_view(), name='update_user_info'),
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('auth/google/', GoogleLoginAPIView.as_view(), name='google-login'),
path('auth/generate-otp/', GenerateOTPAPIView.as_view(), name='generate-otp'),
    path('auth/verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),

]