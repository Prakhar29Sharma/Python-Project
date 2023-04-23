from django.urls import path
from .views import DashboardView, CreateProfileView, ContributeView, CreateCourseView, CreateContentView, DisplayProfileView, DraftView, DeleteDraftView, SubmitForReview
from django.contrib.auth.decorators import login_required

app_name = "Contributor"

urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("create_profile/", login_required(CreateProfileView.as_view()), name="create_profile"),
    path("profile/", login_required(DisplayProfileView.as_view()), name="profile"),
    path("contribute/", login_required(ContributeView.as_view()), name="contribute"),
    path("course/", login_required(CreateCourseView.as_view()), name="create_course"),
    path("course/<str:subject>/<str:unit>/", login_required(CreateContentView.as_view()), name="create_content"),
    path("draft/<str:course_id>/", login_required(DraftView.as_view()), name="draft_view"),
    path("draft/delete/<str:course_id>/", login_required(DeleteDraftView.as_view()), name="delete_draft"),
    path("draft/submit/<str:course_id>/", login_required(SubmitForReview.as_view()), name="submit_for_review")
]
