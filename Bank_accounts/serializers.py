from django.db.models import fields
from rest_framework import serializers
from .models import Bank_Accounts


class AccountSerialzer(serializers.ModelSerializer):


  class Meta:
    model = Bank_Accounts
    fields = [
      'Account_Holder_Fname','Account_Holder_Mname',
      'Account_Holder_Lname','Account_no','ifsc','id','category','phone','bank_br','br_id']
    lookup_field = 'Account_no'

