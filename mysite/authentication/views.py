import json
import requests
import random
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from django.utils import timezone
from django.urls import reverse


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def get_email_domain(email):
    domain_parts = email.split('@')[-1].split('.')
    if len(domain_parts) >= 2:
        return '.'.join(domain_parts[-2:])
    return domain_parts[0]


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        country = request.POST['country']
        location = request.POST['location']
        institution = request.POST['institution']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose another.")
            return redirect('home')
        
        # Check if the email address belongs to an institutional domain
        institutional_domains = ['edu', 'ac', 'edu.au', 'edu.uk', 'ac.ke']
        domain = get_email_domain(email)
        if domain not in institutional_domains:
            messages.error(request, "Please enter a valid institutional email address.")
            return redirect('home')
        
        # Check if email is already registered    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            return redirect('home')
        
        # Create a new user instance
        myuser = CustomUser.objects.create_user(
            username=username, email=email, password=pass1, 
            country=country, location=location, institution=institution
        )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.generate_otp()
        myuser.save()
        
        # send OTP email
        subject = "Your OTP for StudentKonnect"
        message = f"Hello {myuser.first_name}, \n\nYour OTP is {myuser.otp}. It is valid for 10 minutes.\n\nThank You, \nLaine"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        messages.success(request, "Your account has been successfully created. Please check your email for the OTP.")
        
        # Redirect to verify_otp page with email as a parameter
        return redirect(f'{reverse("verify_otp")}?email={email}')
    
    return render(request, "authentication/signup.html") 

def verify_otp(request):
    email = request.GET.get('email') or request.POST.get('email')
    
    if request.method == "POST":
        otp = request.POST['otp']
        
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_otp_valid(otp):
                user.otp = None
                user.otp_created_at = None
                user.save()
                messages.success(request, "OTP verified successfully. You can now log in.")
                return redirect('signin')
            else:
                messages.error(request, "Invalid or expired OTP.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return render(request, "authentication/verify_otp.html", {'email': email})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')
    
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    return redirect('home')

def index(request):
    return render(request, 'authentication/index.html')

def about(request):
    return render(request, 'authentication/about.html')

def career(request):
    return render(request, 'authentication/career.html')

def universities_data(request):
    # Read the JSON file
    with open("data/world_universities_and_domains.json", "r") as json_file:
        universities_data = json.load(json_file)

    # Return the data as a JSON response
    return JsonResponse(universities_data, safe=False)