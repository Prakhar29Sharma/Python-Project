from django.urls import path
from .views import DashboardView, CreateProfileView
from django.contrib.auth.decorators import login_required

app_name = "Contributor"

urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("profile/", login_required(CreateProfileView.as_view()), name="create_profile"),
]
