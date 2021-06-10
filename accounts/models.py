from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
#to store data as form obj, and not as string(optional)
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .managers import CustomUserManager
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin #optional -> to be used for AbstractBaseUser

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

class CustomUser(AbstractUser):
  username = None
  email = LowercaseEmailField(_('email address'), unique=True)
  name = models.CharField(max_length=255)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)



  phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
  phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True,unique = True)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  def __str__(self):
    return self.email

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=5)
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex])
    query = models.TextField()

