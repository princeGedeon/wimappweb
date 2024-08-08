# API WimApp 

## Configuration du Projet Django 

Ce projet Django est configuré pour être exécuté avec Docker en production. Suivez les étapes ci-dessous pour configurer et exécuter le projet en local et en production.

## Prérequis

- Docker et Docker Compose installés sur votre machine.

## Structure du Projet

```
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── wimapp
│   ├── settings.py
│   ├── ...
└── ...
```

## Instructions d'Installation

### Environnement Local (sans Docker)

1. **Configurer la base de données:**
   - Dans `wimapp/settings.py`, commentez la configuration MySQL et décommentez la configuration SQLite.

   ```python
   # Pour l'environnement local
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }

   # Commenter la configuration MySQL
   # DATABASES = {
   #     'default': {
   #         'ENGINE': 'django.db.backends.mysql',
   #         'NAME': ...,
   #         'USER': ...,
   #         'PASSWORD': ...,
   #         'HOST': ...,
   #         'PORT': ...,
   #     }
   # }
   ```

2. **Installer les dépendances:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Exécuter les migrations et créer un super utilisateur:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Démarrer le serveur local:**

   ```bash
   python manage.py runserver
   ```

### Environnement de Production (avec Docker)

1. **Configurer la base de données:**
   - Dans `wimapp/settings.py`, commentez la configuration SQLite et décommentez la configuration MySQL.

   ```python
   # Pour l'environnement de production
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': ...,
           'USER': ...,,
           'PASSWORD': ...,
           'HOST': ...,
           'PORT': ...,
       }
   }

   # Commenter la configuration SQLite
   # DATABASES = {
   #     'default': {
   #         'ENGINE': 'django.db.backends.sqlite3',
   #         'NAME': BASE_DIR / 'db.sqlite3',
   #     }
   # }
   ```

2. **Construire et démarrer les conteneurs Docker:**

   ```bash
   docker-compose up --build
   ```

3. **Exécuter les migrations et créer un super utilisateur:**

   Ouvrez un nouveau terminal et exécutez:

   ```bash
   docker exec -it django_wim_app python manage.py migrate
   docker exec -it django_wim_app python manage.py createsuperuser
   ```

## Accès à l'Application

- **Application Django:** http://localhost:8081
- **phpMyAdmin:** http://localhost:7997 (Utilisez les identifiants de `docker-compose.yml`)

## Variables d'Environnement

Configurez les variables d'environnement dans `docker-compose.yml` selon les besoins de votre projet.

- `DEBUG`: Définissez à `1` pour le développement local, `0` pour la production.
- `SECRET_KEY`: Votre clé secrète Django.
- `ALLOWED_HOSTS`: Liste des hôtes autorisés.

## Commandes Utiles

- **Collecter les fichiers statiques:**

  ```bash
  docker exec -it django_wim_app python manage.py collectstatic
  ```

- **Exécuter les tests:**

  ```bash
  docker exec -it django_wim_app python manage.py test
  ```



By princeGedeon
