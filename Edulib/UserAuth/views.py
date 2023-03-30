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


def login(request):
    if request.method == "POST":
        if request.POST["login_type"] == "normal":
            username = request.POST["username"]
            password = request.POST["password"]
            if username and password:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponse(f"<h1>You're logged in as {user.username}</h1>")
                else:
                    messages.info(request, "invalid credentials")
                    return redirect("login")
            else:
                messages.info(request, "please fill all the details")
                return redirect("login")
        elif request.POST["login_type"] == "google":
            username = request.user.username
            email = request.user.email
            role = request.user.role
            password = None
            user = auth.authenticate(username=username, password=password, email=email, role=role)
            if user is not None:
                # get role
                # redirect to dashboard according to role
                return HttpResponse(f"<h1>This is google user data, username: {request.user.username}, email: {request.user.email}, role: {request.user.role}</h1>")
            else:
                # give new form to ask role
                # save the data to database
                # redirect to form with new view
                return redirect("google_auth")


    return HttpResponseRedirect("/accounts/google/login/")


def register(request):
    if request.method == "POST":
        if request.POST["register_type"] == "normal":
            username = request.POST["username"]
            email = request.POST["email"]
            pass1 = request.POST["password1"]
            pass2 = request.POST["password2"]
            role = request.POST["role"]
            if username and pass1 and pass2 and email and role:
                if pass1 == pass2:
                    if User.objects.filter(email=email).exists():
                        messages.info(request, "Email Already Used")
                        return redirect("register")
                    elif User.objects.filter(username=username).exists():
                        messages.info(request, "Username already used")
                        return redirect("register")
                    else:
                        if role == "student":
                            student = Student.student.create_user(
                                username=username, email=email, password=pass1
                            )
                        elif role == "educator":
                            educator = Contributor.contributor.create_user(
                                username=username, email=email, password=pass1
                            )
                        elif role == "evaluator":
                            evaluator = Evaluator.evaluator.create_user(
                                username=username, email=email, password=pass1
                            )

                        return redirect('login')
                else:
                    messages.info(request, "Password didn't match")
                    return redirect("register")
            else:
                messages.info(request, "please fill all the required details")
                return redirect("register")
        else:
            return redirect("register")
    return render(request, "register.html")


def google_auth(request):
    if request.method == "POST":
        username = request.user.username
        email = request.user.email
        role = request.POST["role"]
        if role is not None:
            if role == "student":
                student = Student.student.create_user(
                    username=username, email=email, password=None
                )
            elif role == "educator":
                educator = Contributor.contributor.create_user(
                    username=username, email=email, password=None
                )
            elif role == "evaluator":
                evaluator = Evaluator.evaluator.create_user(
                    username=username, email=email, password=None
                )
        else:
            messages.info(request, "please select a role to continue")
            return redirect("google__auth")

    return render(request, "google_auth.html")


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


# @login_required(login_url="/login/")
# def dashboard(request):
#     return render(request, "dashboard.html")
