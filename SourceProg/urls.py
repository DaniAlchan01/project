from django.urls import path
from .views import add_expense, expenses_list

app_name = "SourceProg"  # Пространство имен

urlpatterns = [
    path('add/', add_expense, name='add_expense'),
    path('list/', expenses_list, name='expenses_list'),
]
