from django.urls import path
from . import views

app_name = 'SourceProg'

urlpatterns = [
    path('add-expense/', views.add_expense_view, name='add_expense'),
    path('add-category/', views.add_category_view, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category_view, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category_view, name='delete_category'),

    path('expense-history/', views.expense_history_view, name='expense_history'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense,name='delete_expense'),

    path('credits/', views.credits_view, name='credits'),
    path('debts/', views.debts_view, name='debts'),

    path('expense-chart/', views.expense_chart_view, name='expense_chart'),
]
