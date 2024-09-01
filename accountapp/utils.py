import requests
from django.contrib.auth import authenticate

from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from accountapp.models import CustomUser
from core import settings


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token,requests.Request())
            if "accounts.google.com" in id_info['iss']:
                return id_info
        except Exception as e:
            return "token est invalid"
def login_user(email,password):
    user=authenticate(email=email,password=password)
    user_tokens=user.tokens()
    return {
        'access_token':str(user_tokens.get('access'))
    }
def register_social_user(provider,email,):
    user=CustomUser.objects.fiter(email=email)
    #####
    if user.exists():
        if provider==user[0].auth_provider:
            auth_user=login_user(email,"SOCIAL")
        else:
            raise AuthenticationFailed(
                detail=f"Please continue your login with {user[0].auth_provider} "
            )
    else:
        new_user={
            "email":email,
            "username":email.split('@')[0],
            "password":"social"
        }
        register_user=CustomUser.objects.create_user(**new_user)
        register_user.auth_provider=provider
        register_user.is_verified=True
        register_user.save()
        login_user(email=register_user.email,
                   password="social")