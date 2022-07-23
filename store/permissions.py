from rest_framework import permissions
from django.contrib.auth.models import AnonymousUser

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user,AnonymousUser):
            return False    
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)




class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user,AnonymousUser):
            return False    
        return bool(request.user and request.user.type=='C')

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if isinstance(request.user,AnonymousUser):
            return False    
        return bool( not request.user.type=='C' and not request.user.type=='V')

