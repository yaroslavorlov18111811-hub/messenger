from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'users/register.html')
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('chat_page')
    
    return render(request, 'users/register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('chat_page')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'users/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')  # ← ИСПРАВЛЕНО!