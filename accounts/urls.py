from django.contrib import admin
from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView


from django.contrib.auth import views as auth_views

#For Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Open Banking Api",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.fintract.co.uk/openbanking/policies/terms/",
      contact=openapi.Contact(email="mail.fintract.co.uk"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

#Urls start here

urlpatterns = [
  path('register/',RegisterView.as_view(),name = "register"),
  #path('email-verify/',VerifyEmail.as_view(),name = "email-verify"),
  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  #path('login/',LoginView.as_view(),name = "Login"),
]

