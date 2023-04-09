import json

import requests
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CreateContentForm
from .models import ContributorProfile
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


# class DashboardView(View):
#     def get(self, request):
#         return render(request, "Contributor/index.html")

class DashboardView(TemplateView):
    template_name = "Contributor/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateCourseView(View):

    template_name = "Contributor/create_course.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        subject = request.POST["subject"]
        unit = request.POST["unit"]
        post_data = dict(request.POST)
        json_data = json.dumps(post_data)
        return redirect(reverse('Contributor:create_content', args=(subject, unit)))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateContentView(View):
    template_name = "Contributor/create_content.html"
    form = CreateContentForm()

    def get(self, request, *args, **kwargs):
        subject = self.kwargs['subject']
        unit = self.kwargs['unit']
        context = {
            "subject": subject,
            "unit": unit,
            "form": self.form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post_data = dict(request.POST)
        print(post_data)
        return HttpResponse(f"<p>{post_data}</p>")


class ContributeView(View):
    template_name = "Contributor/contribute.html"

    def get(self, request):
        drafts = {
            "drafts": {
                "title": "Title1"
            }
        }
        return render(request, self.template_name, drafts)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DisplayProfileView(View):

    template_name = 'Contributor/user_profile.html'

    def get(self, request):
        user = User.objects.get(username=request.user.username, email=request.user.email)
        if user.isProfileComplete:
            return render(request, self.template_name)
        else:
            return redirect('Contributor:dashboard')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateProfileView(View):
    template_name = 'Contributor/create_profile.html'
    context = {
        "subjects": [
            "DSA",
            "DBMS",
            "CN",
        ]
    }

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        print("hi")
        try:
            profile = ContributorProfile.objects.get(uid=user)
            print(profile)
            if profile is not None:
                return redirect("Contributor:dashboard")
            else:
                return render(request, self.template_name, self.context)
        except:
            print("profile doesn't exist")

        return render(request, self.template_name, self.context)

    def post(self, request):
        post_data = dict(request.POST)
        json_data = json.dumps(post_data)
        print(json_data)

        username = request.user.username
        email = request.user.email
        first_name = post_data["first_name"][0]
        last_name = post_data["last_name"][0]
        dob = post_data["dob"][0]
        phone_number = post_data["phone_number"][0]
        city = post_data["city"][0]
        college = post_data["college"][0]
        university = post_data["university"][0]
        qualification = post_data["qualification"][0]
        years_of_experience = post_data["years_of_exp"][0]
        subjects_to_contribute = post_data["subjects_to_contrib"]
        subjects_of_interest = post_data["subjects_of_interest"]
        linkedin_profile = post_data["linkedin"][0]
        github_profile = post_data["github"][0]
        portfolio_website = post_data["portfolio"][0]

        user = User.objects.get(email=email)

        profile = ContributorProfile(uid=user, first_name=first_name, last_name=last_name, email=email, dob=dob, phone_number=phone_number, city=city, college=college, university=university, qualification=qualification, years_of_experience=years_of_experience, subjects_to_contribute=subjects_to_contribute, subjects_of_interest=subjects_of_interest,linkedin_profile=linkedin_profile, github_profile=github_profile, portfolio_website=portfolio_website)
        profile.save()

        user.isProfileComplete = True
        user.save()

        return render(request, self.template_name, self.context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


