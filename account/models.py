from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, ValidationError
from account.managers import *
import advertisement.models 
from datetime import datetime
from .validators import *

# Create your models here.



class User(AbstractUser):
    username = models.CharField(max_length = 50, blank = False, null = False, unique = True)
    email = models.EmailField(validators=[EmailValidator],unique = True,blank = False) 
    role = models.CharField(max_length = 50,blank = False, null = False,default ="role")
    is_technician = models.BooleanField('Technician', default=False)
    is_customer = models.BooleanField('Customer', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role'] 
    
    def __str__(self): 
        return f"{self.id,self.username,self.email,self.role,self.is_technician,self.is_customer}"

    objects = UserManager()

    

class Address(models.Model):
    # user can have one current address and many saved address
    User = models.OneToOneField(User,on_delete=models.CASCADE,related_name="currentaddress",null=True,blank=True,unique=True)
    Useraddress = models.OneToOneField(advertisement.models.SavedAddress,on_delete=models.CASCADE,null=True,blank=True,unique=True)
    def __str__(self): 
        return f"{self.User,self.Useraddress}"
    objects = AddressManager()

employment_type_choices = []
("FULL-TIME, Full-Time"),
("PART_TIME","Part-time"),

class Experience(models.Model):
    
    User = models.ForeignKey(User,on_delete=models.CASCADE,related_name="work")
    Title = models.CharField(max_length = 50, blank = True)
    Employment_type = models.CharField(max_length = 50, blank = True,choices=employment_type_choices)
    Company = models.CharField(max_length = 50, blank = True)
    Start_date = models.DateField()
    End_date = models.DateField()
    def __str__(self): 
        return f"{self.User,self.Title,self.Employment_type,self.Company,self.Start_date,self.End_date}"

    objects = ExperienceManager()




class Education(models.Model):
    User= models.ForeignKey(User,on_delete=models.CASCADE,related_name="education")
    School = models.CharField(max_length = 50, blank = True)
    Degree = models.CharField(max_length = 50, blank = True)
    Field_of_study = models.CharField(max_length = 50, blank = True)
    Start_date = models.DateField()
    End_date = models.DateField()
   
    def __str__(self): 
        return f"{self.User,self.School,self.Degree,self.Field_of_study,self.Start_date,self.End_date}"
    objects = EducationManager()





#user can have one profile
class Profile(models.Model):    
    User = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile",unique=True)
    Fullname = models.CharField(max_length = 50, blank = True,null = True)
    Recovery_email = models.EmailField(validators=[EmailValidator],unique = False,blank = False,null = True)
    Address = models.ForeignKey(Address,null = True,on_delete=models.SET_NULL,related_name="address")
    Phone_number = models.CharField(max_length = 15,validators=[phonenumberValidator],null=True,blank=True) 

    Designation = models.CharField(max_length = 50, blank = True,null = True)
    About = models.CharField(max_length = 50, blank = True,null = True)
    Licence = models.BooleanField('Licence',default=False)
    Totalexperience = models.IntegerField( blank = True,null = True,default=0)
    Education = models.ForeignKey(Education,null = True,on_delete=models.SET_NULL,related_name="education")
    Experience = models.ForeignKey(Experience,null = True,on_delete=models.SET_NULL,related_name="experience")

    
    

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % (self.Fullname)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        short_name = self.Fullname.split(" ",1)
        return short_name

    def get_user_address(self):
        return self.Address


    def __str__(self): 
        return f"{self.User,self.Fullname,self.Recovery_email,self.Phone_number,self.Address,self.Totalexperience,self.Licence}"
    
    objects = ProfileManager()
  

class Discussion(models.Model):
    User = models.ForeignKey(User,null = False,on_delete=models.CASCADE,related_name="Userdiscussion")
    Jobrequest = models.ForeignKey(advertisement.models.JobRequest,null=True,blank=True,on_delete=models.CASCADE,related_name="IncomingJobrequest")
    Jobresponse = models.ForeignKey(advertisement.models.JobResponse,null=True,blank=True,on_delete=models.CASCADE,related_name="OutgoingJobresponse")
    Updated_date_time = models.DateTimeField("DateTime",auto_now=True)
    Checked = models.BooleanField('check', default=False)
    def __str__(self): 
        return f"{self.User,self.Jobrequest,self.Jobresponse,self.Updated_date_time,self.Checked }"


class Notification(models.Model):
    # common messages like, appointment created or job status changed
    User = models.ForeignKey(User,null = False,on_delete=models.CASCADE,related_name="userNotification")
    Message = models.TextField(max_length = 1000,null =True)
    Appointment = models.ForeignKey(advertisement.models.Appointment,on_delete=models.CASCADE,related_name="userAppointment")
    Job = models.ForeignKey(advertisement.models.Job,null = True,on_delete=models.CASCADE,related_name="userJob")
    Checked = models.BooleanField('check', default=False)
    Updated_date_time = models.DateTimeField("DateTime",auto_now=True)
    def __str__(self): 
        return f"{self.User,self.Message,self.Checked }"
