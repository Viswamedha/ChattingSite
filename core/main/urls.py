from django.urls.conf import path
from .views import *


urlpatterns = [
    path('', home),

    path('login/', login_view),
    path('logout/', logout_view),
    path('signup/', signup_view),
    
]