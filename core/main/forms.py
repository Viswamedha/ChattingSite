from .models import * 
from django import forms
import datetime 
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class DateInput(forms.DateInput):
    input_type = 'date'


class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = { 
                'placeholder': 'Enter Email Address',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ), 
        label = 'Email Address: '
    )
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter Username',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ), 
        label = 'Username: '
    )
    date_of_birth = forms.DateField(
        widget = DateInput(
            attrs = {
                'type': 'date',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ),
        label = 'Date of birth: '
    )
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter First Name',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ), 
        label = 'First Name: '
    )
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter Last Name',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ), 
        label = 'Last Name: '
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Enter Password',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ), 
        label = 'Password: '
    )
    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Re-enter Password',
                'class': 'form-control',
                'style': 'margin: 0.5rem;',
            }
        ), 
        label = 'Confirm Password: '
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'date_of_birth', 'first_name', 'last_name')
      
    def save(self, commit = True):
        if self.cleaned_data["password"] and self.cleaned_data["confirm_password"] and self.cleaned_data["password"] == self.cleaned_data["confirm_password"]: 
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["confirm_password"])
            if commit: 
                user.save()
            return user
        return None


class EditUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'date_of_birth', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_verified')
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=[str(i) for i in range(int(datetime.datetime.now().year)-70, int(datetime.datetime.now().year)-10)][::-1])  
        }

    def clean_password(self): 
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'placeholder': 'Enter Email Address',
                'id': 'email',
                'class': 'form-control',
                'style': 'margin-bottom: 1rem;',
            }
        ),
        label = 'Email Address: '
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Enter Password Here',
                'id': 'password',
                'class': 'form-control',
                'style': 'margin-bottom: 1rem;',
            }
        ),
        label = 'Password: '
    )

    def is_valid_user(self):
        try: 
            user = User.objects.get(email=self.cleaned_data.get('email'))
        except: 
            user = None
        if user and check_password(self.cleaned_data.get('password'), user.password): 
            return user
        else: 
            return None