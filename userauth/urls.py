from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "userauth"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", LogoutView.as_view(next_page="main:home"), name="logout"),

    # Password reset views
    path("password_reset/", views.password_reset_by_login_view, name="password_reset_by_login"),
    path("password_reset/confirm/", views.password_reset_confirm_view, name="password_reset_confirm"),
    path("password_reset/done/", views.password_reset_complete_view, name="password_reset_complete"),

    # Profile, password, and username change
    path("update_profile/", views.update_profile_view, name="update_profile"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("change-username/", views.change_username_view, name="change_username"),
    path('delete-account/', views.delete_account, name='delete_account'),

    # VIP pages
    path('vipping/', views.vipping, name='vipping'),
    path('vip/pay/', views.vip_payment_page, name='vip_payment_page'),
    path('vip/process/', views.process_vip_payment, name='process_vip_payment'),
]
