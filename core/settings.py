"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import environ
# settings.py
import os
import firebase_admin
from firebase_admin import credentials
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))




#FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'workinmusic-30b37-firebase-adminsdk-h7ihz-8152566065.json')

#cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIAL)
#firebase_admin.initialize_app(cred)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pd7(cbqees77gvuo1bl^mdpbiiowe4g*xa2v_e$breh93q=xq_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["app.workinmusic.fr","*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    "corsheaders",
    'rest_framework',

    'social_django',


    'import_export',
'djoser',

    "rest_framework_simplejwt.token_blacklist",
    'rest_framework_simplejwt',
    "rest_framework.authtoken",
    'drf_yasg',



    #----
    "accountapp",
    "licenceapp",
    "musicapp",
    "quizzapp"
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "social_django.middleware.SocialAuthExceptionMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
       # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

WSGI_APPLICATION = 'core.wsgi.application'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('NAME'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
        'HOST': 'db', # Change to your MySQL host if it's not local
        'PORT': config("PORT"),
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_bin',
        'OPTIONS': {
            'use_unicode': True,
            'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        },
        # Change to your MySQL port if needed
    }
}

"""

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/


LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_ROOT =os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS=[ os.path.join(BASE_DIR, 'statics')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
"https://app.workinmusic.fr",
    "http://app.workinmusic.fr",
"https://www.app.workinmusic.fr",
    "http://www.app.workinmusic.fr",
"http://localhost:8001",
"http://127.0.0.1:9000",
"http://localhost:8000",
"http://127.0.0.1:8000",
"http://localhost:8080",
"http://localhost:8080",
"http://localhost:8081",

]
CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'accountapp.CustomUser'
CSRF_TRUSTED_ORIGINS = ['https://*.workinmusic.fr','https://*.127.0.0.1',"https://app.workinmusic.fr","http://app.workinmusic.fr"]

#Djsoer
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ["http://localhost:3000","https://workinmusic.fr"],
    "SERIALIZERS": {
        "user_create": "accountapp.serializers.CustomUserCreateSerializer",
        "user": "accountapp.serializers.CustomUserUpdateSerializer",
        "current_user": "accountapp.serializers.CustomUserUpdateSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}
# Auth
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    'rest_framework_social_oauth2.backends.DjangoOAuth2',



]
#Google
"""SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.apple.AppleIdAuth',
)"""

# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "guedjegedeon03@gmail.com"
#'contacts@workinmusic.fr'ff
EMAIL_HOST_PASSWORD ="odtoljgqbzjdhcnh"
EMAIL_USE_TLS = True  # Utilisez TLS pour sécuriser la connexion
#-------------------

SOCIAL_AUTH_APPLE_ID_CLIENT= 'com.workinmusic.wimusic'
SOCIAL_AUTH_APPLE_ID_TEAM= '2F99S874FL'               # Your Team ID, ie K2232113
SOCIAL_AUTH_APPLE_ID_KEY= '24T3K2WRWN'                # Your Key ID, ie Y2P99J3N81K
SOCIAL_AUTH_APPLE_ID_SECRET= """
-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgmyF9+Du/EojT0Qpr
SnPOCeb8TZu13NqB0xjvWLwYODGgCgYIKoZIzj0DAQehRANCAAQ/0HDCJPQW/fDV
RpU6xfkc30bDtL6VVDL9PxKcUhMr07Z7WKiTwx5Qf1h5FHbeHL9MKL72W652DugD
pIk4fLQk
-----END PRIVATE KEY-----"""
SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True


SOCIALACCOUNT_PROVIDERS = {
    'apple': {
        'APP': {
            'client_id': SOCIAL_AUTH_APPLE_ID_CLIENT,
            'secret': {
                'key': SOCIAL_AUTH_APPLE_ID_KEY,
                'team_id': SOCIAL_AUTH_APPLE_ID_TEAM,
                'private_key': SOCIAL_AUTH_APPLE_ID_SECRET,
            },
        }
    }
}
#------------