from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your models here.

class User_Reg(models.Model):
    def validate_balance(price):
        if price < 0:
            raise ValidationError("Balance can not be negative.")

    name = models.CharField(max_length=100, blank = False)

    phone_regex = RegexValidator(
        regex=r'^(?:\s+|)((0|(?:(\+|)91))(?:\s|-)*(?:(?:\d(?:\s|-)*\d{9})|(?:\d{2}(?:\s|-)*\d{8})|(?:\d{3}(?:\s|-)*\d{7}))|\d{10})(?:\s+|)', message=("Phone Number is not valid"))
    phone = models.CharField(max_length=14, blank=False, validators=[phone_regex] )

    account_no_regex = RegexValidator(
        regex=r'[0-9]{9,18}', message=("Account Number is not valid"))
    account_no = models.CharField(max_length=18, blank=False, validators=[account_no_regex])

    account_bal = models.DecimalField(decimal_places=2, default=0.00, max_digits=10, blank=False, validators=[validate_balance])
    bank_br = models.TextField(blank=False)
    br_id = models.CharField(max_length=122, blank=False)
    br_add = models.TextField(blank=False)

    ifsc_regex = RegexValidator(
        regex=r'^[A-Za-z]{4}[A-Z0-9a-z]{6}$', message=("IFSC Code is not valid"))
    ifsc = models.CharField(max_length=10, blank=False, validators=[ifsc_regex])

    your_add = models.TextField(blank=False)

    pin_regex = RegexValidator(
        regex=r'^[1-9][0-9]{5}$', message=("Pincode is not valid"))
    pin = models.CharField(max_length=6, blank=False, validators=[pin_regex])

    # date = models.DateField()


    def __str__(self):
        return self.name