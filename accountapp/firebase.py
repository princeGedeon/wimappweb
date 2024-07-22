# firebase.py
import os

import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

from core.settings import BASE_DIR
FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'workinmusic-30b37-firebase-adminsdk-h7ihz-8152566065.json')

# Remplacez le chemin par le chemin de votre fichier de clé de compte de service
cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIAL)
firebase_admin.initialize_app(cred)
