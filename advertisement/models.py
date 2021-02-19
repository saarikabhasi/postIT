from django.db import models
from django.core.validators import EmailValidator, ValidationError
from .managers import *
from datetime import datetime
import account.models

# Create your models here.

class SavedAddress(models.Model):
    #all saved address

    User = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name="savedAddress")
    Line1 = models.CharField(max_length = 80, blank = False,default="line 1")
    Line2 = models.CharField(max_length = 80, blank = True,default="line 2")
    City = models.CharField(max_length = 80, blank = False,default="city")
    State = models.CharField(max_length = 80, blank = False,default="state")
    Country = models.CharField(max_length = 80, blank = False,default="country")
    Zipcode = models.IntegerField(blank = False,default=0)
    


    def __str__(self): 
        return f"{self.id,self.User,self.Line1,self.Line2,self.City,self.State,self.Country,self.Zipcode}"
    objects = SavedAddressManager()
            
    
job_type_choices = (
("ELECTRICAL","Electrical"),
("PLUMBING","Plumbing"),
("HANDYMAN","Handyman"),)

priority_type_choices = (
("URGENT","Urgent"),
("MODERATE","Moderate"),)

job_status = (
("OPEN","Open"),
("PENDING","Pending"),
("CLOSED","Closed"),)


class Job(models.Model):
    #model that stores job information

    Customer = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name="Customer")
    Job_type = models.CharField(max_length = 50, null = False, blank = False,choices=job_type_choices,default=job_type_choices)
    Description = models.CharField(max_length = 500, blank = True, null = False)
    Location = models.ForeignKey(SavedAddress,on_delete=models.SET_NULL,related_name="jobLocation",null=True)
    Date = models.DateField("Required Date",default=datetime.today().strftime('%Y-%m-%d'))
    Time = models.TimeField("Required Time",default=datetime.now)
    Priority = models.CharField(max_length = 10,null=False,blank=False,choices=priority_type_choices,default=priority_type_choices[0][0])
    Amount = models.DecimalField(max_digits=6, decimal_places=0,default=50)
    Currency = models.CharField(max_length=15,default ="USD")
    Technician_experience_preference = models.IntegerField(default=0)
    Licence = models.BooleanField('Licence',default=False)
    Status = models.CharField(max_length = 50,choices=job_status,default=job_status[0][0])


    
    @classmethod
    def default_priority(cls):
        if 0<=cls.Date - datetime.datetime.now()<=2:
            return Job.Date.update(default="Urgent")

        
    @classmethod
    def default_location(cls,id):
        return {'id':2}
    
    def __str__(self): 

        return f"{self.id,self.Customer,self.Job_type,self.Description,self.Location.__str__(),self.Date,self.Priority,self.Amount,self.Currency,self.Technician_experience_preference,self.Licence,self.Status }"
    
    objects = JobManager()


class JobRequest(models.Model):
    Technician =  models.ForeignKey('account.User',on_delete=models.CASCADE,related_name="RequestTechnician")
    Job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="Job",null=False,blank=False,default="None")
    Quote = models.TextField(max_length = 1000)
    Date = models.DateField("Date",default=datetime.today().strftime('%Y-%m-%d'))
    Time = models.TimeField("Time",default=datetime.now)
    Amount = models.DecimalField(max_digits=6, decimal_places=0,default=50)
    Currency = models.CharField(max_length=15,default ="USD")
    def __str__(self): 
        return f"{self.id,self.Technician,self.Job }"

job_response_choice = (
("ACCEPT","Accept"),
("REJECT","Reject"),
)

class JobResponse(models.Model):
    Customer = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name="ResponseCustomer")
    Jobrequest = models.ForeignKey(JobRequest,on_delete=models.CASCADE,related_name="Jobrequest")
    Message = models.TextField(max_length = 1000,null =True)
    Response = models.CharField(max_length = 50, null = False, blank = False,choices=job_response_choice,default=job_response_choice)
    Date = models.DateField("Date",default=datetime.today().strftime('%Y-%m-%d'))
    Time = models.TimeField("Time",default=datetime.now)
    Amount = models.DecimalField(max_digits=6, decimal_places=0,default=50)
    Currency = models.CharField(max_length=15,default ="USD")

    def __str__(self): 
        return f"{self.id,self.Customer,self.Jobrequest,self.Response }"



class Appointment(models.Model):
    Job = models.ForeignKey('advertisement.Job',on_delete=models.CASCADE,related_name="Upcoming_jobs")
    Technician = models.ForeignKey('account.User',on_delete=models.CASCADE,related_name="Technician")
    Jobresponse = models.ForeignKey(JobResponse,on_delete=models.CASCADE,related_name="Jobresponse")
    def __str__(self): 
        return f"{self.id,self.Job,self.Technician,self.Jobresponse }"

class Review(models.Model):
    Reviewer = models.ForeignKey('account.User',null = False,on_delete=models.CASCADE,related_name="Reviewer")
    Reviewee = models.ForeignKey('account.User',null = False,on_delete=models.CASCADE,related_name="Reviewee")
    Comment = models.TextField(max_length = 100, blank = True,null = True)
    Rating = models.DecimalField("Rating",max_digits=2,null=True,blank=True, decimal_places=1)
    Appointment = models.ForeignKey(Appointment,on_delete=models.SET_NULL,null=True,related_name="reviewed_appointment")
    def __str__(self): 
        return f"{self.Reviewer,self.Reviewee,self.Comment,self.Rating,self.Appointment}"

