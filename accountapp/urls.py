
from django.urls import include, path


from accountapp.views import UpdateUserInfoView, CustomUserCreateView, GoogleLoginAPIView, GenerateOTPAPIView, \
    VerifyOTPAPIView, AppleLogin, AssignTuteurView, ProfileImageUpdateView, CustomLoginView

urlpatterns = [
path('assign-tuteur/', AssignTuteurView.as_view(), name='assign_tuteur'),
    path('api/auth/apple/', AppleLogin.as_view(), name='apple_login'),
    path(r'', include('djoser.urls')),
    path(r'', include('djoser.urls.jwt')),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('updateInfosUser/', UpdateUserInfoView.as_view(), name='update_user_info'),
    path('register/', CustomUserCreateView.as_view(), name='register'),
    path('auth/google/', GoogleLoginAPIView.as_view(), name='google-login'),
path('auth/generate-otp/', GenerateOTPAPIView.as_view(), name='generate-otp'),
    path('auth/verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('update-profile-image/', ProfileImageUpdateView.as_view(), name='update-profile-image'),

]