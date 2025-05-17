from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Category
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
