from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
import uuid, base64, random


class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, date_of_birth, password=None):
        # Checking if an email is present! 
        if not email: 
            raise ValueError('Users must have an email address')
        
        # Creating a model object
        user = self.model(
            email = self.normalize_email(email), 
            username = username, 
            first_name = first_name, 
            last_name = last_name, 
            date_of_birth = date_of_birth
        )

        # Assigning a password
        user.set_password(password)
        
        # Comitting changes to database
        user.save(using = self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, date_of_birth, password=None):
        # Fetching a regular user object
        user = self.create_user(email, username, first_name, last_name, date_of_birth, password)
        
        # Adding in admin permissions
        user.is_admin = True 
        
        # Re comitting changes
        user.save(using=self._db)

        return user





class User(AbstractBaseUser):

    # Reference Indicators
    tag = models.UUIDField(verbose_name = 'Tag', default = uuid.uuid4, editable = False)
    email = models.EmailField(verbose_name = 'Email Address', max_length = 255, unique = True)
    # Key data
    username = models.CharField(verbose_name = 'Username', max_length = 40, unique = True)

    first_name = models.CharField(verbose_name = 'First Name', max_length = 50)
    last_name = models.CharField(verbose_name = 'Last Name', max_length = 50)
    date_of_birth = models.DateField(verbose_name = 'Date of Birth')

    # Boolean Switches
    is_active = models.BooleanField(verbose_name = 'Is Currently Active?', default = True)
    is_admin = models.BooleanField(verbose_name = 'Is Admin?', default = False)
    # Time stamps
    created_at = models.DateTimeField(verbose_name = 'Created At', auto_now_add = True)
    updated_at = models.DateTimeField(verbose_name = 'Last Changed', auto_now = True)
     # Verification data
    is_verified = models.BooleanField(verbose_name = 'Verified', default = False)
    verification_token = models.CharField(verbose_name = 'Verfication Token', max_length = 200, null = True)
    # Reset password data
    reset_password_token =  models.CharField(verbose_name = 'Reset Password Token', max_length = 200, null = True)
    reset_instance_token = models.CharField(verbose_name = 'Reset Instance Token', max_length = 200, null = True)
    password_reset_at = models.DateTimeField(default = '2001-02-09 18:34:10.568064+00:00', null = True)
    # Constants
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'date_of_birth']
    # Setting manager
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    @property
    def is_staff(self): 
        return self.is_admin
    def has_perm(self, perm, obj=None): 
        return True
    def has_module_perms(self, app_label): 
        return True

    # Code generation
    def regenerate_code(self, rlength = 40):
        return "".join([str(random.choice(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q", "R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"])) for i in range(0, rlength)])
    # Sending User Verifcation
    def verify_user(self):
        self.verification_token = self.regenerate_code()
        self.save()
        tag = base64.b64encode(bytes(str(self.tag), 'utf-8')).decode().strip("=") 
        token = base64.b64encode(bytes(str(self.verification_token), 'utf-8')).decode().strip("=")
        page = render_to_string('main/emails/confirmation.html', {'site': settings.SITE_URL + '/verify','tag': tag, 'token': token})
        return send_mail('User Confirmation!', strip_tags(page), settings.EMAIL_HOST_USER, [self.email], fail_silently=True, html_message=page)
    # Sending Password Reset
    def forgot_password(self):
        self.reset_password_token = self.regenerate_code()
        self.password_reset_at = timezone.now()
        self.save()
        tag = base64.b64encode(bytes(str(self.tag), 'utf-8')).decode().strip("=") 
        token = base64.b64encode(bytes(str(self.reset_password_token), 'utf-8')).decode().strip("=")
        page = render_to_string('main/emails/forgot-password.html', {'site': settings.SITE_URL + '/forgot-password','tag': tag, 'token': token, 'name': self.first_name})
        return send_mail('User Password Reset!', strip_tags(page), settings.EMAIL_HOST_USER, [self.email], fail_silently=True, html_message=page)
    # Generating password reset instance
    def forgot_password_instance(self):
        self.reset_instance_token = self.regenerate_code(rlength=60)
        self.save()
        return self.reset_instance_token
    # Resetting all reset data
    def reset_forgot_password(self):
        self.reset_password_token = None
        self.password_reset_at = None
        self.reset_instance_token = None
        self.save()
    # Time difference checker
    def time_left(self, default = 60*60*24):
        if self.password_reset_at:
            dif = (timezone.now() - self.password_reset_at).total_seconds()
            if dif <= default: 
                return True
        return False

