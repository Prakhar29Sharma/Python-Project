from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# abstract class
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        CONTRIBUTOR = "CONTRIBUTOR", "Contributor"
        EVALUATOR = "EVALUATOR", "Evaluator"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    isProfileComplete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


# Filter out STUDENT
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)

    def create_user(self, username, email, password):
        student = Student(username=username, password=password, email=email)
        student.set_password(password)
        student.save()


class Student(User):
    base_role = User.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


# Filter out CONTRIBUTOR
class ContributorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CONTRIBUTOR)

    def create_user(self, username, email, password):
        contrib = Contributor(username=username, password=password, email=email)
        contrib.set_password(password)
        contrib.save()


class Contributor(User):
    base_role = User.Role.CONTRIBUTOR

    contributor = ContributorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for contributors"


# Filter out EVALUATOR
class EvaluatorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EVALUATOR)

    def create_user(self, username, email, password):
        evaluator = Evaluator(username=username, password=password, email=email)
        evaluator.set_password(password)
        evaluator.save()


class Evaluator(User):
    base_role = User.Role.EVALUATOR

    evaluator = EvaluatorManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for evaluators"
