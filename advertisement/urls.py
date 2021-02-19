  
from django.urls import path
from . import views

app_name = 'advertisement'
urlpatterns = [
    
    path("", views.index, name="index"),
    path("jobsearch/<str:type>", views.jobsearch, name="jobsearch"),

    path("job-profile/<slug:type>-<int:id>", views.job_profile, name="job_profile"),
    path("job-application/<int:id>", views.job_application, name="job_application"),   

    path("schedule-appointment/<int:id>",views.fix_appointment,name="fix_appointment"),
    path("appointment",views.appointment,name="appointment"),
    path("appointment/<int:id>",views.appointment,name="appointment"),
    path("review/appointment-<int:id>",views.review,name="review"),

    path("<str:username>/", views.user_account, name="user_account"),
    path("<str:username>/<slug:section>", views.user_account, name="user_account"),
    path("<str:username>/section/<slug:section>",views.section, name="section"),
    path("<str:username>/section/<slug:section>/address/", views.current_address, name="current_address"),
    path("<str:username>/section/<slug:section>/savedaddress/", views.saved_address, name="saved_address"),
    path("<str:username>/section/<slug:section>/add-address/", views.add_new_address, name="add_new_address"),
    

]