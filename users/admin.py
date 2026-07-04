from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_moderator', 'is_blocked', 'is_staff')
    list_filter = ('is_moderator', 'is_blocked', 'is_staff')
    search_fields = ('username', 'email')
    fields = ('username', 'email', 'password', 'is_moderator', 'is_blocked', 'is_staff', 'is_active', 'is_superuser')