from django.urls import path
from authentication.views import *


urlpatterns = [
    path('',userLogin,name="userLogin"),
    path('register/',userRegister,name="userRegister"),
    path('registration_varify/<auth_token>',varify,name="varify"),
]
