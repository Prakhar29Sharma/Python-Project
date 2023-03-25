from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from . import views


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("accounts/", include("allauth.urls")),
    path("login", views.login, name="login"),
    path("logout", LogoutView.as_view()),
    path("register/", views.register, name="register")
]
