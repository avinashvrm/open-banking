from django.core.mail.message import EmailMessage
from django.shortcuts import render
from rest_framework import generics, serializers, status, views, permissions
from .serializers import RegisterSerializer, EmailVerificationSerializer, UpdateSerializer, ResetToken, LoginSerializer, OTPVerificationSerializer, ResetPasswordEmailSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser,CustomUserManager
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import random
import string
import smtplib

import jwt

from email.message import EmailMessage
from django.template.loader import get_template
from datetime import datetime, timezone

from .utils import  Util

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token


        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi' +user.username+ 'Use Link bellow to verify \n' + absurl
        data = {'email_body' : email_body,'to_email': user.email, 'email_subject' : 'Verify your email'}
        Util.sent_email(data)
        # html_message = get_template('email.html').render(
        #     {'link': absurl, 'user': user.username, 'email': user.email})


        # msg = EmailMessage()
        # msg['Subject'] = 'Email Verification'
        # msg['From'] = settings.EMAIL_HOST_USER
        # msg['To'] = user.email
        # msg.add_alternative(html_message, subtype='html')
        # server = smtplib.SMTP("tkrs2620@gmail.com", 587)
        # server.starttls()
        # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        # server.send_message(msg)
        # server.quit()

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):

    serializer_class = EmailVerificationSerializer

    #token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,description='Enter Token for Email Verification', type=openapi.TYPE_STRING)

    #@swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        # print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms='HS256')

            user = CustomUser.objects.get(id=payload['user_id'])
            # print(user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return render(request, 'Verified.html', status=status.HTTP_200_OK)
            #return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:

            context = {'message': "Activation Expired"}
            return render(request, 'InvalidToken.html', context)
            #return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            # user.delete()
            context = {'message': "Invalid Token"}
            return render(request, 'InvalidToken.html', context)
            #return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer


    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        #user_data = serializer.data
        # user = User.objects.get(email=user_data['email'])
        # key = random.randint(100000, 999999)
        # user.otp = key
        # time = datetime.now(timezone.utc)
        # user.otp_time = time
        # user.save()
        # msg = EmailMessage()
        # msg['Subject'] = 'Login OTP'
        # msg['From'] = settings.EMAIL_HOST_USER
        # msg['To'] = user.email
        # html_message = get_template('otp.html').render(
        #     {'link': key, 'user': user.username})
        # msg.add_alternative(html_message, subtype='html')
        # server = smtplib.SMTP("mail.fintract.co.uk", 587)
        # server.starttls()
        # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        # server.send_message(msg)
        # server.quit()

        #return Response({"id": user.id}, status=status.HTTP_200_OK)


class VerifyOTP(views.APIView):

    serializer_class = OTPVerificationSerializer
    # permission_classes=(permissions.IsAuthenticated,)
    def post(self, request, pk):
        otp = request.POST.get('otp')
        user = User.objects.get(id=pk)

        # Calculating time difference
        current_time = datetime.now(timezone.utc)
        otp_time = user.otp_time
        diff_min = ((current_time-otp_time).total_seconds())/60

        if diff_min > 10:
            user.otp = 0
            user.save()
            return Response({'error': 'Sesssion Expired, Login again'}, status=status.HTTP_400_BAD_REQUEST)
        if otp == user.otp:
            # user.is_loggedin = True
            user.otp = 0
            user.save()
            context = {"message": 'Successfully Logged In', "id": user.id, "email": user.email, "username": user.username,
                       "country": user.country, "password": user.password, "verification_status": user.is_verified}
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfo(views.APIView):


    def get(self, request, pk):

        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            user = None

        if  not user:
            return Response({'error': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {"id": user.id, "email": user.email, "username": user.username,
                       "country": user.country,"phone":user.phone,"gender":user.gender, "password": user.password, "verification_status": user.is_verified}
            return Response(context, status=status.HTTP_200_OK)
            

class ResetPassword(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        user_mail = request.POST.get('email')
        try:
            user = User.objects.get(email=user_mail)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response({'error': 'Invalid credentials, try again'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'error': 'Account Dissabled, contact admin'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response({'error': 'Email is not Verified, Create a new account'}, status=status.HTTP_400_BAD_REQUEST)

        N = 10
        # using random.choices()
        # generating random strings
        res = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=N))
        password = str(res)
        user.set_password(password)
        user.save()
        msg = EmailMessage()
        msg['Subject'] = 'New Password'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user.email
        html_message = get_template('password.html').render(
            {'link': password, 'user': user.username})
        msg.add_alternative(html_message, subtype='html')
        server = smtplib.SMTP("mail.fintract.co.uk", 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()

        return Response({'password': 'Successfully Changed'}, status=status.HTTP_200_OK)


class NewToken(generics.GenericAPIView):

    serializer_class = ResetToken

    def post(self, request):
        user_mail = request.POST.get('email')
        try:
            user = User.objects.get(email=user_mail)
        except User.DoesNotExist:
            user = None

        if not user:
            return Response({'error': 'Invalid credentials, try again'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'error': 'Account Dissabled, contact admin'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        html_message = get_template('email.html').render(
            {'link': absurl, 'user': user.username, 'email': user.email})

        msg = EmailMessage()
        msg['Subject'] = 'Email Verification'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = user.email
        msg.add_alternative(html_message, subtype='html')
        server = smtplib.SMTP("mail.fintract.co.uk", 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        return Response({'message': 'New token sent'}, status=status.HTTP_201_CREATED)


class Update(generics.GenericAPIView):

    serializer_class = UpdateSerializer

    def put(self, request, pk):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        country = request.POST.get('country')
        gender=request.POST.get('gender')
        phone=request.POST.get('phone')
        user = User.objects.get(id=pk)

        if username != "":
            user.username = username
        if email != "":
            user.email = email
        if country != "":
            user.country = country
        if gender != "":
            user.gender = gender
        if phone != "":
            user.phone = phone
        if password != "":
            # print(len(password))
            if len(password) < 7:
                return Response({'error': "Password too short"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(password)
        user.save()
        return Response({'message': "Updated Successfully"}, status=status.HTTP_201_CREATED)


class DeleteUser(views.APIView):


    def delete(self, request, pk):

        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            user = None

        if  not user:
            return Response({'error': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.delete()
            context = {"msg": "Account Successfully deleted"}
            return Response(context, status=status.HTTP_200_OK)