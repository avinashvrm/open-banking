from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields

from .models import CustomUser,Contact

from django import forms
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)



class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'email',
            'phone',
            'query',
            'name'
        ]




class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'email',
            'name',
            'phone',
            'password1',
            'password2',
        ]


class SendOtpBasicForm(forms.Form):
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = forms.CharField(max_length=255, validators=[phone_regex])

    class Meta:
        fields = [
            'phone',
        ]

class VerifyOtpBasicForm(forms.Form):
    otp_regex = RegexValidator( regex = r'^\d{4}$',message = "otp should be in six digits")
    otp = forms.CharField(max_length=6, validators=[otp_regex])
