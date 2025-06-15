from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from SourceProg.models import Expense, SpendingLimit, Notification
from .models import Review
from .forms import ReviewForm, LimitForm
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string



def home_view(request):
    return render(request, "main/home.html")

def settings_view(request):
    return render(request, "main/settings.html")

def about_platform(request):
    user_review = Review.objects.filter(user=request.user).first() if request.user.is_authenticated else None

    if request.method == "POST":
        if user_review:
            messages.warning(request, "Вы уже оставляли отзыв.")
            return redirect('main:about')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('main:about')
    else:
        form = ReviewForm() if not user_review else None

    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'main/about.html', {
        'form': form,
        'reviews': reviews,
        'total_count': reviews.count(),
        'user_review': user_review
    })

def load_more_reviews(request):
    page = int(request.GET.get("page", 1))
    reviews = Review.objects.all().order_by('-created_at')
    paginator = Paginator(reviews, 10)

    try:
        page_reviews = paginator.page(page)
    except:
        return JsonResponse({'success': False})

    html = render_to_string("main/_review_items.html", {'reviews': page_reviews})
    return JsonResponse({'success': True, 'html': html})

@login_required
def account_view(request):
    # Последние расходы
    latest_expenses = Expense.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Уведомления
    all_notifications_qs = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications = list(all_notifications_qs[:5])  # Срез — сразу в список
    unread_count = all_notifications_qs.filter(is_read=False).count()  # Без среза

    # Лимит
    limit, _ = SpendingLimit.objects.get_or_create(user=request.user)
    form = LimitForm(request.POST or None, instance=limit)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Лимит обновлён.")
        return redirect('main:account')

    return render(request, 'main/account.html', {
        'user': request.user,
        'latest_expenses': latest_expenses,
        'notifications': notifications,
        'unread_notifications': unread_count,
        'limit_form': form,
        'limit': limit,
    })


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user or request.user.is_superuser:
        review.delete()
    return redirect('main:about')  # ✅ предполагаем, что отзывы на странице "about"
@login_required
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    user = request.user

    if user in review.likes.all():
        review.likes.remove(user)
        liked = False  # Лайк был снят
    else:
        review.likes.add(user)
        liked = True  # Лайк был поставлен

    # Возвращаем JSON с количеством лайков и статусом (лайк/не лайк)
    return JsonResponse({
        'total_likes': review.total_likes(),
        'liked': liked
    })

@login_required
def notifications_partial(request):
    qs = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications = list(qs[:5])
    unread_count = qs.filter(is_read=False).count()

    return render(request, "main/_notifications_partial.html", {
        'notifications': notifications,
        'unread_notifications': unread_count
    })

@require_POST
@login_required
def mark_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})