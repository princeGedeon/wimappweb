from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from core import settings
from licenceapp.models import Licence


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff_member', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    numTel = models.CharField(max_length=15, null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    profilImg=models.ImageField(upload_to="images_profil/", null=True, blank=True)
    typeCompte = models.CharField(max_length=10, choices=[('STANDARD', 'Standard'), ('PREMIUM', 'Premium')],
                                  default='STANDARD')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    licences = models.ManyToManyField(Licence, related_name='users', blank=True)
    fcm=models.CharField(max_length=10, null=True, blank=True)
    is_auto=models.BooleanField(default=False,null=True,blank=True)
    tuteur = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='tutored_users')
    secondary_email = models.EmailField(null=True, blank=True,help_text="Email du tuteur",default="",verbose_name="Email secondaire de l'utilisateur")
    objects = CustomUserManager()
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_staff_member

    def add_licence(self, licence):
        if licence.is_assignable():
            self.licences.add(licence)
            licence.user = self
            licence.save()
            return "Licence ajoutée avec succès."
        return "Licence non assignable."


class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300  # Valid for 5 minutes