from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *
from .utils import *

urlpatterns = [
    path('404/', BaseView.as_view(template_name='main/static/404.html'), name='404'),
    path('', BaseView.as_view(template_name = 'main/home.html'), name = 'home'),
    
    path('login/', LoginView.as_view(template_name = 'main/auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('signup/', SignupView.as_view(template_name = 'main/auth/signup.html'), name='signup'),
    path('verify/<id>/<token>', VerificationView.as_view(), name='verify'),
    path('verify/check-your-mail/', BaseView.as_view(template_name='main/static/confirm-mail-sent.html'), name='verify-sent'),

    path('forgot-password/', ForgotPasswordRequestView.as_view(template_name = 'main/auth/reset-forgot-password.html'), name='reset-request'),
    path('forgot-password/check-your-mail/', BaseView.as_view(template_name='main/static/reset-mail-sent.html'), name='reset-sent'),
    path('forgot-password/<id>/<token>', ForgotPasswordProcessingView.as_view(), name='reset-processing'),
    path('reset/<instance>', ForgotPasswordChangeView.as_view(), name = 'reset-change'),
]
