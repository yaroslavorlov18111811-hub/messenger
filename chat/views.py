from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Message

@login_required
def chat_page(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat.html', {'users': users})

@login_required
def get_messages(request, user_id):
    try:
        receiver = User.objects.get(id=user_id)
        messages = Message.objects.filter(
            sender__in=[request.user, receiver],
            receiver__in=[request.user, receiver]
        ).order_by('timestamp')
        
        messages_data = [{
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
                content=content
            )
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)