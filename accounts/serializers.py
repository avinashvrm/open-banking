from rest_framework import serializers
from .models import CustomUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        # country=attrs.get('country','')

        ok = False
        if "@gmail.com" in email:
            ok = True  # any check you need
        elif "@rediff.com" in email:
            ok = True
        elif "@yahoo.com" in email:
            ok = True
        elif "@fintract.co.uk" in email:
            ok = True

        if ok != True:
            raise serializers.ValidationError(
                "Enter Valid Gmail address (gmail,rediff,yahoo,fintract)")

        if password != password2:
            raise serializers.ValidationError("Passwords should be same")
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only = True)
    customer_id = serializers.CharField(max_length=255, min_length=3, read_only = True)
    tokens = serializers.CharField(max_length=80, min_length=3, read_only = True)
    #username = serializers.CharField(max_length=225, min_length=3)

    class Meta:
        model = CustomUser
        fields = ['email', 'password','username','customer_id','tokens']
        #fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        return {
            'email' : user.email,
            'username' : user.username,
            'customer_id' : user.customer_id,
            'tokens' : user.tokens()

        }
        return super().validate(attrs)


class OTPVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['otp']


class ResetPasswordEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = CustomUser
        fields = ['email']


class ResetToken(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = CustomUser
        fields = ['email']


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password',
                  'country', 'phone', 'gender']