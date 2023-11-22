from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
  
  #creating new model which has one to one attribute of User model with extra custom attributes
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  #additional attributes
  portfolio_site = models.URLField(blank = True, )
  profile_pic = models.ImageField(upload_to = 'profile_pic', blank = True)

  def __str__(self):
    return self.user.username
  