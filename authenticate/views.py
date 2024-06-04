import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, ChangePasswordForm
from django.contrib.sessions.models import Session
from django_ratelimit.decorators import ratelimit


@ratelimit(key='ip', rate='100/h')
def home(request):
    if request.user.is_authenticated:
        return render(request, 'authenticate/home.html')
    else:
        return redirect('login')


@ratelimit(key='ip', rate='100/h')
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['username'] = username
            request.session.save()
            login(request, user)

            messages.success(request, 'You have been logged in successfully')
            return redirect('home')
        else:
            messages.warning(request, "Username or Password is incorrect !!")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html')


@ratelimit(key='ip', rate='100/h')
def logout_user(request):
    Session.objects.filter(session_key=request.session.session_key).delete()
    logout(request)

    messages.success(request, "Logged out successfully")
    return redirect('home')


@ratelimit(key='ip', rate='100/h')
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            request.session['username'] = username

            request.session.save()
            login(request, user)

            return redirect('home')
        else:
            form = SignUpForm(request.POST)
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'authenticate/register.html', context)


@ratelimit(key='ip', rate='100/h')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password Changed Successfully")
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, 'authenticate/change_password.html', context)
