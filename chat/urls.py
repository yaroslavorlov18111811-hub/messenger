from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('get_messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('moderator/', views.moderator_panel, name='moderator_panel'),
    path('moderator/toggle_block/<int:user_id>/', views.toggle_block, name='toggle_block'),
    path('moderator/delete_message/<int:message_id>/', views.moderator_delete_message, name='moderator_delete_message'),
]