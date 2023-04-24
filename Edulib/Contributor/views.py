import datetime
import json
import os.path

import requests
from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import CreateContentForm
from .models import ContributorProfile
# from UserAuth.models import Contributor
from django.contrib.auth import get_user_model
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.http import FileResponse
import random
import string

User = get_user_model()

client = MongoClient("mongodb://localhost:27017/")
mydb = client["my_database"]
course_draft = mydb["course_draft"]
courses = mydb["courses"]
notifications = mydb["notifications"]
# Create your views here.


# class DashboardView(View):
#     def get(self, request):
#         return render(request, "Contributor/index.html")

class DashboardView(View):
    template_name = "Contributor/index.html"
    context = {}

    def get(self, request):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1
        self.context = {
            "notifications": notifications.find({"uid": request.user.pk}),
            "notifications_count": count,
            "my_contributions": courses.find({"uid": request.user.pk})
        }
        return render(request, self.template_name, self.context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateCourseView(View):
    template_name = "Contributor/create_course.html"

    def get(self, request):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1
        profile = ContributorProfile.objects.get(email=request.user.email)
        subjects = profile.subjects_to_contribute
        subjects = subjects.replace("[", "").replace("]", "").replace("'", "")
        subjects = subjects.split(", ")
        context = {
            "subjects": subjects,
            "notifications": notifications.find({"uid": request.user.pk}),
            "notifications_count": count
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
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1
        subject = self.kwargs['subject']
        unit = self.kwargs['unit']
        context = {
            "subject": subject,
            "unit": unit,
            "form": self.form,
            "notifications": notifications.find({"uid": request.user.pk}),
            "notifications_count": count
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
        course_video = request.FILES["course_video"]
        course_image = request.FILES["course_image"]
        body = post_data["body"][0]

        letters = string.digits
        course_id = ''.join(random.choice(letters) for i in range(10))

        # handling video uploaded
        original_name, extension = os.path.splitext(course_video.name)
        new_file_name = str(uid) + str(course_id) + extension
        path = '/home/prakhar/Edulib/Edulib/static/' + new_file_name
        with open(path, 'wb+') as destination:
            for chunk in course_video.chunks():
                destination.write(chunk)

        # handling image uploaded
        if course_image:
            filename, extension = os.path.splitext(course_image.name)
            new_image_name = str(uid)+str(course_id)+extension
            path = os.path.join('/home/prakhar/Edulib/Edulib/static/' + new_image_name)
            with open(path, 'wb') as destination:
                for chunk in course_image.chunks():
                    destination.write(chunk)

        document = {
            "course_id": course_id,
            "uid": uid,
            "username": username,
            "course_title": course_title,
            "subject": subject,
            "unit": unit,
            "course_description": course_description,
            "objectives": objectives,
            "prerequisites": prerequisites,
            "course_video": new_file_name,
            "course_image": new_image_name,
            "body": body
        }

        # mongodb
        course_draft.insert_one(document)
        return redirect("Contributor:contribute")


class DraftView(View):
    template_name = "Contributor/show_draft.html"
    context = {}
    form = CreateContentForm()

    def get(self, request, course_id):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1
        uid = request.user.pk
        draft = course_draft.find_one({"uid": uid, "course_id": course_id})
        video_name = draft["course_video"]
        # path = os.path.join("/home/prakhar/Edulib/Edulib/static/", video_name)

        text_editor_content = draft["body"]
        self.form = CreateContentForm(initial={'body': text_editor_content})
        self.context = {
            "draft": draft,
            "video": video_name,
            "form": self.form,
            "notifications": notifications.find({"uid": request.user.pk}),
            "notifications_count": count
            # "course_content": text_editor_content
        }
        return render(request, self.template_name, self.context)

    def post(self, request, course_id):
        post_data = dict(request.POST)
        username = request.user.username
        user = User.objects.get(username=username)
        uid = user.pk
        draft = course_draft.find_one({"uid": uid, "course_id": course_id})
        course_title = post_data["course_title"][0]
        subject = draft["subject"]
        unit = draft["unit"]
        course_description = post_data["course_description"][0]

        if post_data["objectives"][0] == "":
            objectives = draft["objectives"]
        else:
            objectives = post_data["objectives"]

        if post_data["prerequisites"][0] == "":
            prerequisites = draft["prerequisites"]
        else:
            prerequisites = post_data["prerequisites"]

        body = post_data["body"][0]

        new_document = {
            "course_id": course_id,
            "uid": uid,
            "username": username,
            "course_title": course_title,
            "subject": subject,
            "unit": unit,
            "course_description": course_description,
            "objectives": objectives,
            "prerequisites": prerequisites,
            "body": body
        }

        updated_values = {"$set": new_document}

        course_draft.update_one({"uid": uid, "course_id": course_id}, updated_values)

        return redirect("Contributor:contribute")


class DeleteDraftView(View):

    def get(self, request, course_id):
        uid = request.user.pk
        course_draft.delete_one({"uid": uid, "course_id": course_id})
        return redirect("Contributor:contribute")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SubmitForReview(View):
    def get(self, request, course_id):
        uid = request.user.pk
        email = request.user.email
        user = User.objects.get(email=email)

        course_content = course_draft.find_one({"uid": uid, "course_id": course_id})
        letters = string.digits
        new_id = ''.join(random.choice(letters) for i in range(10))
        course_content["_id"] = new_id
        courses.insert_one(course_content)
        subject = course_content["subject"]
        unit = course_content["unit"]
        upload_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        notifications.insert_one({
            "uid": uid,
            "subject": subject,
            "unit": unit,
            "upload_time": upload_time
        })
        return redirect("Contributor:contribute")


class CourseView(View):
    template_name = "Contributor/show_course.html"
    context = {}

    def get(self, request, course_id):
        course_content = courses.find_one({"course_id": course_id})
        self.context = {
            "course_content": course_content
        }
        return render(request, self.template_name, self.context)


class ContributeView(View):
    template_name = "Contributor/contribute.html"

    def get(self, request):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1
        context = {
            "drafts": course_draft.find({"uid": request.user.pk}),
            "notifications": notifications.find({"uid": request.user.pk}),
            "notifications_count": count
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class DisplayProfileView(View):
    template_name = 'Contributor/user_profile.html'

    def get(self, request):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1
        user = User.objects.get(username=request.user.username, email=request.user.email)
        if user.isProfileComplete:
            profile = ContributorProfile.objects.get(uid=user)
            context = {
                "profile": profile,
                "notifications": notifications.find({"uid": request.user.pk}),
                "notifications_count": count
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
        ],

    }

    def get(self, request):

        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1

        self.context["notifications"] = notifications.find({"uid": request.user.pk})
        self.context["notifications_count"]: count

        user = User.objects.get(email=request.user.email)
        # print("hi")
        try:
            profile = ContributorProfile.objects.get(uid=user)
            # print(profile)
            if profile is not None:
                return redirect("Contributor:dashboard")
            else:
                return render(request, self.template_name, self.context)
        except:
            print("profile doesn't exist")

        return render(request, self.template_name, self.context)

    def post(self, request):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1

        self.context["notifications"] = notifications.find({"uid": request.user.pk})
        self.context["notifications_count"]: count

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

        profile = ContributorProfile(uid=user, first_name=first_name, last_name=last_name, email=email, dob=dob,
                                     phone_number=phone_number, city=city, college=college, university=university,
                                     qualification=qualification, years_of_experience=years_of_experience,
                                     subjects_to_contribute=subjects_to_contribute,
                                     subjects_of_interest=subjects_of_interest, linkedin_profile=linkedin_profile,
                                     github_profile=github_profile, portfolio_website=portfolio_website)
        profile.save()
        
        c = User.objects.get(pk=request.user.pk)
        c.isProfileComplete = True
        c.save()

        if c.isProfileComplete:
            return redirect("Contributor:dashboard")

        return render(request, self.template_name, self.context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OthersContributionView(View):
    template_name = "Contributor/others_contributions.html"
    context = {}

    def get(self, request):
        count = 0
        n = notifications.find({"uid": request.user.pk})
        for x in n:
            count += 1

        others_courses = courses.find({"uid": {"$ne": request.user.pk}})

        self.context = {
            "notifications": notifications.find({"uid": request.user.pk}),
            "notifications_count": count,
            "courses": others_courses
        }
        return render(request, self.template_name, self.context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)