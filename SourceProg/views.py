from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Sum
from django.utils import timezone
from datetime import date
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.timezone import now
from decimal import Decimal


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
            check_limit_and_notify(request.user)
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

def check_limit_and_notify(user):
    this_month = now().replace(day=1)
    total = Expense.objects.filter(user=user, created_at__gte=this_month).aggregate(Sum('amount'))['amount__sum'] or 0
    try:
        limit = SpendingLimit.objects.get(user=user)
        if limit.monthly_limit > 0 and total > limit.monthly_limit:
            if not Notification.objects.filter(user=user, message__icontains="лимит", created_at__date=now().date()).exists():
                Notification.objects.create(user=user, message="Вы превысили лимит расходов на месяц.")
    except SpendingLimit.DoesNotExist:
        pass

@login_required
def categories_view(request):
    form = CategoryForm()
    categories = Category.objects.filter(created_by=request.user)
    return render(request, 'sourceprog/categories.html', {
        'form': form,
        'categories': categories
    })

@login_required
def add_category_view(request):
    if not request.user.is_vip:
        user_categories_count = Category.objects.filter(created_by=request.user).count()
        if user_categories_count >= 9:
            messages.warning(request, 'У вас лимит категорий (9)...')
            return redirect('SourceProg:categories')

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, 'Категория успешно добавлена!')
            return redirect('SourceProg:categories')
        else:
            messages.error(request, 'Ошибка при добавлении категории.')
            return redirect('SourceProg:categories')

    return redirect('SourceProg:categories')  


@login_required
def delete_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Удостоверимся, что пользователь является владельцем категории
    if category.created_by != request.user:
        return HttpResponseForbidden("У вас нет прав на удаление этой категории.")

    category.delete()
    messages.success(request, 'Категория успешно удалена!')
    return redirect('SourceProg:categories')

@login_required
def edit_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, created_by=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно обновлена!')
        else:
            messages.error(request, 'Ошибка при обновлении категории.')
        return redirect('SourceProg:categories')
    
    return redirect('SourceProg:categories') 

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

def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Расход успешно удалён!')
        return redirect('SourceProg:expense_history')

@login_required
def credits_view(request):
    credits = Credit.objects.filter(user=request.user)
    credit_data = []
    for credit in credits:
        paid_count = credit.payments.count()
        paid_sum = credit.monthly_payment * paid_count
        remaining = credit.amount - paid_sum
        last_payment = credit.payments.last()
        paid_this_month = last_payment and last_payment.payment_date.year == now().year and last_payment.payment_date.month == now().month

        credit_data.append({
            'credit': credit,
            'paid_count': paid_count,
            'paid_sum': paid_sum,
            'remaining': remaining,
            'paid_this_month': paid_this_month
        })

    form = CreditForm()
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.user = request.user
            credit.save()
            messages.success(request, 'Кредит успешно добавлен!')
            return redirect('SourceProg:credits')
        else:
            messages.error(request, 'Форма содержит ошибки.')

    return render(request, 'sourceprog/credits.html', {
        'credit_form': form,
        'credits_data': credit_data,
    })

@login_required
def pay_credit_view(request, credit_id):
    credit = get_object_or_404(Credit, id=credit_id, user=request.user)
    
    today = now().date()
    already_paid = credit.payments.filter(
        payment_date__year=today.year,
        payment_date__month=today.month
    ).exists()

    if already_paid:
        messages.info(request, 'Вы уже оплатили кредит в этом месяце.')
    else:
        CreditPayment.objects.create(credit=credit)
        messages.success(request, 'Оплата за этот месяц успешно зафиксирована.')

    return redirect('SourceProg:credits')

@login_required
def edit_credit_view(request, credit_id):
    credit = get_object_or_404(Credit, id=credit_id, user=request.user)

    if request.method == 'POST':
        form = CreditForm(request.POST, instance=credit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Кредит успешно обновлён.')
            return redirect('SourceProg:credits')
        else:
            messages.error(request, 'Ошибка в форме.')
    else:
        form = CreditForm(instance=credit)

    return render(request, 'sourceprog/edit_credit.html', {
        'form': form,
        'credit': credit
    })

@login_required
def delete_credit_view(request, credit_id):
    credit = get_object_or_404(Credit, id=credit_id, user=request.user)

    if request.method == 'POST':
        credit.delete()
        messages.success(request, 'Кредит успешно удалён.')
        return redirect('SourceProg:credits')

    return render(request, 'sourceprog/delete_credit_confirm.html', {
        'credit': credit
    })

@login_required
def debts_view(request):
    debts_i_owe = Debt.objects.filter(user=request.user, direction='i_owe', is_closed=False)
    debts_they_owe = Debt.objects.filter(user=request.user, direction='they_owe', is_closed=False)
    form = DebtForm()

    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user
            debt.save()
            messages.success(request, 'Долг добавлен.')
            return redirect('SourceProg:debts')

    return render(request, 'sourceprog/debts.html', {
        'form': form,
        'debts_i_owe': debts_i_owe,
        'debts_they_owe': debts_they_owe,
    })


@login_required
def close_debt_view(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id, user=request.user)
    debt.is_closed = True
    debt.closed_date = timezone.now()
    debt.save()
    messages.success(request, 'Долг закрыт.')
    return redirect('SourceProg:debts')


@login_required
def delete_debt_view(request, debt_id):
    debt = get_object_or_404(Debt, id=debt_id, user=request.user)
    debt.delete()
    messages.success(request, 'Долг удалён.')
    return redirect('SourceProg:debts')


@login_required
def debts_history_view(request):
    debts = Debt.objects.filter(user=request.user, is_closed=True).order_by('-closed_date')
    return render(request, 'sourceprog/debts_history.html', {'debts': debts})

@login_required
def analytics_view(request):
    user = request.user

    expenses = Expense.objects.filter(user=user)
    expenses_by_category = expenses.values('category__name', 'category__color').annotate(total=Sum('amount'))
    expenses_by_day = expenses.extra({'day': "date(created_at)"}).values('day').annotate(total=Sum('amount')).order_by('day')

    def convert_queryset(queryset, date_field=None):
        result = []
        for item in queryset:
            new_item = dict(item)
            if 'total' in new_item:
                new_item['total'] = float(new_item['total']) if new_item['total'] else 0
            if date_field and isinstance(new_item.get(date_field), date):
                new_item[date_field] = new_item[date_field].isoformat()
            result.append(new_item)
        return result

    return render(request, 'sourceprog/analytics.html', {
        'expenses_by_category_json': json.dumps(convert_queryset(expenses_by_category)),
        'expenses_by_day_json': json.dumps(convert_queryset(expenses_by_day, date_field='day')),
    })
