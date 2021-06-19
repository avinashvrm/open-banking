from django.db import models
# from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from accounts.models import CustomUser
# Create your models here.

class Bank_Accounts(models.Model):

    CATEGORY_OPTIONS = [
        ('UK','UK'),
        ('India','India')
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=10)
    Account_Holder_Fname = models.CharField(max_length=100, blank = False)
    Account_Holder_Mname = models.CharField(max_length=100, default="")
    Account_Holder_Lname = models.CharField(max_length=100, blank = False)
    phone_regex = RegexValidator(
        regex=r'^(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)', 
        message=("Phone Number is not valid"))
    phone = models.CharField(max_length=14, blank=False, validators=[phone_regex] )
    account_no_regex = RegexValidator(
        regex=r'[0-9]{9,18}', message=("Account Number is not valid"))

    Account_no = models.CharField(max_length=18, blank=False, validators=[account_no_regex], unique= True, db_index=True)

    bank_br = models.TextField(blank=False)
    br_id = models.CharField(max_length=122, blank=False)

    ifsc = models.CharField(max_length=10, blank=False)

    
    #phone_regex = RegexValidator(
    #regex=r'^(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)', message=("Phone Number is not valid"))
    #phone = models.CharField(max_length=14, blank=False )
    owner = models.ForeignKey(to=CustomUser,on_delete= models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    # date = models.DateField()
    
    def __str__(self):
        return self.Account_no