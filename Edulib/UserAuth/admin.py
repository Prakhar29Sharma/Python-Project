from django.contrib import admin
from .models import User, Student, Contributor, Evaluator
# Register your models here.

admin.register(User)
admin.register(Student)
admin.register(Contributor)
admin.register(Evaluator)
