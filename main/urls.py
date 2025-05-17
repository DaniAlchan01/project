from django.urls import path
from .views import home_view, about_platform, account_view, delete_review, like_review

app_name = "main"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_platform, name="about"),
    path("account/", account_view, name="account"),
    path("reviews/delete/<int:pk>/", delete_review, name="delete_review"),
    path("reviews/like/<int:pk>/", like_review, name="like_review"),
]
