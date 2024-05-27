from django.shortcuts import render

# Create your views here.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView

import sys
sys.path.append('D:\\Python\\Music-Analyzer\\source\\Parsing')
from DBHelper import DBHelper

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт создан для {user.username}!')
            db = DBHelper(database="music", user="postgres", password="1111", host='localhost')
            db.exec(f"insert into users.users values ('{user.username}')")
            return redirect('home')  # Замените 'home' на нужное вам представление
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'register/login.html'

