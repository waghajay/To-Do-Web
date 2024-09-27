from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_images/",blank=False,null=False)
    auth_token = models.CharField(max_length=100,default="",null=True,blank=True)
    is_varified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"User:- {self.user} ----- Full Name:- {self.user.first_name} {self.user.last_name} ----- Email:- {self.user.email}"
