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
from pymongo import MongoClient
from bson.objectid import ObjectId

User = get_user_model()


client = MongoClient("mongodb://localhost:27017/")
mydb = client["my_database"]
course_draft = mydb["course_draft"]

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
        profile = ContributorProfile.objects.get(email=request.user.email)
        subjects = profile.subjects_to_contribute
        subjects = subjects.replace("[", "").replace("]", "").replace("'", "")
        subjects = subjects.split(", ")
        context = {
            "subjects": subjects
        }
        return render(request, self.template_name, context)

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
        username = request.user.username
        user = User.objects.get(username=username)
        uid = user.pk
        course_title = post_data["course_title"][0]
        subject = self.kwargs['subject']
        unit = self.kwargs['unit']
        course_description = post_data["course_description"][0]
        objectives = post_data["objectives"]
        prerequisites = post_data["prerequisites"]
        course_video = post_data["course_video"][0]
        body = post_data["body"][0]

        document = {
            "uid": uid,
            "username": username,
            "course_title": course_title,
            "subject": subject,
            "unit": unit,
            "course_description": course_description,
            "objectives": objectives,
            "prerequisites": prerequisites,
            "course_video": course_video,
            "body": body
        }

        # mongodb
        course_draft.insert_one(document)
        return HttpResponse(f"<p>{post_data}, username: {username}, userid: {uid}</p>")


class DraftView(View):
    template_name = "Contributor/show_draft.html"
    context = {}

    def get(self, request):
        self.context = {}
        return render(request, self.template_name, self.context)

    def post(self, request):
        course_id = request.POST["course_id"]
        uid = request.user.pk
        _id = ObjectId(course_id)
        draft = course_draft.find_one({"uid": uid, "_id": _id})
        self.context = {
            "draft": draft
        }
        return render(request, self.template_name, self.context)


class ContributeView(View):
    template_name = "Contributor/contribute.html"

    def get(self, request):
        context = {
            "drafts": course_draft.find({"uid": request.user.pk}),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DisplayProfileView(View):

    template_name = 'Contributor/user_profile.html'

    def get(self, request):
        user = User.objects.get(username=request.user.username, email=request.user.email)
        if user.isProfileComplete:
            profile = ContributorProfile.objects.get(uid=user)
            context = {
                "profile": profile
            }
            return render(request, self.template_name, context)
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

        if user.isProfileComplete:
            return redirect("Contributor:dashboard")

        return render(request, self.template_name, self.context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



