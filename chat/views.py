from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import Message

User = get_user_model()

@login_required
def chat_page(request):
    users = User.objects.exclude(id=request.user.id)
    users_with_unread = []
    for user in users:
        unread_count = Message.objects.filter(
            sender=user,
            receiver=request.user,
            is_read=False,
            is_deleted=False
        ).count()
        users_with_unread.append({
            'user': user,
            'unread': unread_count
        })
    return render(request, 'chat/chat.html', {'users_with_unread': users_with_unread})

@login_required
def get_messages(request, user_id):
    try:
        receiver = User.objects.get(id=user_id)
        Message.objects.filter(
            sender=receiver,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

        messages = Message.objects.filter(
            sender__in=[request.user, receiver],
            receiver__in=[request.user, receiver],
            is_deleted=False
        ).order_by('timestamp')

        messages_data = [{
            'id': msg.id,
            'sender': msg.sender.id,
            'content': msg.content,
            'timestamp': msg.timestamp.strftime('%H:%M'),
        } for msg in messages]

        return JsonResponse(messages_data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')

        try:
            receiver = User.objects.get(id=receiver_id)
            message = Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                is_read=False
            )
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        if message.sender != request.user:
            return JsonResponse({'error': 'Нельзя удалить чужое сообщение'}, status=403)
        message.is_deleted = True
        message.save()
        return JsonResponse({'status': 'ok'})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Сообщение не найдено'}, status=404)

@login_required
def moderator_panel(request):
    if not request.user.is_moderator:
        return redirect('chat_page')
    
    users = User.objects.all()
    messages_list = Message.objects.all().order_by('-timestamp')[:50]
    
    return render(request, 'chat/moderator_panel.html', {
        'users': users,
        'messages': messages_list,
        'total_users': users.count(),
        'total_messages': Message.objects.count(),
    })

@login_required
def toggle_block(request, user_id):
    if not request.user.is_moderator:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        user = User.objects.get(id=user_id)
        data = json.loads(request.body)
        user.is_blocked = data.get('block', False)
        user.save()
        return JsonResponse({'status': 'ok'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@login_required
def moderator_delete_message(request, message_id):
    if not request.user.is_moderator:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        message = Message.objects.get(id=message_id)
        message.is_deleted = True
        message.save()
        return JsonResponse({'status': 'ok'})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)