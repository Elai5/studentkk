import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
from mysite import settings
from django.core.mail import send_mail
from django.apps import apps
import json
from django.http import JsonResponse

# Create your views here.
def home(request):
    # return HttpResponse("hello monica")
    return render(request, "authentication/index.html")

def verify_email_with_hunter(email):
    # Replace 'your_api_key_here' with your actual Hunter API key
    api_key = '709a4901e4f150a8aa5909792dfd1a2baceb770d'
    url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}'

    try:
        response = requests.get(url)
        print("Response from Hunter API:", response.json())  # Debug statement
        data = response.json()
        if data['data']['result'] == 'valid':
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False

def signup(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        country = request.POST['country']
        location = request.POST['location']
        institution = request.POST['institution']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        
        # email
        #check if username already exist
        if User.objects.filter(username=username):
            messages.error(request, "username alrady exist. Chose another")
            return redirect('home')
        
        # Check if the email address belongs to an institutional domain
        institutional_domains = ['edu', 'ac', 'edu.au', 'edu.uk']  # Add more domains as needed
        domain = email.split('@')[-1].split('.')[0]
        if domain not in institutional_domains:
            messages.error(request, "Please enter a valid institutional email address.")
            return redirect('home')
        #check if email is already registered    
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')
        
        # Verify email using Hunter API
        if not verify_email_with_hunter(email):
            messages.error(request, "Please enter a valid institutional email address.")
            return redirect('home')

        if len(username)>10:
            messages.error(request, "username be under 10 characters")
            
        if pass1 != pass2:
            messages.error(request, "password doesn`t march")
            
        if not username.isalnum():
            messages.error(request, "username must be alphanumeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1, country=country, location=location, institution=institution)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "your account has been succesfully created")
        # sednmail
        subject = "welcome to studentkonnect login"
        message = "hello" + myuser.first_name + "! \n" + "welcome to sks \n thankyou for visiting. \n weve sent email confrimation. \n\n thank you\n laine"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect('signin')
    return render(request, "authentication/signup.html")


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
            messages.error(request, "bad credentials")
            return redirect('home')
    
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    # messages.success(request, "log out succesfully!")
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
