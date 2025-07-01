from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, CustomUser 

class CustomUserAdmin(UserAdmin):
    list_display = ("id", "first_name", "last_name", "phone_number", "email", "is_staff", "is_superuser")
    search_fields = ("first_name", "last_name", "phone_number", "email")
    list_filter = ("is_staff", "is_superuser", "is_active")
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "birth_date")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "phone_number", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

    ordering = ("id",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)

# jaff
# 12345678