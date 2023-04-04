from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ContributorProfileForm

# Create your views here.


# class DashboardView(View):
#     def get(self, request):
#         return render(request, "Contributor/index.html")

class DashboardView(TemplateView):
    template_name = "Contributor/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateProfileView(View):
    form_class = ContributorProfileForm
    template_name = 'Contributor/create_profile.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # link uid and email to profile
            form.save()
            # set isProfileComplete to true from false
            return HttpResponse("Your profile is created!")
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


