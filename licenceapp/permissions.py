from django.utils import timezone
from rest_framework import permissions

from django.utils import timezone
from rest_framework import permissions

class NoLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.licences.exists()

class ValidLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        for licence in request.user.licences.all():
            if licence.is_active and licence.date_exp >= timezone.now().date():
                return True
        return False

class StudentLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        for licence in request.user.licences.all():
            if licence.is_active and licence.date_exp >= timezone.now().date() and licence.type == 'etudiant':
                return True
        return False

class TeacherLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        for licence in request.user.licences.all():
            if licence.is_active and licence.date_exp >= timezone.now().date() and licence.type == 'enseignant':
                return True
        return False
