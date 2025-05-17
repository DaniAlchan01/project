from django.db import models
from django.conf import settings  # Импортируем настройки
from django.contrib.auth import get_user_model  # Импортируем функцию get_user_model

User = get_user_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_reviews", blank=True)

    def total_likes(self):
        return self.likes.count()
