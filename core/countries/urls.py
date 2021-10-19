from django.urls.conf import path
from .views import *


urlpatterns = [
    path('<slug:slug>/', country),
    path('', country),
]