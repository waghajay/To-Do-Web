from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse

from django.contrib.auth.models import User
from authentication.models import UserProfile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import uuid
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string



# Create your views here.


def userLogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        print("Password: " + password)
        
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
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        new_pass = request.POST.get('new_pass')
        conf_pass = request.POST.get('conf_pass')
        
        print("New password", new_pass)
        print("Conform password", conf_pass)
        
        
        if new_pass==conf_pass:
            if User.objects.filter(email=email).exists():
                messages.success(request,"Email already exists..")
                return redirect('userRegister')
            
            user = User.objects.create_user(username=email,password=new_pass,first_name=first_name,last_name=last_name,email=email)
            user.save()
            
            auth_token = str(uuid.uuid4())
            user_profile_obj = UserProfile.objects.create(user=user,auth_token=auth_token)
            send_mail_after_registration(email,auth_token,first_name,last_name)
            messages.success(request,"Verification email has been sent to your registered email..")
            return redirect('userLogin')
        
        else:
            messages.success(request,"Password Not Match")
            return redirect('userRegister')    
        
        
        
    return render(request, 'authentication/register.html')


def send_mail_after_registration(email, token, first_name,last_name):
    name = f"{first_name} {last_name}"
    subject = "Email Confirmation || To-Do's"
    html_content = render_to_string('authentication/email-confirm-email.html', {'name': name, 'token': token})
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    
def varify(request,auth_token):
    try:
        user_profile_obj = UserProfile.objects.filter(auth_token=auth_token).first()
        
        if user_profile_obj is None:
            return HttpResponse("Opps Something went wrong")
        
        if user_profile_obj:
            if user_profile_obj.is_varified:
                messages.success(request,"Your account is already varified")
                return redirect('userLogin')
            
            
            user_profile_obj.is_varified = True
            user_profile_obj.save()
            messages.success(request,"Your account has been varified")            
            return redirect('userLogin')
        else:
            # return redirect('error')
            return HttpResponse("Opps Something went wrong")
    except Exception as e:
        print(e)