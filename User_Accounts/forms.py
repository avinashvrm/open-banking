from django.forms import ModelForm
from django import forms
from .models import User_Reg
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class UserForm(ModelForm):
    class Meta:
        model = User_Reg
        fields = '__all__'