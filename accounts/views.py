from django.shortcuts import render, HttpResponse, redirect

from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from .forms import RegistrationForm, ContactUsForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from .models import CustomUser

from openbanking import settings
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.


class Index(TemplateView):
    template_name = 'accounts/index.html'


def contactus2(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():  # clean_data
            if len(form.cleaned_data.get('query')) > 10:
                form.add_error('query', 'Query length is not right')
                return render(request, 'accounts/contactUs.html', {'form': form})
            form.save()
            return HttpResponse("Thank You")
        else:
            if len(form.cleaned_data.get('query')) > 10:
                #form.add_error('query', 'Query length is not right')
                form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
            return render(request, 'accounts/contactUs.html', {'form': form})
    return render(request, 'accounts/contactUs.html', {'form': ContactUsForm})


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    # def post(self, request, *args, **kwargs):
    #     #form = RegistrationForm(request.POST)
    #     response = super().post(request, *args, **kwargs)
    #     user_email = request.POST.get('email')

    #     if response.status_code == 200:
    #         user = CustomUser.objects.get(email = user_email)
    #         user.is_active = False
    #         user.save()
    #         current_site = get_current_site(request)
    #         mail_subject = 'Activate your account.'
    #         message = render_to_string('accounts/registration/acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token':account_activation_token.make_token(user),
    #         })
    #         print(message)
    #         to_email = user_email
    #         #form = RegistrationForm(request.POST)   # here we are again calling all its validations
    #         form = self.get_form()
    #         try:
    #             send_mail(
    #                 subject=mail_subject,
    #                 message=message,
    #             from_email=settings.EMAIL_HOST_USER,
    #             recipient_list= [to_email],
    #             fail_silently=False,    # if it fails due to some error or email id then it get silenced without affecting others
    #         )
    #         messages.success(request, "link has been sent to your email id. please check your inbox and if its not there check your spam as well.")
    #         return self.render_to_response({'form':form})
    #     except:
    #         form.add_error('', 'Error Occured In Sending Mail, Try Again')
    #         messages.error(request, "Error Occured In Sending Mail, Try Again")
    #         return self.render_to_response({'form':form})
    # else:
    #     return response


class LoginViewUser(LoginView):
    template_name = "accounts/login.html"

class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('index')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully Logged In")
        return redirect(reverse_lazy('index'))
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')

# @login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('/login')

# @login_required(login_url='login/')
def profile(request):
    # return render(request, 'accounts/profile.html')
    return render(request, 'account_det.html')
