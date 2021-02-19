from .models import *
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
import datetime
from datetime import date
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

def check_if_field_exist_in_model(argument,model):
    
    '''
    checks if given argument exist in given model
    '''

    model_fields = model._meta.fields
    for field in model_fields:
        if argument in str(field):
            return True
    return False

def check_if_field_isa_model(argument):
    
    '''
    checks if there is a model in given name
    '''
    
    #get all models (from another app as well)
    models = apps.get_models()

    for model in models:
        if argument in str(model):
            return True
    return False


def get_user_role(request):
    """
    Get user role
    """
    role = None
    if request.user.is_customer:
        role = "Customer"
    if request.user.is_technician:
        role ="Technician"
    return role
            
def get_user_obj(user_id):
    """
    return user object
    """
    userObj = get_object_or_404(User,id=user_id)
    return userObj




def get_user_address(user_id):
    
    """
    return user address 
    """
    try:
        userObj = get_user_obj(user_id)
        result = userObj.currentaddress
        return result
    except ObjectDoesNotExist:
        print("Address does not exists") 
        return None





def get_user_profile(user_id):
    """
    get profile of user

    """

    try:
        result = Profile.objects.select_related().get(User = user_id)   
        return result
    except ObjectDoesNotExist:
        print("Profile for this user does not exists") 
        return None


def get_user_work(user_id):
    """
    get work  of user
    """

    try:
        result = Experience.objects.select_related().get(User=user_id)
        return result
    except ObjectDoesNotExist:
        print("Work does not exists") 
        return None


def get_user_education(user_id):
    """
    get education  of user
    """
    try:
        result = Education.objects.select_related().get(User=user_id)
        return result
    except ObjectDoesNotExist:
        print("education does not exists") 
        return None



def update_profile(section,user_instance,newvalue,modelobj=None):
    profile = get_user_profile(user_instance.id)

    if profile:
        #update profile
        if section == "Address" or section == "Experience" or section=="Education":
            function_name = f'{section}.objects.get_instance(user_instance)'
            try:
                modelobj =eval(function_name)
                setattr(profile,section,modelobj)
            except ObjectDoesNotExist:
                print("unable to update profile")
                return False      
        else:
            
            setattr(profile,section,newvalue)
            
        profile.save()  
          
    else:

        #create profile
        if section == "Address" or section == "Experience" or  section=="Education":
            function_name = f'Profile.objects.create_Profile(user_instance,{section}=modelobj)'
        else:
            function_name = f'Profile.objects.create_Profile(user_instance,{section}=newvalue)'

        
        try:
            profileobj =  eval(function_name)   
        except ObjectDoesNotExist:
            print("Unable to create profile instance")
            return False 
        profileobj.save()
    return True   
        
def update_Address(section,user_id,newvalue):
    """
    Update address
    """
    user_instance = get_user_obj(user_id)


    Line1 = newvalue["Address_line_1"]
    Line2 = newvalue["Sublocality_level_2"]
    City = newvalue["Locality"]
    State = newvalue["Administrative_area_level_1"]
    Country = newvalue["Country"]
    Zipcode = newvalue["Postal_code"]

    if section == "Address":

        #update or create new saved address
        save_address_obj,save_address_created = advertisement.models.SavedAddress.objects.update_or_create(User=user_instance,Line1=Line1,Line2=Line2,City=City,State=State,Country=Country,Zipcode=Zipcode)
        
        if Address.objects.get_filter(user_instance):
            #delete previous address
            address_obj_get = get_object_or_404(Address,User=user_id)
            address_obj_get.delete()
        #link to new address
        address_obj,address_created = Address.objects.update_or_create(User= user_instance,Useraddress = save_address_obj)
        return address_obj,True

         
def update_model(section,user_id,newvalue=dict()):
    """
    Update given model which exists in Profile
    """
    # Address in stored in advertisement.SavedAddress 
    # And profile refers to account.Address
    # So when updating or adding address, 
    # Save values to SavedAddress and make reference of SAvedAddress id to Address table of account
    # and from Address table to profile

    #check if user exist in db
    if get_user_obj(user_id):
        user_instance = User.objects.get(id=user_id)
        modelobj = None
        status = False
        #check if section is a model (ex: Experience is a model in account app)
        if check_if_field_isa_model(section):  
            #check if already a value exist 

            attributes = {
            "Experience":'Title= newvalue["Title"],Employment_type = newvalue["Employment_type"],Company = newvalue["Company"],Start_date=newvalue["Start_date"],End_date = newvalue["End_date"]',
            "Education":'School=newvalue["School"],Degree= newvalue["Degree"],Field_of_study = newvalue["Field_of_study"],Start_date=newvalue["Start_date"],End_date = newvalue["End_date"]',
            }
            if section == "Address":
                # call update addres function
                #if user is updating Address, update SavedAddress model.

                modelobj,status =update_Address(section,user_id,newvalue)
            else:
                attr = attributes[section]
                function_name = f'{section}.objects.get_filter(user_instance)'
 
   

                section_instance =eval(function_name)

                if section_instance:
                    #update
                    function_name = f'section_instance.update({attr})'
                    eval(function_name)
            
                else:
                    #create new          
                    operation = f"create_{section}"   
                    function_name = f'{section}.objects.{operation}(user_instance,{attr})' 
                    modelobj =  eval(function_name)
                    modelobj.save()
        if check_if_field_exist_in_model(section,Profile):
            #update profile
            #if section address, make sure we have a postive status to proceed with updating address to profile
            if section=="Address":
                if status:
                    return update_profile(section,user_instance,newvalue,modelobj)
                else:
                    print("Error while editing/adding Address/savedaddress")
                    return False
            else:
                return update_profile(section,user_instance,newvalue,modelobj)
                
        return True

     
    else:
        print("User doesnt exists")



    