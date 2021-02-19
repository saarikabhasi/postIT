from django.db import models
import account.models
import advertisement.models
from datetime import date,timedelta
from django.db.models import Q
from django.conf import settings
def notification_check(request):
    
    """
    Count number of unchecked notifications
    
    """
    try:
        count = account.models.Notification.objects.filter(User=request.user,Checked=False).count()
        
    except:
        count = 0

    return{'not_checked_notifications_count':count }

def discussion_check(request):
    
    """
    Count number of unchecked discussions
    
    """
    try:
        count = account.models.Discussion.objects.filter(User=request.user,Checked=False).count()
    except:
        count = 0

    return{'not_checked_discussions_count':count }

def appointment_expiry_check(request):
    """
    1. Change job status to closed for the jobs that are older than 7 days,  
    2. delete those jobs
    """
    today = date.today()
    
    #get all the appointments which is past today
    # change the status to closed
    
    jobresponse_id = advertisement.models.Appointment.objects.all().values("Jobresponse")
   
    jobresponse =advertisement.models.JobResponse.objects.filter(Date__lt =today-timedelta(days=7)).filter(id__in = jobresponse_id)
    
    appointments = advertisement.models.Appointment.objects.all().filter(Jobresponse__id__in=jobresponse)

    # change status of old jobs and add to past jobs and delete them
    # jobs whose status to be changed
   
    jobs = advertisement.models.Job.objects.filter(id__in=appointments.values_list("Job",flat=True))
    


    jobs.update(Status = "Closed") 
    jobs.delete()

    return{'Delete':True }

def google_key(request):
    """
    Get google key from setting
    """
    return {'google_key': settings.GOOGLE_KEY}
    
    

