# postIT


Youtube: - https://www.youtube.com/watch?v=joHAiOwrOzw

# Description

PostIT is web application to find Handyman, Electrician or Plumber. Developed with Django framework. 


## Work flow: 
There are two types of users: **Customer and Technician**. 

1. Customer creates job/ad with a short description, specifying any requirements such as the budget, Date and time, Location and Technician preference. 
2. Once an ad is created, Technican may apply for the job once, by filling out job request form.
3. Customer may receive multiple job requests from different technicians for an ad and a Technician may apply for multiple ads. 
3. On recieving job request from Technician, Customer may accept/reject the job request by  filling out Job response form with details once again.
4. If customer accepted the offer, Technician may schedule an appointment or an reject message is displayed
5. Customers and Technicians may communicate within the application.
6. Once job's appointment is compeleted Users can give their feedback and ratings.
7. Auto delete ads/jobs which has an appointment scheduled and is 7 days older than current date.


## Distinctiveness and complexities
1. Only verified user can use this application. 
    * Email verification is required for any user to use this web application
2. User can login with username/email
3. Show password feature while logging in and registering
4. Server-side password validation using django Password validation and custom Password validation
5. Client-side password validation in javascript
13. Server-side and Client-side Validation of dates to prevent creating jobs, Job request ,Job response and appointment with past dates 
14. Customer can post advertisment not just for their location but also for another location
13. Job location/ Address form is autofilled with  Google Places Api.
6. User can search or find a job using filter such as Job status/ Job type
7. Pagination in index page- shows maximum 5 jobs at a time
7. Technician cannot apply a job that is in pending status or if technician has  already applied for the job. 
8. Notifies user everytime when a discussion is created and when a appointment is created. 
9. Clears the notification count once user has checked the notifications. 
10. A discussion is created when job request and/or job reponse is created 
11. Change job status to Closed and Auto delete of ads/jobs that are 7 days old.
12. Write a brief review and rate on scale of 1-5, about the appointment and experience after appointment is a day old.
13. Almost all of the operations are handled asynchronously using Javascript. 


  
   
 
   
# How to run this application:
```
   # clone repository
      git clone https://github.com/saarikabhasi/
      
    # Create a virtualenv(optional)
      python3 -m venv venv  
     
      
    # Install all dependencies
       pip install -r requirements.txt
       
    # ENV Variables in venv/bin/activate
      export EMAIL = Your gmail address
      export PASSWORD = Your gmail address's password
      export GOOGLE_KEY = You google api key
      export SECRET_KEY= Your django secret key 
      
    # Activate the virtualenv
      source venv/bin/activate or .venv/bin/activate
    
    # Run application
     ./manage.py runserver or python manage.py runserver
     
     # UML Class diagram
      pip install django-extensions.
      pip install pyparsing pydot
      pip install graphviz 
      added django_extensions to INSTALLED_APPS in settings.py
      python manage.py graph_models account advertisement -o models.png
      
      For more information:
      https://django-extensions.readthedocs.io/en/latest/graph_models.html
     
```

  


# Additional information:
   1. This application uses google api - Maps JavaScript API and Places API. 
   For more information - https://developers.google.com/maps/documentation/javascript/places-autocomplete
  

# Author
NAIR SAARIKA BHASI
         
   
      



      
         
     
 







