from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from mysite import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    # return HttpResponse("hello monica")
    return render(request, "authentication/index.html")

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
        
        if User.objects.filter(username=username):
            messages.error(request, "username alrady exist. Chose another")
            return redirect('home')
            
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "username be under 10 characters")
            
        if pass1 != pass2:
            messages.error(request, "password doesn`t march")
            
        if not username.isalnum():
            messages.error(request, "username must be alphanumeric")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
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