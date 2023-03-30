from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = "UserAuth"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("accounts/", include("allauth.urls")),
    path("login", views.login, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("google_auth/", views.google_auth, name="google_auth"),
]
