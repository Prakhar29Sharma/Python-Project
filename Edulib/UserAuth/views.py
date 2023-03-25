from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Student, Evaluator, Contributor
from .models import User
from django.views.generic import ListView, DetailView, CreateView

User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("/")


def register(request):
    return render(request, "register.html")


def login(request):
    return HttpResponseRedirect("/accounts/google/login/")

# def login(request):
#     if request.method == "POST":
#         if request.POST["login_type"] == "normal":
#             username = request.POST["username"]
#             password = request.POST["password"]
#             if username and password:
#                 user = auth.authenticate(username=username, password=password)
#                 if user is not None:
#                     auth.login(request, user)
#                     return redirect("dashboard")
#                 else:
#                     messages.info(request, "invalid credentials")
#                     return redirect("login")
#             else:
#                 messages.info(request, "please fill all the details")
#                 return redirect("login")
#         else:
#             return redirect("/")
#     return HttpResponseRedirect("/")
