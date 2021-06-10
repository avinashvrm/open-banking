from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  path('', views.Index.as_view(), name = 'index'),
  #path('login/',views.login, name = 'login')
  path('contactUs/', views.contactus2, name="contactus"),

  #Authentication Endpoints
  path('signup/', views.RegisterView.as_view(), name="signup"),
  path('login/', views.LoginViewUser.as_view(redirect_authenticated_user=True), name="login"),
  path('logout/', views.LogoutViewUser.as_view(), name="logout"),
  path('activate/<uidb64>/<token>', views.activate, name='activate'),
  
  #profile endpoints
  path('profile/', views.profile, name = 'profile'),
]