from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username','email','role' 'is_staff', 'is_active',)
    list_filter = ('username','email', 'role','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username','email', 'password','role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','role' 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username','email',)
    ordering = ('username','email',)

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Discussion)
admin.site.register(Notification)

