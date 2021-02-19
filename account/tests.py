from django.test import TestCase,Client
from .models import *
from . import util
# Create your tests here.

class profile(TestCase):
    print("profile")
    def setUp(self):
        print("setup")
        user = User.objects.create_user(username="test",email="test@test.com",password="Test@1234",role="customer")
        address = Address.objects.create(user=user,line1="123 Kite ct",state="FL",country="US")
        payment = Payment.objects.create(user=user)
        profile = Profile.objects.create(user=user, fullname="Alice Mcdonalds",recovery_email="bob@bob.com",address=address,payment=payment)
        



    def test_profile(self):
        print("test_profile")
        user = User.objects.get(username = "test")
        get_profile_details = util.get_profile_data(user_id = user.id)
        self.assertEqual(get_profile_details.count(),1)

    def test_index(self):
        print("test_index")
        c = Client()
        response = c.get(f"/account/profile")
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context["flights"].count(), 3)
