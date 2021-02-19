from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404,HttpRequest
from django.contrib.auth.decorators import login_required
from django.db import models
from django.urls import reverse
from . import forms
import account.models
import account.util
from collections import deque
from .models import *
from django.db.models import Q
import json
from json import dumps 
from django.template import loader
from functools import reduce
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from datetime import date
# Create your views here.
jobsearch_stack=deque()
request_method_get =(
    ('GET','get'),
   
)
request_method_post =(
    ('POST','post'),
   
)
def paginate(request,argument):

    """
    1. Function to paginate - maximum 5 count on a page
    """
    page_number = request.GET.get('page',1)
    paginator = Paginator(argument, 5) 

    try:
        paginated_argument = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_argument = paginator.page(1)
    except EmptyPage:
        paginated_argument = paginator.page(paginator.num_pages)
    
    return paginated_argument

def index(request):

    """
    index -show all jobs 
    """
 
    if request.user.is_authenticated:
        #clear search stack
        jobsearch_stack.clear()
        
        jobs = paginate(request,Job.objects.all().order_by('Date'))
        return render(request,"advertisement/index.html",{
            "jobs":jobs,
 
            "job_requests_ids":list(JobRequest.objects.filter(Technician=request.user).values_list("Job",flat=True)),
            })
        
    else:
        return HttpResponseRedirect(reverse("account:login"))

def job_profile(request,**args):
    """
    show job profile
    """
    if request.user.is_authenticated:
        #get job id from url
        job_id = args["id"]
    
        #check if request already sent 
        request_sent = check_job_request_sent(request,job_id)
 


        # get job location
        inst = Job.objects.get(id=job_id)
        loc = inst.Location
        
        #render to webpage
        return render(request,"advertisement/job-profile.html",{
            "job":inst,
            "location":loc,
            'request_sent':request_sent,
            
            })
        
    else:
        return HttpResponseRedirect(reverse("account:login"))
status = ["OPEN","PENDING"]
job_type = ['ELECTRICAL', 'PLUMBING','HANDYMAN']

@login_required
def jobsearch(request,**args):
    """  
    Job search via filter
    Filter options: Job type and Job status
    jobsearch_stack is Doubly Ended Queue

    """
    
    if request.user.is_authenticated:
        searchby = args["type"]
        if searchby not in jobsearch_stack:
            jobsearch_stack.append(searchby)

        else:
            jobsearch_stack.remove(searchby)
        result = ""
        status_list = []
        job_list = []
        for i in jobsearch_stack:
            if i in status:
                status_list.append(i)
            if i in job_type:
                job_list.append(i)

        if len(status_list) == 0:
            status_list = status
        if len(job_list) == 0:
            job_list = job_type
        
        #ignore case of status/job type for lookup
        j_list = map(lambda jname: Q(Job_type__iexact=jname), job_list)
        j_list = reduce(lambda a, b: a | b, j_list)
        
        s_list = map(lambda sname: Q(Status__iexact=sname), status_list)
        s_list = reduce(lambda a, b: a | b, s_list)
   
        result = {"result":list(Job.objects.filter(j_list,s_list).order_by('Date').values()),
                  "job_requested_ids": list(JobRequest.objects.filter(Technician=request.user).values_list("Job",flat=True))}
        

        
        response = json.dumps(result,default=str)
        return HttpResponse(response,content_type = "application/json")
        

    else:
        return HttpResponseRedirect(reverse("account:login"))

def check_job_request_sent(request,job_id):
    """
    checks if job request had already been sent by user
    """
    # job instance
    job_instance = Job.objects.get(id=job_id)     
                   
    # check if user had already sent request 
    if JobRequest.objects.filter(Technician = request.user, Job=job_instance).exists():
        return True
    return False

@login_required
def job_application(request,**args):

    """
    1. Quote -charfield
    2. Available dates and time (date and time range)
    
    """

    
    job_id = args["id"] 
    if (any(request.method in i for i in request_method_get)):

        form= forms.JobapplicationForm()
        return render(request, "advertisement/job-application.html",{
            "applicationForm":form,
            "id":job_id,

        })
        
    if (any(request.method in i for i in request_method_post)):

        error =""
        message=""
        form= forms.JobapplicationForm(request.POST)
        if form.is_valid():
            Quote = form.cleaned_data["Quote"]
            Date = form.cleaned_data["Date"]
            Time = form.cleaned_data["Time"]
            Amount = form.cleaned_data["Amount"]
            Currency = form.cleaned_data["Currency"]


        try:
            #get job instance
            job_instance = Job.objects.get(id=job_id)     

            #user must be technician 
            if account.util.get_user_role(request) == "Technician":
                if check_job_request_sent(request,job_id): 
                    #previous job request exist so 
                    error = "Request already sent!"
                else:

                    #create job request
                    jobrequest = JobRequest.objects.create(Technician = request.user,Job=job_instance,Quote=Quote,Date=Date,Time=Time,Amount=Amount,Currency=Currency)
                    jobrequest.save()

                    #create discussion for job owner (customer)

                    #get customer instance
                    customer_instance = account.models.User.objects.get(id=job_instance.Customer.id)

                    #create discussion for customer
                    discussion = account.models.Discussion.objects.create(User=customer_instance,Jobrequest=jobrequest,Jobresponse=None,Checked=False)
                    discussion.save()

                    request.session['has_checked'] = False
           

                    message="Message sent!"
            else:
                # Customers not authorised to sent job request
                raise Http404("Not authorised")
        except:
            error = "Unable to process"

        
        return render(request, "advertisement/job-application.html",{
            "message":message,
            "error" :error,
            "id":job_id,

        })
    raise Http404("Not Found")

@login_required
def user_account(request,**args):

    if request.user.is_authenticated:
        
        initialcategory = ""
        if "section" in args.keys():
            initialcategory=args["section"]
        if (any(request.method in i for i in request_method_get)):
            # new-job form
            form = forms.JobForm()
            return render(request, "advertisement/ad.html",{
                "initialcategory":initialcategory,
                "Jobform":form,
            })
                
        if (any(request.method in i for i in request_method_post)):
            # new-job form
            form = forms.JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.Customer = request.user
                job.Status = 'OPEN'
                job.save()
                
                return HttpResponseRedirect(reverse("advertisement:index"))
            else:
                return render(request, "advertisement/ad.html",{
                "initialcategory":initialcategory,
                "Jobform":form,
            })

       

def section(request,**args):
    #navigate to sections in user_account

    result =""
    if request.user.is_customer:
        #get job profile
        job = Job.objects.filter(Customer=request.user)
    if args["section"] == "ads":
        if request.user.is_customer:
            result = {"result":list(job.order_by('Date').values())}
        else:
            raise Http404("Un authorised to perform this action")
    if args["section"] == "appointments":
      
        result = {"result": list(retrieve_appointments(request).values())}

    if args["section"] == "reviews":
        review =Review.objects.filter(Reviewee = request.user)
        result = {
            "result": list(review.values("Comment","Rating"))

            }
    if args["section"] == "given_reviews":
        givenreview =Review.objects.filter(Reviewer = request.user)
        result = {
            "result": list(givenreview.values("Comment","Rating"))

            }

    response = json.dumps(result,default=str)
    return HttpResponse(response,content_type = "application/json")


@login_required
def current_address(request,**args):

    try:
        user_address = account.models.Address.objects.get(User = request.user.id)
        #get user's saved current address form Saved address model
        current_address = SavedAddress.objects.filter(id=user_address.Useraddress.id)

    except:
        current_address = None

    #if there is no saved current address, show result as none
    if current_address!=None:
        result = {"result":list(current_address.values())}
    else:
        result ={"result":None}

    response = json.dumps(result,default=str)
    return HttpResponse(response,content_type = "application/json")

@login_required
def saved_address(request,**args):

    try:
        #check if user has set any current address

        if account.models.Address.objects.filter(User = request.user.id):
            user_address = account.models.Address.objects.get(User = request.user.id)
        else:
            user_address=None

        #exclude all address except current address
        if user_address:
            saved_address=SavedAddress.objects.filter(User=request.user.id).exclude(id=user_address.Useraddress.id).order_by('-id')
        else:
            #user has not current addresss set so take all address
            saved_address=SavedAddress.objects.filter(User=request.user.id)
    except:
        saved_address = None
    
    if saved_address!=None:
        result = {"result":list(saved_address.values())}
    else:
        result ={"result":None}

    response = json.dumps(result,default=str)
    return HttpResponse(response,content_type = "application/json")

@login_required
def add_new_address(request,**args):

    if (any(request.method in i for i in request_method_get)):
        response = ""
        return HttpResponse(response,content_type = "application/json")
    if (any(request.method in i for i in request_method_post)):

        if request.POST['address-type'].strip() == 'current':
            Line1 = request.POST["ADDRESS_LINE_1"]
            Line2 = request.POST["sublocality_level_2"]
            City = request.POST["locality"]
            State = request.POST["administrative_area_level_1"]
            Country = request.POST["country"]
            Zipcode = request.POST["postal_code"]
            # current
            # 1.add to saved address
            # 2. update address model and update profile
            try:
                user_instance = account.models.User.objects.get(id=request.user.id)
                save_address_obj,save_address_created = SavedAddress.objects.update_or_create(User=user_instance,Line1=Line1,Line2=Line2,City=City,State=State,Country=Country,Zipcode=Zipcode)

            except:
                print("unable to save Savedaddress")
            
           
            if account.models.Address.objects.get_filter(user_instance):
                Address.objects.get(User=user_instance).delete()
            try:
                address_obj,address_created = account.models.Address.objects.update_or_create(User= user_instance,Useraddress = save_address_obj)
                profile = account.util.update_profile("Address",user_instance,None,modelobj=address_obj)

        
            except:
                print("unable to save address")
                raise Http404("unable to save address")
            result = {"result":list(SavedAddress.objects.filter(id=save_address_obj.id).values())}

        
        if request.POST['address-type'].strip() == 'another':
            #another
            # 1.add to saved address

            try:
                user_instance = account.models.User.objects.get(id=request.user.id)
                savedaddressobj = SavedAddress.objects.create_SavedAddress(User=user_instance,Line1=request.POST['ADDRESS_LINE_1'],Line2=request.POST['sublocality_level_2'],City=request.POST['locality'],State=request.POST['administrative_area_level_1'],Country=request.POST['country'],Zipcode=request.POST['postal_code'] )

                savedaddressobj.save()
            except: 
                print("unable to save address")
                raise Http404("Error")
            #after adding new another address back to javascript

            print(list(SavedAddress.objects.filter(id=savedaddressobj.id).values()))

            result = {"result":list(SavedAddress.objects.filter(id=savedaddressobj.id).values())}

        response = json.dumps(result,default=str)
        return HttpResponse(response,content_type = "application/json")
            
            
@login_required
def fix_appointment(request,**args):

    jobresponse_id = args["id"]
    # get Jobresponse instance
    Jobresponse= JobResponse.objects.get(id=jobresponse_id)
    

    # if already an appointment exists then don not create
    if  not Appointment.objects.filter(Job=Jobresponse.Jobrequest.Job):
        appointment = Appointment.objects.create(Job=Jobresponse.Jobrequest.Job,Technician=request.user,Jobresponse=Jobresponse)
        appointment.save()

        # change status of job
        Job.objects.filter(id = Jobresponse.Jobrequest.Job.id).update(Status="Pending")
        
        #create notification for customer
        #get customer instance
        customer_instance = account.models.User.objects.get(id=Jobresponse.Customer.id)
        Message = f"You have one new appointment" 
        notification = account.models.Notification.objects.create(User=customer_instance,Message=Message,Appointment=appointment,Job = None,Checked=False)
        notification.save()

        request.session['has_checked'] = False
    else:
        raise Http404("unable to schedule appointment")
    # except:
    #     Http404("unable to schedule appointment")
    appointment_obj = Appointment.objects.filter(id=appointment.id)
    jobresponse_obj = JobResponse.objects.filter(id=Appointment.objects.get(id=appointment.id).Jobresponse.id)
   
    result = {
        "id":list(appointment_obj.values('id')),
        "Job_id":Jobresponse.Jobrequest.Job.id,
        "Date":list(jobresponse_obj.values('Date')),
        "Time":list(jobresponse_obj.values('Time')),
        "Amount":list(jobresponse_obj.values('Amount')),
        "Currency":list(jobresponse_obj.values('Currency')),
    }

    response = json.dumps(result,default=str)
    return HttpResponse(response,content_type = "application/json")

@login_required
def appointment(request,**args):


    if "id" in args.keys():
        appointment_job__id = args['id']
        review = False
        send_review = False
        appointment = Appointment.objects.get(Job__id=appointment_job__id)
        if request.user == appointment.Job.Customer or request.user== appointment.Technician:
            #if appointment is one day old, display a review form. 
            #user can enter their review
            appointment_ids = appointment_expiry_check(request)

            if appointment_ids:
                if (appointment.id in set(appointment_ids)):
                    #prevent double review
                    if not Review.objects.filter( Q(Appointment=appointment) & Q(Reviewer = request.user)): 
                        review = True
                        send_review= False
                    else:
                        send_review =True
                    
            
            return render(request, "advertisement/appointment.html",{
                "appointment":appointment,
                "review":review,
                "send_review":send_review
            })
        else:
            raise Http404("Unauthorised")
   

@login_required 
def retrieve_appointments(request,**args):
    #get all appointments for user
    # need job details, appointment time and date from job response.
    if request.user.is_customer:
        #get jobs by this customer
        appointments_job = Appointment.objects.all().values_list('Job',flat='True')
        
        jobs=Job.objects.filter(id__in = appointments_job).filter(Customer = request.user)
    
        # get date and time from job response
        


    if request.user.is_technician:
        appointments = Appointment.objects.filter(Technician=request.user)
        jobs= Job.objects.filter(id__in = appointments.values_list('Job',flat=True))


        
    return jobs 
        
        


@login_required
def review(request,**args):

    appointment_id =""
    if "id" in args.keys():
        appointment_id = args["id"]
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except:
            raise Http404("Unable to find this appointment")

        if request.user == appointment.Job.Customer or request.user == appointment.Technician :  
        
            if (any(request.method in i for i in request_method_get)):
                #GET
                
                
                form  = forms.ReviewForm()

                return render(request, "advertisement/review.html",{
                    "reviewform":form,
                    "id":appointment_id,


                })
            if (any(request.method in i for i in request_method_post)):
                form = forms.ReviewForm(request.POST)
                
                if form.is_valid():
    
                    review = form.save(commit=False)
                    if request.user.is_customer:
                        review.Reviewee = appointment.Technician
                        review.Reviewer =  request.user
                    if request.user.is_technician:
                        review.Reviewee = appointment.Job.Customer
                        review.Reviewer =  request.user
                    review.Rating = request.POST["rating"]
                    review.Appointment = appointment
                    review.save()
                    return HttpResponseRedirect(reverse("advertisement:appointment",kwargs={"id":appointment.Job.id}))

        else:
            raise Http404("Unauthorised operation")



def appointment_expiry_check(request):
    
    today = date.today()

    #get all the appointments which is past today
    # change the status to closed
    
    jobresponse_id =Appointment.objects.all().values("Jobresponse")
    jobresponse = JobResponse.objects.filter(id__in = jobresponse_id).filter(Date__lt =today)
    
    advertisement_ids = Appointment.objects.filter(Jobresponse__id__in=jobresponse).values_list('id',flat=True)
    return advertisement_ids

    


