from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import render
from django.contrib import messages
from .forms import (
    RegisterForm, LoginForm, UpdateProfileForm, ChangePasswordForm,
    PasswordResetByLoginForm, ChangeUsernameForm
)
import os

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "userauth/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm()
    return render(request, "userauth/login.html", {"form": form})


@login_required
def update_profile_view(request):
    user = request.user  # Текущий пользователь

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            new_avatar = request.FILES.get("avatar")

            if new_avatar:
                # 📌 Генерируем путь и сохраняем аватар в папку пользователя
                user.avatar = new_avatar

            user.save()  # ✅ Теперь сохранит и обновит путь в БД
            messages.success(request, "Профиль успешно обновлён!")
            return redirect("main:account")

    else:
        form = UpdateProfileForm(instance=user)

    return render(request, "userauth/update_profile.html", {"form": form})

@login_required
def change_password_view(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("main:account")
    else:
        form = ChangePasswordForm(user=request.user)
    return render(request, "userauth/change_password.html", {"form": form})

def password_reset_by_login_view(request):
    if request.method == "POST":
        form = PasswordResetByLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            user = User.objects.filter(username=username).first()

            if user is None:
                form.add_error("username", "Пользователь с таким логином не найден.")
                return render(request, "userauth/password_reset_by_login.html", {"form": form})

            request.session["reset_user_id"] = user.id
            return redirect("userauth:password_reset_confirm")
    else:
        form = PasswordResetByLoginForm()

    return render(request, "userauth/password_reset_by_login.html", {"form": form})

def password_reset_confirm_view(request):
    user_id = request.session.get('reset_user_id')
    user = User.objects.filter(id=user_id).first()
    if not user:
        return redirect("userauth:password_reset_by_login")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['reset_user_id']
            return redirect("userauth:password_reset_complete")
    else:
        form = SetPasswordForm(user)
    return render(request, "userauth/password_reset_confirm.html", {"form": form})

def password_reset_complete_view(request):
    return render(request, "userauth/password_reset_complete.html")

@login_required
def change_username_view(request):
    if request.method == "POST":
        form = ChangeUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Чтобы не разлогинивало после смены
            return redirect("main:account")  # Перенаправление в личный кабинет
    else:
        form = ChangeUsernameForm(instance=request.user)

    return render(request, "userauth/change_username.html", {"form": form})
