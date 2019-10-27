from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Project, Comments, Rate

class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'date', 'firstname', 'lastname']
        

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['pub_date','user','profile']


class commentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['posted_by','profile','commented_project']


class RateForm(forms.ModelForm):
    class Meta:
        model =Rate
        exclude= ['user','project']