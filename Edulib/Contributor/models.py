from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
from ckeditor.fields import RichTextField
User = get_user_model()

SUBJECTS = [
    ('DSA', 'DSA'),
    ('DBMS', 'DBMS'),
    ('CN', 'CN'),
]


class ContributorProfile(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    dob = models.DateField()
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    college = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    qualification = models.CharField(max_length=50)
    years_of_experience = models.PositiveIntegerField()
    subjects_to_contribute = models.CharField(
        choices=SUBJECTS,
        max_length=50,
        blank=True,
        null=True
    )
    subjects_of_interest = models.CharField(
        choices=SUBJECTS,
        max_length=50,
        blank=True,
        null=True

    )
    linkedin_profile = models.URLField(max_length=200)
    github_profile = models.URLField(max_length=200)
    portfolio_website = models.URLField(max_length=200)


class CourseContent(models.Model):
    body = RichTextField(blank=True, null=True)



