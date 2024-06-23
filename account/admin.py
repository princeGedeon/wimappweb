from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from licenceapp.models import Licence

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('fullname', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilUrl', 'typeCompte')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_staff_member', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Licences'), {'fields': ('licences',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'fullname', 'age', 'genre', 'numTel', 'pays', 'ville', 'profilUrl', 'typeCompte', 'is_active', 'is_admin', 'is_staff_member', 'is_superuser')}
        ),
    )
    list_display = ('email', 'fullname', 'is_admin', 'is_active', 'is_staff_member', 'is_superuser')
    search_fields = ('email', 'fullname')
    ordering = ('email',)

    # Removing filter_horizontal and list_filter definitions
    filter_horizontal = ()
    list_filter = ('is_active', 'is_admin', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)
