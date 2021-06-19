from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.



admin.site.register(CustomUser)
