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

class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.name} ({self.amount})"
    

class CreditPayment(models.Model):
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.credit.name} оплачено {self.payment_date}'

class Debt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    direction = models.CharField(  
        max_length=10,
        choices=[('i_owe', 'Я должен'), ('they_owe', 'Мне должны')]
    , default='they_owe')
    name = models.CharField("Имя", max_length=255, default=" ")  
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    taken_date = models.DateField("Дата взятия")
    due_date = models.DateField("Дата возврата")
    is_closed = models.BooleanField("Закрыт?", default=False)
    closed_date = models.DateField("Дата закрытия", null=True, blank=True)

    def __str__(self):
        return f"{self.name} — {self.amount}₸"

class SpendingLimit(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monthly_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.monthly_limit}₸"
    
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username}: {self.message[:40]}"
