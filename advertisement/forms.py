from django.forms import ModelForm
from advertisement.models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from datetime import date

class SavedAddressForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(SavedAddressForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'new_job_form_components'

    class Meta:
        model = SavedAddress
        exclude = ['User']
        widgets = {
            
        'Line1': forms.TextInput(attrs={'name':'ADDRESS_LINE1','id':'autocomplete','placeholder':'Line 1','class':'profile_form_components','autocomplete':'street-address','aria-autocomplete':'list'}),
        'Line2': forms.TextInput(attrs={'name':'sublocality_level_2','id':'sublocality_level_2','placeholder':'Line 2','class':'profile_form_components','autocomplete':'address-level1'}),
        'City': forms.TextInput(attrs={'name':'locality','id':'locality','placeholder':'City','class':'profile_form_components','autocomplete':'address-level2'}),
        'State': forms.TextInput(attrs={'name':'administrative_area_level_1','id':'administrative_area_level_1','placeholder':'State','class':'profile_form_components','autocomplete':'address-level1'}),
        'Country': forms.TextInput(attrs={'name':'country','id':'country','placeholder':'Country','class':'profile_form_components','autocomplete':'address-level2'}),
        'Zipcode': forms.TextInput(attrs={'name':'postal_code','id':'postal_code','placeholder':'Postal Code','class':'profile_form_components'}),
       
        }


def start_date():
    date_today = date.today().strftime('%Y-%m-%d')
    return date_today


class JobForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = ' new_job_form_components'
            
        self.fields['Date'] = forms.DateField()
   
    class Meta:
        model = Job
        exclude = ['Customer','Status']
   
        widgets = {
        
        'Description': forms.Textarea(attrs={'placeholder':'Enter Description','class':'col-sm-11','style':'top:2rem'}),
        'Date': forms.DateInput(format=('%m:%d:%Y'), attrs={ 'placeholder':'Select a date', 'type':'date', 'value':start_date, 'min':start_date}),
        'Time': forms.TimeInput(format=('%H:%M'), attrs={ 'placeholder':'Select a time', 'type':'time'}),
        'Location' : forms.HiddenInput(attrs={'name':'Location','class':'col-sm-11','placeholder': 'Enter location','disabled':'true'}),
  
        }

  


class JobapplicationForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(JobapplicationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():

            visible.field.widget.attrs['class'] = 'form-control  new_job_form_components'

    class Meta:
        model = JobRequest
        exclude = ['Technician','Job']

        widgets = {
            'Quote': forms.Textarea(attrs={'cols':'100','placeholder':'Enter your quote ','class':'col-lg-12','style':'top:2rem'}),
            'Date': forms.DateInput(format='%m:%d:%Y',attrs={'placeholder':'Select a date', 'type':'date', 'style':'margin-top:2rem' ,'id':'datepicker','min':start_date,'value':start_date }),
            'Time': forms.TimeInput(format='%H:%M',attrs={'placeholder':'Select a time', 'type':'time','style':'top:2rem'}),
        }

    
class JobresponseForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(JobresponseForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  new_job_form_components'
        
    class Meta:
        model = JobResponse
        exclude = ['Customer','Jobrequest','Response']
    
        widgets = {
            
            'Message': forms.Textarea(attrs={'cols':'100','placeholder':'Enter your Message with date and time','class':'col-lg-12','style':'top:2rem'}) , 
            'Date': forms.DateInput(format='%m:%d:%Y',attrs={'placeholder':'Select a date', 'type':'date', 'style':'margin-top:2rem' ,'id':'datepicker','min':start_date,'value':start_date }),
            'Time': forms.TimeInput(format='%H:%M',attrs={'placeholder':'Select a time', 'type':'time','style':'top:2rem'}),

            }

class ReviewForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control  new_job_form_components'

    class Meta:
        model = Review
        exclude = ['Reviewer','Reviewee',"Appointment",'Rating']
   
        widgets = {
        
        'Comment': forms.Textarea(attrs={'placeholder':'Enter your comments','class':'col-sm-11','style':'top:2rem'}),
        
        }





