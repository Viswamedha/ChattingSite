from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin 
from .models import *
from .forms import *

admin.site.unregister(Group)




@admin.register(User)
class UserAdmin(UserAdmin):
    
    form = EditUserForm
    add_form = CreateUserForm
    
    list_display = ('email', 'username', 'date_of_birth', 'is_admin', 'is_verified')
    list_filter = ('is_admin', 'is_verified')

    fieldsets = (
        ('Personal Info', {
            'classes': ('collapse', 'extrapretty'),
            'fields': (('email', 'username'), ('first_name', 'last_name'), ('date_of_birth','tag'),'password'),
            'description': 'Main user details! '
            }),
        ('Permissions', {
            'classes': ('collapse', 'extrapretty'),
            'fields': (('is_active', 'is_admin', 'is_verified',),),
            'description': 'Key permissions! (Need a proper permission framework later)'
            }),
        ('Logs', {
            'classes': ('collapse', 'extrapretty'),
            'fields': (('created_at', 'updated_at',),),
            'description': 'All logging data from a user! '
            }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'date_of_birth', 'first_name', 'last_name', 'password', 'confirm_password'),
        }),
    )
    search_fields = ('email','username','created_at',)
    ordering = ('email','created_at',)
    filter_horizontal = ()
    readonly_fields = ['tag', 'created_at','updated_at']






