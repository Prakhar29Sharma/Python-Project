import json

import requests
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ContributorProfileForm, CreateContentForm


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


class CreateProfileView(View):
    form_class = ContributorProfileForm
    template_name = 'Contributor/create_profile.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        post_data = dict(request.POST)
        json_data = json.dumps(post_data)
        print(json_data)

        first_name = post_data["first_name"][0]
        last_name = post_data["last_name"][0]
        dob = post_data["dob"][0]
        phone_number = post_data["phone_number"][0]
        city = post_data["city"][0]
        college = post_data["college"][0]
        university = post_data["university"][0]
        qualification = post_data["qualification"][0]
        years_of_experience = post_data["years_of_exp"][0]
        subjects_to_contribute = post_data["subjects_to_contribute"]
        subjects_of_interest = post_data["subjects_of_interest"]
        linkedin_profile = post_data["linkedin"][0]
        github_profile = post_data["github"][0]
        portfolio_website = post_data["portfolio"][0]

        profile = CreateContentForm()

        return render(request, self.template_name)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


