from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User
from django.utils.translation import gettext_lazy as _

class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", 'full_name', 'country', 'National_id',"bio", 
                  'title', 'experience_level')}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
    
        
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2","National_id"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


    

admin.site.register(User, UserAdmin)

