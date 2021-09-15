from django.views.generic import View
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.conf import settings



class LoginMixin:
    '''
    Mixin only allows users that are logged in! 
    '''

    login_url = settings.LOGIN_URL or '../../login'

    @method_decorator(login_required(login_url = login_url))
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': 
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST': 
            return self.post(request, *args, **kwargs)


class AdvancedMixin:
    '''
    For handing form data! 
    '''

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': 
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST': 
            return self.post(request, *args, **kwargs)

class AdvancedLoginMixin:
    '''
    Mixin only allows users that are logged in and for forms! 
    '''

    login_url = settings.LOGIN_URL or '../../login'

    @method_decorator(login_required(login_url = login_url))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': 
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST': 
            return self.post(request, *args, **kwargs)


class BaseView(View):

    template_name = None 
    context = dict()

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': 
            return self.get(request, *args, **kwargs)
        elif request.method == 'POST': 
            return self.post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def add_context(self, context = dict(), *args, **kwargs):
        return self.context.update(context)


class AuthorisedView(LoginMixin, BaseView):
    '''
    Allows only logged in users! 
    '''


class FormView(AdvancedMixin, BaseView):
    '''
    View with a form in place with potential redirect! 
    '''
    form_class = None 
    error_message = None 
    success_url = None 

    def get(self, request, *args, **kwargs):
        self.add_context({'form': self.form_class()})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            if self.success_url is not None: 
                return HttpResponseRedirect(self.sucess_url)
            return self.get()
        else:
            self.add_context({'error': self.error_message})
            return self.get()

class AuthorisedFormView(AdvancedLoginMixin, FormView):
    '''
    Forms for users that are logged in! 
    '''


class MultiFormView(View):
    '''
    MultiFormView
    -------------
    template_name  - path to template file 
    context  - variable dictionary passed into the template
    forms  - all forms to be sent + mapped respones (as callables)
    error_message  - message to be shown if post data is invalid
    success_url  - redirect url if form is valid
    login_url  - determined by `LOGIN_URL` variable in settings! Defaults to '../../login' of site!

    Forms - Usage
    {
        Form : {
            'name' : 'context_variable_name',
            'button' : 'post_button_name',
            'action' : callable_function
        }
    }
    '''
    template_name = None
    context = {}
    forms = {}
    error_message = None
    sucess_url = None
    login_url = settings.LOGIN_URL or '../../login'

    # Unloading method for separating request methods
    
    @method_decorator(login_required(login_url=login_url))
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET': return self.get(request, *args, **kwargs)
        elif request.method == 'POST': return self.post(request, *args, **kwargs)

    # Main get method for serving webpage
    def get(self, request, *args, **kwargs):
        self.add_context(request, *args, **kwargs)   
        return render(request, self.template_name, self.context)
    
    # Allows updating context directly
    def add_context(self, request, *args, **kwargs):
        for form in self.forms: 
            self.context[self.forms[form]['name']] = form()
        return self.context

    # Main post method for handing form data
    def post(self, request, *args, **kwargs):
        # Selecting form and passing in post data - Only uses 1 form at a time
        form = None
        for form in self.forms:
            if self.forms[form]['button'] in request.POST:
                form = form 
                break
        if not form:
            return self.get(request, *args, **kwargs)
       
        request_form = form(request.POST, request.FILES or None)
        # status represents validity of form, response is None if status is True
        status, response = self.forms[form]['action'](request, request_form)
        if not status:  
            self.context[response[0]] = response[1]
        elif response:
            
            return HttpResponseRedirect(response)
        return self.get(request, *args, **kwargs)



