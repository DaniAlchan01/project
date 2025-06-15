from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Category, Expense, SpendingLimit, Notification
from django.db.models import Sum
from django.utils.timezone import now

from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def create_default_categories_for_user(sender, instance, created, **kwargs):
    if created:
        if not instance.is_vip:
            default_categories = [
                {'name': 'Еда', 'color': '#FF5733'},
                {'name': 'Транспорт', 'color': '#33FF57'},
                {'name': 'Развлечения', 'color': '#3357FF'},
                {'name': 'Здоровье', 'color': '#FF33A6'},
                {'name': 'Образование', 'color': '#FFFF33'},
                {'name': 'Жилье', 'color': '#8B33FF'},
                {'name': 'Одежда', 'color': '#33FFDC'},
                {'name': 'Подарки', 'color': '#FF8C33'},
                {'name': 'Прочее', 'color': '#8C33FF'}
            ]
            for cat in default_categories:
                if not Category.objects.filter(name=cat['name'], created_by=instance).exists():
                    Category.objects.create(
                        name=cat['name'],
                        color=cat['color'],
                        is_default=True,
                        created_by=instance
                    )

        else:
            # Если VIP, то возможности по созданию категорий не ограничены
            pass

@receiver(post_save, sender=Expense)
def check_spending_limit(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    this_month = now().replace(day=1)

    total_spent = Expense.objects.filter(
        user=user,
        created_at__gte=this_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    try:
        limit = SpendingLimit.objects.get(user=user)

        if limit.monthly_limit > 0 and total_spent > limit.monthly_limit:
            exceeded = total_spent - limit.monthly_limit

            already_notified = Notification.objects.filter(
                user=user,
                message__icontains="лимит",
                created_at__date=now().date()
            ).exists()

            if not already_notified:
                Notification.objects.create(
                    user=user,
                    message=f"Вы превысили лимит расходов на месяц: {total_spent:.2f} ₸ / {limit.monthly_limit:.2f} ₸. "
                            f"Превышение на {exceeded:.2f} ₸."
                )

    except SpendingLimit.DoesNotExist:
        pass