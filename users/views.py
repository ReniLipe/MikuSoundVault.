from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Benvenuto, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Credenziali non valide.')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Hai effettuato il logout.')
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Le password non coincidono.')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username già in uso.')
        else:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                role='customer'
            )
            login(request, user)
            messages.success(request, 'Registrazione completata!')
            return redirect('home')
    return render(request, 'users/register.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        request.user.phone = request.POST.get('phone', '')
        request.user.address = request.POST.get('address', '')
        request.user.save()
        messages.success(request, 'Profilo aggiornato!')
    return render(request, 'users/profile.html')