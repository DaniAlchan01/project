from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_view(request):
    return render(request, "main/home.html")

def about_view(request):
    return render(request, "main/about.html")

@login_required
def account_view(request):
    return render(request, 'main/account.html', {'user': request.user})

@login_required
def add_expense_view(request):
    return render(request, "main/add_expense.html")