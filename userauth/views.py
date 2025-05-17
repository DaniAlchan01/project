from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .forms import (
    RegisterForm, LoginForm, UpdateProfileForm, ChangePasswordForm,
    PasswordResetByLoginForm, ChangeUsernameForm
)

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("/")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    return render(request, "userauth/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = LoginForm()
    return render(request, "userauth/login.html", {"form": form})

@login_required
def update_profile_view(request):
    user = request.user
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new_avatar = request.FILES.get("avatar")
            if new_avatar:
                user.avatar = new_avatar
            user.save()
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
            update_session_auth_hash(request, request.user)
            return redirect("main:account")
    else:
        form = ChangeUsernameForm(instance=request.user)
    return render(request, "userauth/change_username.html", {"form": form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        reason = request.POST.get('delete_reason', '')
        if reason:
            print(f"Причина удаления: {reason}")
        user.delete()
        messages.success(request, "Ваш аккаунт был удалён.")
        return redirect('userauth:login')
    return redirect('userauth:account')

@login_required
def vipping(request):
    return render(request, 'userauth/vipping.html')

@login_required
def process_vip_payment(request):
    user = request.user
    user.is_vip = True
    user.save()
    messages.success(request, "Поздравляем! Вы стали VIP-пользователем.")
    return redirect('main:account')

@login_required
def vip_payment_page(request):
    if request.method == 'POST':
        user = request.user
        user.is_vip = True
        user.save()
        messages.success(request, "Поздравляем! VIP-статус успешно оплачен и активирован.")
        return redirect("main:account")
    return render(request, 'userauth/payment.html')