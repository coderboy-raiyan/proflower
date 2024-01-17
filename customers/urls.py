from django.contrib import admin
from django.urls import path, include
from .views import UserSignUpView, UserSignInView, UserProfileView, user_logout, activate

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("signin/", UserSignInView.as_view(), name="signin"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('activate/<uid64>/<token>/', activate, name="activate"),
    path("logout/", user_logout, name="logout")
]
