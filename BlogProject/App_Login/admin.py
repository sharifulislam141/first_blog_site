from django.contrib import admin
from . models import UserProfile
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(UserProfile)
