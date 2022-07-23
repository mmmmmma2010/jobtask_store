from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin,GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import AnonymousUser,Group
from.models import  User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'email','first_name','last_name','type'),
            },
        ),
    )
    def has_module_permission(self, request) -> bool:      
        if not   isinstance(request.user,AnonymousUser) :
            if request.user.type=='V':
                return False
            return True

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    def has_module_permission(self, request) -> bool:      
        if not   isinstance(request.user,AnonymousUser) :
            if request.user.type=='V':
                return False
            return True
