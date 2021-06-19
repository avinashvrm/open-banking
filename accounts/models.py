from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
#to store data as form obj, and not as string(optional)
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
# from .managers import CustomUserManager, BaseUserManager
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin #optional -> to be used for AbstractBaseUser

import random

#For customer id
from datetime import datetime
import shortuuid

from django.contrib.auth.base_user import BaseUserManager

#For Login
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, email, password=None, password2=None):
        """
        Create and save a User with the given email and password.
        """
        if username is None:
            raise TypeError('Users should have a username')

        if email is None:
            raise TypeError('Users should have a Email')

        
        email = self.normalize_email(email)       
        #lowercasing the domain part of email to prevent multiple signups
        user = self.model(username = username,email=email)           #self.normalize_email(email).lower 
        
        #set password for hashing of password
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,email, password=None):
        """
        Create and save a SuperUser with the given email and password.
        """
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user
class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class CustomUser(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=255, unique=True, db_index=True)
  email = LowercaseEmailField(_('email address'), unique=True,  db_index=True)
  customer_id = models.CharField(max_length=60,default = datetime.now().strftime('%Y%m%d') + str(random.randint(1000,9999)), unique= True, db_index=True)
  name = models.CharField(max_length=255,null=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_verified = models.BooleanField(default=False)
  phone = models.CharField(max_length=20, default="",null=True)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  otp = models.CharField(max_length=255,default=0)
  otp_time=models.DateTimeField(auto_now=False,null=False, blank=False,auto_now_add=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  objects = CustomUserManager()


  def __str__(self):
    return self.email
  

  def tokens(self):
      refresh = RefreshToken.for_user(self)
      return {
          'refresh':(refresh),
          'access':str(refresh.access_token)
      }

# class Contact(models.Model):
#     email = models.EmailField()
#     name = models.CharField(max_length=5)
#     phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
#     phone = models.CharField(max_length=255, validators=[phone_regex])
#     query = models.TextField()

