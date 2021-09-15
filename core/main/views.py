from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.conf import settings
from .utils import *
from .forms import *
#from ratelimit.decorators import ratelimit
import base64



class LoginView(FormView):

    form_class = LoginForm
    success_url = settings.LOGIN_REDIRECT_URL or '../dashboard/'
    error_message = 'User not found / Password incorrect!'
    next = ""

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('../../../')
        if 'next' in request.GET: 
            self.next = request.GET['next']
        return render(request, self.template_name, {'form': self.form_class(), 'errors': '', 'next': self.next})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        self.next = request.GET.get('next', '/')
        if self.next == "/": self.next = self.success_url
        if form.is_valid():
            user = form.is_valid_user()
            if user: 
                if not user.is_verified:
                    return HttpResponseRedirect('../verify/invalid/')
                auth.login(request, user)
                return HttpResponseRedirect(self.next)
            return render(request, self.template_name, {'form': self.form_class(), 'error': self.error_message})
        return render(request, self.template_name, {'form': self.form_class(), 'error': ''})




class LogoutView(View):
    '''
    Main Logout View
    ----------------
    success_url  - determined by `LOGOUT_REDIRECT_URL` variable in settings! Defaults to root of site!
    auth.logout  - django default logout processing, logs out user and deletes session key!
    '''
    success_url = settings.LOGOUT_REDIRECT_URL or '../../'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(self.success_url)


class SignupView(FormView):
    template_name = 'main/auth/signup.html'
    form_class = CreateUserForm
    success_url = '../verify/check-your-mail/'
    error_message = 'User creation failed! Please try again! '

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('../../../')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                user.save()
                user.verify_user()
                return HttpResponseRedirect(self.success_url)
        print(form.errors.as_json())
        return render(request, self.template_name, {'form': self.form_class(request.POST), 'error': 'User creation failed! Please try again! '})


class VerificationView(BaseView):
    
    def get(self,  request, id, token, *args, **kwargs):
        for i in range(0,3):
            try:
                token = base64.b64decode(token.encode('utf-8')).decode()
                break
            except: 
                token += '='
        for i in range(0,3):
            try:
                id = base64.b64decode(id.encode('utf-8')).decode()
                break
            except: 
                id += '='
        try:
            user = User.objects.get(verification_token=token, tag=id)
        except:
            return HttpResponseRedirect('../../../404') 
        user.is_verified = True
        user.verification_token = None 
        user.save()
        return HttpResponseRedirect('../../../login')


class ForgotPasswordRequestView(FormView):
    template_name = 'main/auth/reset-forgot-password.html'
    form_class = ResetRequestForm
    success_url = '../forgot-password/check-your-mail/'
    error_message = 'Account either does not exist or is not verified!'
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.validate()
            if user:
                user.forgot_password()
                return HttpResponseRedirect(self.success_url)
        self.context['error'] = self.error_message
        return self.get(request, *args, **kwargs)


class ForgotPasswordProcessingView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': return self.get(request, *args, **kwargs)
        elif request.method == 'POST': return self.get(request, *args, **kwargs)

    def get(self,  request, id, token, *args, **kwargs):
        for i in range(0,3):
            try:
                token = base64.b64decode(token.encode('utf-8')).decode()
                break
            except: 
                token += '='
        for i in range(0,3):
            try:
                id = base64.b64decode(id.encode('utf-8')).decode()
                break
            except: 
                id += '='
        try:
            user = User.objects.get(reset_password_token=token, tag=id)
        except:
            return HttpResponseRedirect('../../404') # change to 404 page
        if not user.time_left():
            return HttpResponseRedirect('../../404')
        instance = user.forgot_password_instance()
        return HttpResponseRedirect(f'../../../reset/{instance}')


class ForgotPasswordChangeView(FormView):
    template_name = 'main/auth/password-reset-valid.html'
    form_class = ResetPasswordForm
    error_message = 'Passwords do not match! '

    def get(self, request, instance=None, *args, **kwargs):
        try:
            user = User.objects.get(reset_instance_token=instance)
        except:
            return HttpResponseRedirect('../../../404/')
        if user:
            return render(request, self.template_name, {'user': user, 'form': self.form_class()})
    
    def post(self, request, instance=None, *args, **kwargs):
        user = User.objects.get(reset_instance_token=instance)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            if form.validate():
                user.reset_forgot_password()
                return HttpResponseRedirect('../../../login/')

        return render(request, self.template_name, {'user': user, 'form': self.form_class(), 'error': self.error_message})










