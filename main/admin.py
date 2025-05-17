from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Review
from userauth.models import CustomUser   # Убедись, что путь к CustomUser верный (если он в том же приложении)

# --- Админка для отзывов ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_text', 'rating', 'created_at', 'total_likes_count')
    list_filter = ('created_at', 'rating')
    search_fields = ('user__email', 'text')
    readonly_fields = ('created_at',)

    def short_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    short_text.short_description = 'Текст отзыва'

    def total_likes_count(self, obj):
        return obj.total_likes()
    total_likes_count.short_description = 'Лайков'

    def has_delete_permission(self, request, obj=None):
        return True  # Удаление разрешено


# --- Админка для пользователей ---
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_staff", "is_vip", "date_joined", "avatar_preview")
    list_filter = ("is_staff", "is_superuser", "is_vip", "is_active", "groups")
    search_fields = ("username", "email")
    ordering = ("date_joined",)
    readonly_fields = ("avatar_preview",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Личная информация", {"fields": ("first_name", "last_name", "avatar", "avatar_preview")}),
        ("Статус", {"fields": ("is_active", "is_staff", "is_superuser", "is_vip")}),
        ("Права доступа", {"fields": ("groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_vip", "avatar"),
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar and obj.avatar.url:
            return f'<img src="{obj.avatar.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;">'
        return "-"
    avatar_preview.allow_tags = True
    avatar_preview.short_description = "Превью аватара"
