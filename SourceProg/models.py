from django.db import models
from django.conf import settings


def user_expense_photo_path(instance, filename):
    """
    Генерирует путь для сохранения файлов:
    media/expenses/{username}/{category}/filename
    """
    return f"expenses/{instance.user.username}/{instance.category}/{filename}"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('medicine', 'Медицина'),
        ('food', 'Питание'),
        ('gifts', 'Подарки'),
        ('clothing', 'Одежда'),
        ('transport', 'Транспорт'),
        ('entertainment', 'Развлечения'),
        ('education', 'Образование'),
        ('bills', 'Коммунальные платежи'),
        ('other', 'Прочее'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    comment = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to=user_expense_photo_path, blank=True, null=True)  # Обновлено
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"
