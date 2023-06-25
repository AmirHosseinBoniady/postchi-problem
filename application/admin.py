from django.contrib import admin
from .models import UserProfile, Mission

# Register your models here.

@admin.register(UserProfile) # type:ignore
class UserProfile(admin.ModelAdmin):
    list_display = ['name','email','address']

@admin.register(Mission) # type:ignore
class UserProfile(admin.ModelAdmin):
    list_display = ['title','assigned_to','created_time']