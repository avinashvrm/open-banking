from django.shortcuts import render
from rest_framework import serializers
from .serializers import AccountSerialzer
#Using Generic Classes to update endpoints
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .models import Bank_Accounts

#For checking owner
from .permissions import IsOwner
# Create your views here.

class AccountsList(ListCreateAPIView):
  serializer_class = AccountSerialzer

  #For  Authentications 
  permission_classes = (permissions.IsAuthenticated,)

  #QuerySet to find user object
  queryset = Bank_Accounts.objects.all()


  #Overide a method, to link logged in user with owner
  def perform_create(self, serializer):
      return serializer.save(owner = self.request.user)


  def get_queryset(self):
      return self.queryset.filter(owner = self.request.user)



class AccountDetailsList(RetrieveUpdateDestroyAPIView):
  serializer_class = AccountSerialzer

  #For  Authentications 
  permission_classes = (permissions.IsAuthenticated,IsOwner,)
  lookup_field = 'id'
  #lookup_value_regex = "[^/]+"
#   lookup_url_kwarg = 'Account_no'


  #QuerySet to find user object
  queryset = Bank_Accounts.objects.all()
  

  #Overide a method, to link logged in user with owner
  def perform_create(self, serializer):
      return serializer.save(owner = self.request.user)


  def get_queryset(self):
      return self.queryset.filter(owner = self.request.user)

