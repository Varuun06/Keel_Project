from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_superuser')  # ✅ Only show these columns

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
