from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, username, email, password,role, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not role:
            raise ValueError("Role is required")
        email = self.normalize_email(email)

             
        if role == 'is_technician':
            user = self.model(username=username,email=email,is_technician='True', **extra_fields)
        
        if role == 'is_customer':
            user = self.model(username=username,email=email, is_customer="True", **extra_fields)

        if role == 'admin':
            user = self.model(username=username,email=email, **extra_fields)
        try:
            validate_password(password,user)
        except ValidationError as e:
            #return ValueError(e)
            raise ValidationError({"password": e })
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_user(self, username, email, role,password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password,role, **extra_fields)

    def create_superuser(self, username, email, password,role=None,**extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        

        return self._create_user(username,email, password,role="admin", **extra_fields)
    
    def get_filter(self,user_id):
        return self.filter(id=user_id)

    def get_instance(self,user_id):
        return self.get(id=user_id)

    def user_address(self,User):
        inst = self.get_instance(User)
        return inst.currentaddress
        
class ProfileManager(models.Manager):

    def create_Profile(self, User,Fullname=None,Recovery_email=None,Address=None,Phone_number=None,Designation=None,About=None,Licence=None,Totalexperience=None,Education=None,Experience=None):
        if Licence == None:
            Licence = False 
        profile = self.create(User=User,Fullname = Fullname, Recovery_email=Recovery_email,Address=Address,Phone_number=None,Designation=None,About=About,Licence=Licence,Totalexperience=Totalexperience,Education=Education,Experience=Experience)
        return profile

    def get_filter(self,User):
        return self.filter(User=User)

    def get_instance(self,User):
        return self.get(User=User)
        
    

class AddressManager(models.Manager):

    def create_Address(self, User,Useraddress):
        addressObj = self.create(User=User,Useraddress=Useraddress)
        return addressObj

    def get_filter(self,User):
        return self.filter(User=User)

    def get_instance(self,User):
        return self.get(User=User)

class ExperienceManager(models.Manager):
    def create_Experience(self, User,Title,Employment_type,Company,Start_date,End_date):
        experienceobj = self.create(User=User, Title=Title,Employment_type =Employment_type,Company=Company, Start_date=Start_date,End_date=End_date)
        return experienceobj

    def get_filter(self,User):
        return self.filter(User=User)

    def get_instance(self,User):
        return self.get(User=User)

class EducationManager(models.Manager):

    def create_Education(self, User,School,Degree,Field_of_study,Start_date,End_date):

        educationObj = self.create(User=User,School=School, Degree=Degree,Field_of_study=Field_of_study, Start_date=Start_date, End_date=End_date)
        return educationObj

    def get_filter(self,User):

        return self.filter(User=User)
    def get_instance(self,User):

        return self.get(User=User)