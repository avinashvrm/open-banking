from django.urls import path
from . import views

urlpatterns = [
     path('',views.AccountsList.as_view(), name = 'Accounts'),
     path('<int:id>',views.AccountDetailsList.as_view(), name = 'AccountDetails'),
]
