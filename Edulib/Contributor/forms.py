from django import forms
from .models import ContributorProfile

SUBJECTS_TO_CONTRIBUTE = [
    ('', 'Choose...'),
    ('DSA', 'DSA'),
    ('Python Programming', 'Python Programming'),
    ('Unix', 'Unix'),
    ('DBMS', 'DBMS'),
    ('Computer Networks', 'Computer Networks'),
    ('Computer Architecture', 'Computer Architecture'),
    ('Operating Systems', 'Operating System'),
    ('Java Programming', 'Java Programming'),
]

INTERESTS = (
    ('', 'Choose...'),
    ('DSA', 'DSA'),
    ('Python Programming', 'Python Programming'),
    ('Unix', 'Unix'),
    ('DBMS', 'DBMS'),
    ('Computer Networks', 'Computer Networks'),
    ('Computer Architecture', 'Computer Architecture'),
    ('Operating Systems', 'Operating System'),
    ('Java Programming', 'Java Programming'),
)


class ContributorProfileForm(forms.ModelForm):
    subjects_to_contribute = forms.MultipleChoiceField(choices=SUBJECTS_TO_CONTRIBUTE,
                                                      widget=forms.CheckboxSelectMultiple)
    subjects_of_interest = forms.MultipleChoiceField(choices=INTERESTS, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ContributorProfile
        fields = ['first_name', 'last_name', 'dob', 'phone_number', 'city', 'college', 'university', 'qualification', 'years_of_experience', 'subjects_to_contribute', 'subjects_of_interest', 'linkedin_profile', 'github_profile', 'portfolio_website']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }
