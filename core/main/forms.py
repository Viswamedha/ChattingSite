from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from datetime import datetime
from .models import User

class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = { 
                'placeholder': 'Enter Email Address'
            }
        ), 
        label = 'Email Address: '
    )
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter Username'
            }
        ), 
        label = 'Username: '
    )
    date_of_birth = forms.DateField(
        widget = forms.DateInput(
            attrs = {
                'type': 'date'
            }
        ),
        label = 'Date of birth: '
    )
    first_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter First Name'
            }
        ), 
        label = 'First Name: '
    )
    last_name = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'placeholder': 'Enter Last Name'
            }
        ), 
        label = 'Last Name: '
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Enter Password'
            }
        ), 
        label = 'Password: '
    )
    confirm_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Re-enter Password'
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
            'date_of_birth': forms.SelectDateWidget(years=[str(i) for i in range(int(datetime.now().year)-70, int(datetime.now().year)-10)][::-1])  
        }

    def clean_password(self): 
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'placeholder': 'Enter Email Address',
                'id': 'email'
            }
        ),
        label = 'Email Address: '
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                'placeholder': 'Enter Password Here',
                'id': 'password'
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


class ResetRequestForm(forms.Form):
    email = forms.EmailField()
    def validate(self):
        try:
            user = User.objects.get(email=self.cleaned_data["email"])
            if user: 
                if user.is_verified:
                    return user
            return False
        except Exception as e: 
            print(e)
            return False


class ResetPasswordForm(forms.ModelForm):
    password_1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ()
    
    def validate(self):
        if self.cleaned_data['password_1'] == self.cleaned_data['password_2']:
            self.instance.set_password(self.cleaned_data['password_1'])
            self.instance.save()
            return True
        return False







