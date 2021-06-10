from django.urls import path
from . import views

urlpatterns = [
    path('reg/', views.reg, name = 'reg'),
    path('account_det/', views.account_det, name = 'account_det'),
    # path('', views.profile, name = 'profile')
]