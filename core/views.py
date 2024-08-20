
from social_core.backends.facebook import FacebookOAuth2


class CustomFacebookOAuth2(FacebookOAuth2):
    REDIRECT_STATE = False