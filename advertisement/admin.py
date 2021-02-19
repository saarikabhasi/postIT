from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(SavedAddress)
admin.site.register(Job)
admin.site.register(JobRequest)
admin.site.register(JobResponse)
admin.site.register(Appointment)
admin.site.register(Review)