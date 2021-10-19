from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
import uuid, random, string 


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
    tag = models.UUIDField(verbose_name = 'Tag', default = uuid.uuid4, editable = False, unique = False)
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
    password_reset_at = models.DateTimeField(default = '2000-01-01 0:00:00+00:00', null = True)
    # Constants
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name', 'date_of_birth']
    # Setting manager
    objects = UserManager()
    # Connections
    friends = models.ManyToManyField('self',  verbose_name = 'Friends', blank = True)
    blocked = models.ManyToManyField('self',  verbose_name = 'Blocked',  blank = True)
    following = models.ManyToManyField('self',  verbose_name = 'Following',  blank = True)
        

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['updated_at', '-created_at']

    
    @property
    def is_staff(self): 
        return self.is_admin
    def has_perm(self, perm, obj=None): 
        return True
    def has_module_perms(self, app_label): 
        return True


    def get_token(self, length: int = 40):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


class Group(models.Model):

    name = models.CharField(verbose_name = 'Name', max_length = 50)
    members = models.ManyToManyField(User, verbose_name = 'Members', related_name = 'groups')

    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'groups_created')
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'groups_owned')
    

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    
    def __str__(self):
        return self.name 

