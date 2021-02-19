from django.core.exceptions import ValidationError
from django.db import models
from account.models import *

class SavedAddressManager(models.Manager):

    def create_SavedAddress(self,User,Line1,City,State,Country,Zipcode,Line2=None):

        addressObj = self.create(User=User,Line1=Line1, Line2=Line2, City=City,State=State,Country=Country,Zipcode=Zipcode)
        return addressObj

    def get_filter(self,User):
        print("get_filter")
        return self.filter(User=User)

    def get_instance(self,User):
        print("get_instance")
        return self.get(User=User)

    def get_location_instance(self,id):
        print("get_location_instance")
        return self.get(id=id)

class JobManager(models.Manager):


    def create_Job(self,User,Job_type,Description,Location,Date,Time,Priority,Amount,Currency,Technician_experience_preference,Licence,Status):
        print("create job")
        jobObj = self.create(Customer=User,Job_type=Job_type, Description=Description, Location=Location,Date=Date,Time=Time,Priority=Priority,Amount=Amount,Currency=Currency,Technician_experience_preference=Technician_experience_preference,Licence=Licence,Status=Status)
        return jobObj

    def get_filter(self,User):
        print("get_filter")
        return self.filter(Customer=User)

    def get_instance(self,User):
        print("get_instance",User)
        return self.get(Customer=User)



class AdManager(models.Manager):


    def get_filter(self,User):
        print("get_filter")
        return self.filter(User=User)

    def get_instance(self,User):
        print("get_instance")
        return self.get(User=User)