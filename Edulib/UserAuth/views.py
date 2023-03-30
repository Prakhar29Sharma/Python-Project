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
    return redirect("UserAuth:index")


def login(request):
    if request.method == "POST":
        if request.POST["login_type"] == "normal":
            username = request.POST["username"]
            password = request.POST["password"]
            if username and password:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    if user.role.lower() == 'contributor':
                        return redirect("Contributor:dashboard")
                    else:
                        return HttpResponse('<h1>404 PAge Not Found, Only Contributors part has been implemented!</h1>')
                else:
                    messages.info(request, "invalid credentials")
                    return redirect("UserAuth:login")
            else:
                messages.info(request, "please fill all the details")
                return redirect("UserAuth:login")
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
                return redirect("UserAuth:google_auth")

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
                        return redirect("UserAuth:register")
                    elif User.objects.filter(username=username).exists():
                        messages.info(request, "Username already used")
                        return redirect("UserAuth:register")
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

                        return redirect('UserAuth:login')
                else:
                    messages.info(request, "Password didn't match")
                    return redirect("UserAuth:register")
            else:
                messages.info(request, "please fill all the required details")
                return redirect("UserAuth:register")
        else:
            return redirect("UserAuth:register")
    return render(request, "UserAuth/register.html")


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
            return redirect("UserAuth:login")
        else:
            messages.info(request, "please select a role to continue")
            return redirect("UserAuth:google_auth")

    return render(request, "UserAuth/google_auth.html")


def logout_view(request):
    logout(request)
    return redirect('UserAuth:index')

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
#     return render(request, "index.html")
