from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from .forms import ExpenseForm, CategoryForm, ExpenseEditForm
from django.db.models import Q
from django.core.paginator import Paginator

@login_required
def add_expense_view(request):
    categories = Category.objects.filter(created_by=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        form.fields['category'].queryset = categories
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Расход успешно добавлен!')
            return redirect('SourceProg:add_expense')
        else:
            messages.error(request, 'Ошибка при добавлении расхода. Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ExpenseForm()
        form.fields['category'].queryset = categories

    return render(request, "sourceprog/add_expense.html", {
        'form': form,
        'categories': categories,
        'user': request.user
    })

@login_required
def add_category_view(request):
    if not request.user.is_vip:
        # Проверяем, сколько категорий у пользователя
        user_categories_count = Category.objects.filter(created_by=request.user).count()

        if user_categories_count >= 9:
            # Если категория больше 9, то показываем сообщение с двумя кнопками
            messages.warning(request, 'У вас лимит категорий (9). Для добавления больше категорий, пожалуйста, купите приложение за 3400 тг.')
            return render(request, 'sourceprog/add_expense.html', {
                'form': None,  # Мы не будем отображать форму для добавления новой категории
                'user_has_limit': True,
                'categories': Category.objects.filter(created_by=request.user),
            })

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('SourceProg:add_expense')
        else:
            messages.error(request, 'Ошибка при добавлении категории. Пожалуйста, исправьте ошибки в форме.')
            return render(request, 'sourceprog/add_expense.html', {
                'form': form,
                'categories': Category.objects.filter(created_by=request.user),
            })
    else:
        form = CategoryForm()

    return render(request, 'sourceprog/add_expense.html', {
        'form': form,
        'categories': Category.objects.filter(created_by=request.user)
    })

@login_required
def delete_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Удостоверимся, что пользователь является владельцем категории
    if category.created_by != request.user:
        return HttpResponseForbidden("У вас нет прав на удаление этой категории.")

    category.delete()
    messages.success(request, 'Категория успешно удалена!')
    return redirect('SourceProg:add_expense')

@login_required
def edit_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, created_by=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена!')
            return redirect('SourceProg:add_expense')
        else:
            messages.error(request, 'Ошибка при обновлении категории. Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'sourceprog/add_category.html', {
        'form': form,
        'categories': Category.objects.filter(created_by=request.user),
        'editing_category': category,
    })

@login_required
def expense_history_view(request):
    # Получаем все категории для фильтрации
    categories = Category.objects.filter(created_by=request.user)

    # Извлекаем параметры фильтрации из GET-запроса
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Начинаем строить фильтрацию
    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')

    # Применяем фильтры
    if selected_category:
        expenses = expenses.filter(category_id=selected_category)
    if search_query:
        expenses = expenses.filter(comment__icontains=search_query)
    if start_date:
        expenses = expenses.filter(created_at__gte=start_date)
    if end_date:
        expenses = expenses.filter(created_at__lte=end_date)

    # Пагинация
    paginator = Paginator(expenses, 10)  # Показываем по 10 записей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sourceprog/expense_history.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
    })

def expense_chart_view(request):
    return render(request, 'sourceprog/expense_chart.html')

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseEditForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расход успешно обновлен!')
            return redirect('SourceProg:expense_history')  # Перенаправляем на страницу истории расходов
        else:
            messages.error(request, 'Ошибка при обновлении расхода. Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ExpenseEditForm(instance=expense)

    return render(request, 'sourceprog/edit_expense.html', {'form': form})
