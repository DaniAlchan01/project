from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    login_view, register_view, password_reset_by_login_view,
    password_reset_confirm_view, password_reset_complete_view,
    update_profile_view, change_password_view, change_username_view
)

app_name = "userauth"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", LogoutView.as_view(next_page="main:home"), name="logout"),

    # Сброс пароля по логину
    path("password_reset/", password_reset_by_login_view, name="password_reset_by_login"),
    path("password_reset/confirm/", password_reset_confirm_view, name="password_reset_confirm"),
    path("password_reset/done/", password_reset_complete_view, name="password_reset_complete"),

    # Изменение профиля, пароля и логина
    path("update_profile/", update_profile_view, name="update_profile"),
    path("change-password/", change_password_view, name="change_password"),
    path("change-username/", change_username_view, name="change_username"),
]
