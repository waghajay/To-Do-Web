from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.


def userLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.error(request, "User Not Found")  # Changed to messages.
            print("User Not Found")
            return redirect('userLogin')
        
        user = authenticate(request, username=email, password=password)  # Ensure you use the correct username field
        if user is None:
            messages.error(request, "Wrong Password")  # Changed to messages.error
            print("Wrong Password")            
            return redirect('userLogin')
        
        login(request, user)  # Only call login once
        next_url = request.GET.get('next')
        return redirect(next_url) if next_url else redirect('/')  # Simplified the redirect logic

    return render(request, 'authentication/login.html')


def userRegister(request):
    return render(request, 'authentication/register.html')