from django.urls import path
from .views import home_view, about_view, account_view, add_expense_view

app_name = "main"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("account/", account_view, name="account"),
    path("add-expense/", add_expense_view, name="add_expense"),
]
