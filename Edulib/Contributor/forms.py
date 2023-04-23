from django import forms
from .models import ContributorProfile, CourseContent
from ckeditor.widgets import CKEditorWidget


class CreateContentForm(forms.ModelForm):
    class Meta:
        model = CourseContent
        fields = '__all__'
    body = forms.CharField(widget=CKEditorWidget())
