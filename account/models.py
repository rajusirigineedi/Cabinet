from django.db import models
from django.contrib.auth.models import User

class AppUser(models.Model):
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    phone_number = models.IntegerField(default='0')
    profile_pic = models.ImageField(upload_to='account/images/',null=True, blank=True)
    resume_link = models.CharField(max_length=255,null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
