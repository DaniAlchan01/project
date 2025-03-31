from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense
from .forms import ExpenseForm


@login_required
def add_expense(request):
    """Добавление нового расхода"""
    if request.user.is_vip:
        max_categories = 20  # VIP-пользователи
    else:
        max_categories = 9  # Обычные пользователи

    current_categories = Expense.objects.filter(user=request.user).values('category').distinct().count()

    if current_categories >= max_categories:
        messages.error(request, 'Вы достигли лимита категорий. Станьте VIP, чтобы добавить больше.')
        return redirect('SourceProg:expenses_list')  # Исправлено

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Расход успешно добавлен!')
            return redirect('SourceProg:expenses_list')  # Исправлено

    else:
        form = ExpenseForm()

    return render(request, 'SourceProg/add_expense.html', {'form': form})


@login_required
def expenses_list(request):
    """Отображение всех расходов пользователя"""
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'SourceProg/expenses_list.html', {'expenses': expenses})
