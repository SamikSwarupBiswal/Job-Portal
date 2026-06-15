from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Job, Application

# Register your models here.
#can see and edit the 'role' field in the admin panel
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

# Registering models to the Admin Site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Application)
