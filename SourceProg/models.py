from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

def user_expense_photo_path(instance, filename):
    return f'expense_photos/{instance.user.username}/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to=user_expense_photo_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} — {self.amount} ({self.category})'
