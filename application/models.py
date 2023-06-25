from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager


class UserProfile(AbstractBaseUser):
    #user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username=None
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    is_in_mission = models.BooleanField(default=False)
    current_position_x = models.IntegerField(blank=True,null=True, default=0)
    current_position_y = models.IntegerField(blank=True,null=True, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email','password']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    objects = CustomUserManager()

# class UserProfileDraft(models.Model):
#     #user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)
#     current_position_x = models.IntegerField(blank=True,null=True)
#     current_position_y = models.IntegerField(blank=True,null=True)





class Mission(models.Model):
    title = models.CharField(max_length=100, unique=True)
    start_point_x = models.IntegerField()
    start_point_y = models.IntegerField()
    end_point_x = models.IntegerField()
    end_point_y = models.IntegerField()
    assigned_to = models.ForeignKey(to=UserProfile, related_name='missions',on_delete=models.SET_NULL,blank=True,null=True)
    is_finished = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    
    def __str__(self) -> str:
        return str(self.title)

class Point(models.Model):
    start_point_x = models.IntegerField()
    start_point_y = models.IntegerField()
