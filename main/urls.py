from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_platform, name="about"),
    path("account/", account_view, name="account"),
    path("settings/", settings_view, name="settings"),
    path("reviews/delete/<int:pk>/", delete_review, name="delete_review"),
    path("reviews/load/", load_more_reviews, name="load_more_reviews"),
    path("reviews/like/<int:pk>/", like_review, name="like_review"),
    path("notifications/partial/", notifications_partial, name="notifications_partial"),
    path('notifications/mark-read/', mark_notifications_read, name='mark_notifications_read'),

]
