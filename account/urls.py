from django.urls import path
from django.urls import include, re_path
from . import views

app_name = 'account'
urlpatterns = [
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path("setting",views.account,name="account"),
    path("discussion", views.discussion, name="discussion"),
    path("notification",views.notification, name="notification"),
    path("job-response/<int:jobrequestid>",views.job_response,name="job_response"),
    path("updateprofile/<str:section>/<str:newvalue>", views.update_account, name="update_account"),
    path("updateprofile/<str:section>", views.update_account, name="update_account"),
    path("profile/<str:username>-<int:id>",views.user_profile,name="user_profile"),

]