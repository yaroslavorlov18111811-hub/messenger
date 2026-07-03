from django.db import connection

def ensure_column_exists():
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(chat_message)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'is_deleted' not in columns:
            cursor.execute("ALTER TABLE chat_message ADD COLUMN is_deleted BOOLEAN DEFAULT 0")

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)  # Мягкое удаление

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content[:20]}'

    class Meta:
        ordering = ['timestamp']