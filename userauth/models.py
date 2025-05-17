import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def user_directory_path(instance, filename):
    return f"profile_pics/{instance.username}/{filename}"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_vip = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to=user_directory_path, default="profile_pics/default_avatar.jpg")
    groups = models.ManyToManyField("auth.Group", related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custom_user_permissions", blank=True)

    def save(self, *args, **kwargs):
        user_folder = os.path.join(settings.MEDIA_ROOT, "profile_pics", self.username)
        os.makedirs(user_folder, exist_ok=True)

        try:
            old_avatar = CustomUser.objects.get(id=self.id).avatar
            if (
                old_avatar
                and old_avatar.name != "profile_pics/default_avatar.jpg"
                and old_avatar.name != self.avatar.name
            ):
                old_avatar_path = os.path.join(settings.MEDIA_ROOT, old_avatar.name)
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)
        except CustomUser.DoesNotExist:
            pass  # Пользователь создаётся впервые, старого аватара нет

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"
