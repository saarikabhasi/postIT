from django.forms import ModelForm
from account.models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['Fullname','Recovery_email']

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['Title','Employment_type','Company','Start_date','End_date']

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['School','Degree','Field_of_study','Start_date','End_date']

class AddressForm(forms.Form):
    class Meta:
        model = Address
        fields = ['Line1','Line2','State','Country','Zipcode']


