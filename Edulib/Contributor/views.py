import json

from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ContributorProfileForm
from .models import ContributorProfile

# Create your views here.


# class DashboardView(View):
#     def get(self, request):
#         return render(request, "Contributor/index.html")

class DashboardView(TemplateView):
    template_name = "Contributor/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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
        subjects = []
        return render(request, self.template_name)

    def post(self, request):
        post_data = dict(request.POST)
        json_data = json.dumps(post_data)
        print(json_data)
        return render(request, self.template_name)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ViewProfile(View):
       def get(self, request):
           all_ContributorProfile = ContributorProfile.objects.all
           return render(request, "Contributor/ViewProfile.html",{'all':all_ContributorProfile})
     
    