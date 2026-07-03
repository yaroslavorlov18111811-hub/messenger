from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Message

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

        # Помечаем все сообщения от этого пользователя как прочитанные
        Message.objects.filter(
            sender=receiver,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

        # Показываем только НЕ УДАЛЁННЫЕ сообщения
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
        # Проверяем, что это сообщение принадлежит текущему пользователю
        if message.sender != request.user:
            return JsonResponse({'error': 'Нельзя удалить чужое сообщение'}, status=403)
        # Мягкое удаление — просто скрываем
        message.is_deleted = True
        message.save()
        return JsonResponse({'status': 'ok'})
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Сообщение не найдено'}, status=404)