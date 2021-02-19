from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,Http404,HttpRequest,JsonResponse
from .models import *
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from .forms import *
from django.contrib.auth.decorators import login_required
from . import util,forms
import json
import urllib,sys
from django.db.models import Avg
from advertisement import forms
from django.core.mail import send_mail
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
 
# Create your views here.

def login_view(request):

    """
    1. Login 
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("advertisement:index"))
    else:
        if request.method == "POST":
            # Attempt to signin
            username_or_email = request.POST["username_or_email"]
            password = request.POST["password"]
            role = request.POST["role"]
            
            # authenticate
            user = authenticate(request, username_or_email = username_or_email, password=password,role=role)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("advertisement:index"))
            else:
                return render(request, "account/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "account/login.html")


def logout_view(request):
    """
    1. Logout
    """

    logout(request)
    return HttpResponseRedirect(reverse("advertisement:index"))

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return render (request,"account/success.html")
        
    else:
        return HttpResponse('Activation link is invalid!')

def register(request):

    """
    1. Register
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("advertisement:index"))
    if request.method == "POST":
    
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "account/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username,email,role, password)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account with postIT'
            token =account_activation_token.make_token(user)
            message = render_to_string('account/account_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            to_email = user.email
            #send email with verification link
            send_mail(mail_subject, message,settings.EMAIL_HOST_USER ,[to_email], fail_silently=False)
            return HttpResponse('Please confirm your email address to complete the registration')    
        except IntegrityError as e:
            return render(request, "account/register.html", {
                "message": "Invalid credentials"
            })

        login(request, user,backend ='account.backends.UserBackend')
        return HttpResponseRedirect(reverse("advertisement:index"))
    else:
        return render(request, "account/register.html")

@login_required
def account(request):
    """
    user setting - get all elements from model Profile
    """
    if request.user.is_authenticated:
        user_id = request.user.id
        profile = util.get_user_profile(user_id)
        address = util.get_user_address(user_id)
        if address:
            address = address.Useraddress
        experience = util.get_user_work(user_id)
        education = util.get_user_education(user_id)
       
        return render(request,"account/setting.html",{
            "Profile":profile,
            "Address":address,
            "Experience":experience,
            "Education": education,
            

        })
 
    else:
        return HttpResponseRedirect(reverse("account:login"))

@login_required
def update_account(request,**args):
    """
    update setting
    """
    if args:

        if "section" in args.keys():
            #section exists in args
            section = args['section'].capitalize() 

        # newvalue is dict only when user edits address or experience 
        if "newvalue" in args:
            # new value exists in args
            newvalue = args['newvalue']            
        else:
            
            newvalue=dict()
            if request.method == "post" or request.method == "POST":
                # get form elements
                for key in request.POST.keys():
                    if key != "csrfmiddlewaretoken":     
                        newvalue.update({key.capitalize():request.POST[key]})

            
        try:    
            
            #update Profile
            function_name = f"util.update_model('{section}',{request.user.id},newvalue)"
            if eval(function_name):
                if util.check_if_field_isa_model(section):

                    if section == "Address":
                        addressObj = Address.objects.get(User= User.objects.get(id=request.user.id))
                        result = {"result":list(advertisement.models.SavedAddress.objects.filter(id=addressObj.Useraddress.id).values())}
                    else:
                        function_name = f"{section}.objects.filter(User = User.objects.get(id=request.user.id))"
                        instance = eval(function_name)
                        result = {"result":list(instance.values())}
                    
                else:
                    result = {"result":list(Profile.objects.get_filter(User.objects.get_instance(user_id=request.user.id)).values())}
                response = json.dumps(result,default=str)
                return HttpResponse(response,content_type = "application/json")
            else:
                raise Http404("Unable to update profile")
        except ObjectDoesNotExist:
                print("view object does not exist")


    else:
        print("NO args")

@login_required
def user_profile(request,**args):
    """
    get user profile 
    """

    #get given user id
    profile = util.get_user_profile(args["id"])
    user_info = User.objects.get(id=args["id"])
    obtained_reviews = advertisement.models.Review.objects.filter(Reviewee = user_info)

    return render(request,"account/profile.html",{
        "user_info":user_info,
        "profile":profile,
        "reviews":obtained_reviews,
        "average_reviews":obtained_reviews.aggregate(Avg('Rating')),
        })
    
@login_required
def job_response(request,**args):
    """
    Job application/ job response
    """
    if request.method=="get" or request.method== "GET":
        # get job response  form and send back to client
        form=forms.JobresponseForm()
        return form 
        

        
    if  request.method=="post" or request.method== "POST":
        """ 
        if form is valid then,
            1. save form (creates Job response)
            2. create a Job response instance for technician by customer
            3. Create discussion for technician
        
        else then,
            1. display error 
        """
        #get job request id
        jobrequest_id = args["jobrequestid"]

        #create job instance
        jobrequest_instance = advertisement.models.JobRequest.objects.get(id=jobrequest_id)
        
        # get job instance form job request
        Job_instance = jobrequest_instance.Job


        # get user response
        response = request.POST['btn']




        form=advertisement.forms.JobresponseForm(request.POST)
       
        if form.is_valid():
            job_response = form.save(commit=False)

            try:

                job_response.Customer = request.user
                job_response.Jobrequest = jobrequest_instance
                job_response.Response = response.capitalize()
           
                

            except:
                raise Http404("Unable to create job response")
            # save job response
            job_response.save()
            # job response created
            # update/create discussion
           
            try:
                # create discussion for technician 
                # get technician information from job request
                technician_instance = User.objects.get(id=jobrequest_instance.Technician.id)
                discussion = Discussion.objects.create(User=technician_instance,Jobrequest=jobrequest_instance,Jobresponse=job_response,Checked=False)
                discussion.save()
                request.session['has_checked'] = False
                #created discussion for technician

            except:
                raise Http404("Unable to create discussion for technician")
        

        
            
            
            try:
                # get customer information from job response
                customer_instance = User.objects.get(id=job_response.Customer.id)
                # update discussion for customer with job response
                Discussion.objects.filter(User=customer_instance,Jobrequest=jobrequest_instance).update(Jobresponse = job_response)
            
                #updated notificaiton for customer
                
            except:
                raise Http404("Unable to create discussion for technician")
            
            message="Message sent!"
       
            return HttpResponseRedirect(reverse('account:discussion'))
        else:
            #form not valid
            return HttpResponseRedirect(reverse('account:discussion'))
            



                    





@login_required
def discussion(request,**args):
    """
    Show discussion
    """
    form = ""
    appointments_job_ids =""
    #get discussions by date (latest first)
    discussions = Discussion.objects.filter(User=request.user).order_by('-Updated_date_time')
    
    if request.user.is_customer:
        # if customer had not send a request before
        if Discussion.objects.filter(User=request.user,Jobresponse =None):
            #create job response form
            form = job_response(request)
            #job response not found so getting form
        
    if request.user.is_technician:
        appointments_job_ids = advertisement.models.Appointment.objects.filter(Technician=request.user).values_list('Job',flat=True)
    if request.user.is_customer:
        appointments_job = advertisement.models.Appointment.objects.all().values_list('Job',flat='True')
        appointments_job_ids = advertisement.models.Job.objects.filter(id__in = appointments_job).filter(Customer = request.user).values_list('id',flat=True)
    
    #set all the discussions to be checked
    Discussion.objects.filter(User=request.user).update(Checked=True)
    
    return render(request,"account/discussion.html",{
            'discussions':discussions,
            'job_response_form':form,
            'appointment_job_ids':list(appointments_job_ids),


        })

@login_required
def notification(request,**args):
    """
    notification for user
    """
    #

    notifications = Notification.objects.filter(User=request.user).order_by('-Updated_date_time')

    #set all the discussions to be checked
    Notification.objects.filter(User=request.user).update(Checked=True)

    return render(request,"account/notification.html",{
        "notifications":notifications,


        })





    