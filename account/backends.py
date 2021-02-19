from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User
# from account.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class UserBackend(ModelBackend):

    def authenticate(self, request,  username_or_email = None, password = None,**kwargs):


        try:
            if kwargs['role'] == 'is_customer':
                user = UserModel.objects.get( Q(is_customer=True) & Q(username=username_or_email) | Q(email=username_or_email))
                if user.check_password(password):
                    return user
            if kwargs['role'] == 'is_technician':
                user = UserModel.objects.get( Q(is_technician=True) & Q(username=username_or_email) | Q(email=username_or_email))
                if user.check_password(password):
                    return user

        except UserModel.DoesNotExist:
                print("User does not exist")
        