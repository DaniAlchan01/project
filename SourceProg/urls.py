from django.urls import path
from . import views

app_name = 'SourceProg'

urlpatterns = [
    path('add-expense/', views.add_expense_view, name='add_expense'),
    path('add-category/', views.add_category_view, name='add_category'),
    path("categories/", views.categories_view, name="categories"),
    path('edit-category/<int:category_id>/', views.edit_category_view, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category_view, name='delete_category'),

    path('expense-history/', views.expense_history_view, name='expense_history'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense,name='delete_expense'),

    path('credits/', views.credits_view, name='credits'),
    path('credits/<int:credit_id>/pay/', views.pay_credit_view, name='pay_credit'),
    path('credits/<int:credit_id>/edit/', views.edit_credit_view, name='edit_credit'),
    path('credits/<int:credit_id>/delete/', views.delete_credit_view, name='delete_credit'),

    path('debts/', views.debts_view, name='debts'),
    path('debts/<int:debt_id>/close/', views.close_debt_view, name='close_debt'),
    path('debts/<int:debt_id>/delete/', views.delete_debt_view, name='delete_debt'),
    path('debts/history/', views.debts_history_view, name='debts_history'),

    path("analytics/", views.analytics_view, name="analytics"),
]
