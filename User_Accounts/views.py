from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User_Reg
from .forms import UserForm
from datetime import date

# Create your views here.

# @login_required(login_url='login/')
def reg(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.success(
                request, ('There was an error in your form. Please try again...'))
            return render(request, 'reg.html', {})
        messages.success(request, ('Registration has been done successfully!'))

    return render(request, 'reg.html')

# @login_required(login_url='login/')
def account_det(request):
    all_reg = User_Reg.objects.all()
    found = []
    if request.method == "POST":

        name = request.POST.get('find')
        choice = request.POST.get('find_')

        if(choice == "Choose Below" or name == ""):
            messages.success(
                request, ('Please pick a valid option and enter something in the search box!'))
            return render(request, 'account_det.html')

        if (choice == "1"):
            found = all_reg.filter(

                account_no__icontains=name
            )
        elif (choice == "2"):
            found = all_reg.filter(

                bank_br__icontains=name
            )
        elif (choice == "3"):
            found = all_reg.filter(

                br_id__icontains=name
            )
        elif (choice == "4"):
            found = all_reg.filter(

                ifsc__icontains=name
            )
        elif (choice == "5"):
            found = all_reg.filter(

                name__icontains=name
            )

    return render(request, 'account_det.html', {'list': found})
