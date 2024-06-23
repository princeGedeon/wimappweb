from django.utils import timezone
from rest_framework import permissions

class NoLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return not hasattr(request.user, 'licence') or request.user.licence is None


class ValidLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'licence') or request.user.licence is None:
            return False
        licence = request.user.licence
        return licence.is_active and licence.date_exp >= timezone.now().date()




class StudentLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'licence') or request.user.licence is None:
            return False
        licence = request.user.licence
        return licence.is_active and licence.date_exp >= timezone.now().date() and licence.type == 'etudiant'



class TeacherLicencePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'licence') or request.user.licence is None:
            return False
        licence = request.user.licence
        return licence.is_active and licence.date_exp >= timezone.now().date() and licence.type == 'enseignant'