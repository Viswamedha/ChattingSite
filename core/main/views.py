from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import auth

from .forms import CreateUserForm, LoginForm

# Create your views here.
def home(request: WSGIRequest, *args, **kwargs):
    print(type(request))
    context = {'sitename': 'A Little Bit Of Everything'}
    return render(request, template_name = 'main/home.html', context = context)

def login_view(request: WSGIRequest, *args, **kwargs):
    context = {
        'form': LoginForm()
    }
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.is_valid_user()

            if user is not None:  
                auth.login(request, user)

                return HttpResponseRedirect('/')
        
        context.update(
            {
                'error': 'Invalid credentials provided!'
            }
        )
    return render(request, template_name = 'main/login.html', context = context)


def signup_view(request: WSGIRequest, *args, **kwargs):
    context = {
        'form': CreateUserForm(request.POST)
    }

    if request.method == 'POST':

        context

    return render(request, 'main/signup.html', context = context)


def logout_view(request: WSGIRequest, *args, **kwargs):
    if request.user.is_authenticated:
        auth.logout(request)
    return HttpResponseRedirect('/')






