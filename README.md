# postIT


Youtube: - https://www.youtube.com/watch?v=joHAiOwrOzw

# Description

PostIt is a web application, developed  with Django framework. In this application, users can register as customer or technician. 

Customers can post a new job and find right technician for their job 
Whereas, Technician can find right job for them !

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


# Why you believe your project satisfies the distinctiveness and complexity requirements
1. Only verified user can use this application. 
    * Email verification is required for any user to use this web application
2. User can login with username/email
3. Show password feature while logging in and registering
4. Server-side password validation using django Password validation and custom Password validation
5. Client-side password validation in javascript
13. Server-side and Client-side Validation of dates to prevent creating jobs, Job request ,job response and appointment with past dates 
14. Customer can post advertisment not just for their location but also for another location
13. Job location/ Address form is autofilled with  Google places api.
6. User can search or find a job using filter such as Job status/ Job type
7. Pagination in index page- shows maximum 5 jobs at a time
7. Technician cannot apply a job that is in pending status or if technician has  already applied for the job. 
8. Notifies user everytime when a discussion is created and when a appointment is created. 
9. Clears the notification count once user has checked the notifications. 
10. A discussion is created when job request and/or job reponse is created 
11. Change job status to Closed and Auto delete of ads/jobs that are 7 days old.
12. Write a brief review and rate on scale of 1-5, about the appointment and experience after appointment is a day old.
13. Almost all of the operations are handled asynchronously using Javascript. 


# What’s contained in each file
This project has two apps, **Account and Advertisment**

## Account 
Account app consists of models, html templates and views that are specifically designed to,
* Create and verify User
* User account setting
* Job Response
* Discussion
* Notification 

### Templates:


#### register.html: 

  1. If user already has an account, then a hyperlink that redirects to login page or create new one by entering details in a form.
  2. In Register form, User can enter their username, email address, password, confirm password and their role such as customer or technician
  3. User can check show password checkbox to see the password as user type. 
  4. Client side password validation, As user type the password. If satisfied changes color to green and red if not.
  5. A submit button to register their account
  6. Display error messages if any.
  
   
  
#### account_verification.html:

  1. On successful register, An email is send to the registered email address with one time link with generated token to confirm email address.
  2. shows message "Please confirm your email address to complete the registration" 
  3. When user verifies their account, redirects to success.html

#### success.html:

 1. Shows success message and a hyperlink to redirect to index.html or to login page
 
#### login.html:
 
 1. If user has to create account, then a hyperlink that redirects to register page or login by entering details in a form.
 2. User can enter username or email address
 3. User can check  show password checkbox to see the password. 
 4. User has to chose a role. Customer/Technician
 5. A submit button to Login.
 6. Display error messages if any.

 
#### setting.html: 
1. User can add/edit their personal and profession details in textarea or forms
2. The details that application collects are:
    * Fullname:
      * client side validation : length minimum 1 maximum 50, contains combination of character,space and numbers
    * Recovery email address:
      * client side validation : validating pattern for email
    * Phone number:
      * client side validation : validating pattern for phone number ,length minimum 9 maximum 15
    * Address: 
      * Form where User can add current address, Address Autofill using google autocomplete. 
      
    ##### Technician specific: 
    * Summary: A brief introduction about technician
      * client side validation : length minimum 1 maximum 50, contains combination of character,space and numbers
    * Designation:
      * client side validation : length minimum 1 maximum 50, contains combination of character,space and numbers
    * License : Technician can check if licenced. 
    * Experience(years): Technician can enter the total years of exeperience
      * client side validation : pattern validation to make sure they are numbers
    * Organisation: 
      * Form where Technician can enter  current organisation's Title,Employment type,Company name ,Start and End date
      * Date validation (can not given older dates and End date older than start date)
    * Education: 
      * Form where Technician can enter  Education details such as School,Degree,Field of Study,Start and End date
      * Date validation (can not given older dates and End date older than start date)
3.  User can edit all of the above details asynchronously using javascript, Without page reload.

#### profile.html:
1. Display user profile - Fullname,Overall rating on scale of 5 and Total obtained Reviews count
2. Contact information: Phone number (if provided) and email address.
   #### Technician:
   * Designation and company name(if provided)
   * Summary (if provided)
   * Total Experience(if provided)
   * Licence
   * Education and employment details in card (if provided)
   


#### discussion.html:
Separate block for each Job discussion. 
Each discussion has,
1. Job information : such as Date and time and a hyperlink to job-profile.html
    ##### For Customer:
    2. Job request received
         * On click collapse Job request- Technician,Quote,Date & Time and Budget
    3. Give response /See response sent:
      * Give response:
         * Shows job response model form (user can enter message, Date & Time and Budget)
         * User can accept or reject offer
      * See response sent:
         * On click collapse Job response received block
         * Shows Technician,Quote,Date & Time and Budget
         * Status: appointment created or if pending/reject.
       
   ##### For Technician:
   4. Job request sent
      * On click collapse Job request details- Technician,Quote,Date & Time and Budget
   4. See response received:
      1. Show details of job response
      2. if Customer accepts the offers, Schedule appointment button
      3. if Customer rejected the offer, Shows "Sorry! I am looking for something different"
   5. Schedule appointment:
      1. Schedules appointments and modal is displayed with appointment details and hyper link that takes to appointment.html
      2. if already created, see appointment button takes to appointment page
  
#### notification.html:
   1. creates notification when appointment is created for user
   
### Static:
1. authenticate.js:
   * Register password validation
   * Show password
2. discussion.js:
   * Schedule appointment
3. function.js 
   * setup_google_autocomplete (function is called everytime address form is displayed)
   * Profile/settings validations
   * add/edit Profile components, display textarea/forms in setting.html 
4. google.js
   * Google autocomplete file
5. profile.js
   * Setup html for edit/add setting components
   * save edited form
   * Asynchronus calls to server with updated values
   * Stack to remember previous section click
6. util.js
   * Main file used by all javascript files.
   * Has functions to create tags, forms, button, textarea etc
   
### static/account/
1. style.css: CSS Stylings

### views.py
1. views for login,email verification,register, update setting, setting, user_profile, post/GET job response,create discussion, notification
2. Every time user checkes notification/discussion. Has checked attribute is set to True

### validators.py:
1. validate password such that password has minimum 3 digits 
### util.py
1. Redudant db queries are written in functions.  
2. main functions to update model Profile and its foreign keys. 
### tokens.py 
1. File that create token for email verification
### forms.py
1. Model Forms
### managers.py 
1. create user/ super user 
2. model create and get, filter from model
### backends.py
1. Authenticate user login with username/email address and user role
### tests.py
1. Sample test case
### models.py
1. Django Models - User, Address, Experience, Education, Profile, Discussion, Notification

## Advertisment 
Advertisment exclusively design for job/advertisment. 
### Templates:
1. ad.html:
   * Set intial category as new-job in javascript
   * Section is displayed asynchronously with javascript
   * Has several sections:
   #### Customer
   1. Post a new job:
      * Shows modelForm -Job 
      * User enter job details
      * Job location can be user's current address(which was given in setting)  or can give another address
      * if user selects current address, Current address is displayed in card or link to add new address
      * if user selects another address, All other Saved address by this user is shown also a card with link to add new address
      * Address form wuth Google places autocomplete, if adding new address.
      * Address can be added asynchronously without page reload
   2. Ads:
      * Shows User posted Advertisements
   #### Common for both users
   3. Appointments:
       * Shows user scheduled appointments
   4. Reviews:
       * Shows obtained reviews
   5. Given Reviews:
       * Shows given reviews 
      
2. appointment.html:
   1. Shows appointment information like ,
      * Job hyperlink, scheduled date & time,budget, message if any, Locations ,technician and customer informations
   2. Review button is displayed if scheduled date and time is one older than today.
   3. Already reviewed button is displayed if already user has reviewed
   4. Only appointment related customer/Technician can access this page
   
3. index.html:
   1. Shows all the ads in cards with hyperlink that takes to job profile
   2. Job may be displayed based on filter Status: Open/Pending and Job type: Electrical,Plumbing and Handyman
   3. Job is created asynchronously when displayed using filter. 
   4. Pagination- No more than 5 jobs are displayed
   
4. job-application.html:
   1. Model form is displayed- Jobrequest form
   2. shows messsage- request sent/ request sent already
   
5. job-profile.html:
   1. Shows job details such as job type,location, date and time, posted customer, description and budget
      #### Technician
      1. Apply button if technician had not applied yet, redirects to job-application
      2. if already applied, Job applied already -see request (redirects to discussion.html)
      3. if job is pending, disabled the apply button with displaying job status
      
6. review.html:
   1. Review form to write comments and star rating from 1-5.
   
### Static:
1. ad.js:
   * used by ad.html 
   * display forms, Reviews, Fetch from server, 
   * Autosave new-job form contents to local storage 
   * add address 
   * show address
   * set selected address
2. index.js :
   * used by index.html 
   * Server fetch on filter select.
   * create card based on result

### notification_custom_processor.py 
   * This file is called everytime the application is loaded
   * It helps to counts number of notification and discussion that are unchecked by user, which can be used to notify user
   * finds all the job that are 7 days old, change status of job and delete those jobs.
   * Retriving Google key  from environment variable  

### managers.py
1. Managers for model
2. Creating objects,filter and get

### forms.py 
1. custom Model forms
2. models that have date field, shows and accepts only future dates


### views.py
1. paginate
2. index (for index.html)- clears job stack
3. job_profile- checks if user have send request already and redirects to job-profile.html
4. jobsearch - jobsearch stack
      * appends filter to the stacks as user selects the filter
      * removes the filter from the stack as user selects once again
5.job_application: 
      * GET/POST job request Model form
      * create discussion for customer
6. user_account:
      * default is new-job
      * GET/POST new job
7. section:
      * httpresponse with selected selected seleted data
8. current_address:
      * get current address for ad.html new-job form
9. saved_address:
      * Get all saved address from dn to ad.html
10. add new address:
      * Add new address current/another address
11. fix_appointment:
      * Schedule appointment if not already appointment is created
      * create notification for customer
12. appointment:
      * get appointment details for given job id
13. retreive_appointment:
      * gets all appointments of user
14. review:
      * GET/POST review form
15. appointment_expiry_check:
      * Check if appointment date is older than today.
   

 ### Layout.html
 1. Base layout for all templates
 2. Display notifications and discussion counts in navigation
 
   
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

   
# Models:
1. User(username,email,role,is_customer,is_technician)
   * Primary key: Id
2. SavedAddress(User,Line1,Line2,City,State,Country,Zipcode)
   * Primary key: Id
   * Foreign key:User
2. Address(User, Useraddress)
   * Primary key: Id
   * Foreign key:User,Useraddress(SavedAddress)
3. Experience(User,Title,Employment_type,Company,Start_date,End_date)
   * Primary key: Id
   * Foreign key:User(User)
4. Education(User,School,Degree,Field_of_study,Start_date,End_date)
   * Primary key: Id
   * Foreign key:User(User)
5. Profile(User,Fullname,Recovery_email,Address,Phone_number,Designation,About,Licence,Totalexperience,Education,Experience)
   * Primary key: Id
   * Foreign key:User(User),Address(Address),Education(Education),Experience(Experience)
6. Job(Customer,Job_type,Description,Location,Date,Time,Priority,Amount,Currency,Technician_experience_preference,Licence,Status)
   * Primary key: Id
   * Foreign key:Customer(User),Location(SavedAddress)
7. JobRequest(Technician,Job,Quote,Date,Time,Amount,Currency)
   * Primary key: Id
   * Foreign key:Technician(User),Job(Job)
8. JobResponse(Customer,Jobrequest,Message,Response,Date,Time,Amount,Currency)
   * Primary key: Id
   * Foreign key:Customer(User),Jobrequest(JobRequest)
9. Appointment(Job,Technician,Jobresponse)
   * Primary key: Id
   * Foreign key: Job(Job),Technician,(User),Jobresponse(JobResponse)
10.Review(Reviewer,Reviewee,Comment,Rating,Appointment)
   * Primary key: Id
   * Foreign key:Reviewer(User),Reviewee(User),Appointment(Appointment)
6. Notification(User,Message,Appointment,Job,Checked,Updated_date_time)
   * Primary key: Id
   * Foreign key:User(User),Appointment(Appointment),Job(Job),Experience(Experience)

# Additional information:
   1. This application uses google api - Maps JavaScript API and Places API. 
   For more information - https://developers.google.com/maps/documentation/javascript/places-autocomplete
   2. Added models.png image which was created using 

### Author:
------------
NAIR SAARIKA BHASI
         
   
      



      
         
     
 







