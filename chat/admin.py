from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp', 'is_read', 'is_deleted')
    list_filter = ('is_read', 'is_deleted')
    search_fields = ('sender__username', 'receiver__username', 'content')
    ordering = ('-timestamp',)
