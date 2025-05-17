from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from django.http import JsonResponse


def home_view(request):
    return render(request, "main/home.html")

def about_platform(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('main:about')
    else:
        form = ReviewForm()

    reviews = Review.objects.all()
    return render(request, 'main/about.html', {'reviews': reviews, 'form': form})

@login_required
def account_view(request):
    return render(request, 'main/account.html', {'user': request.user})

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