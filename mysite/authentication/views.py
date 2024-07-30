import json
import random
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, UserProfile, FriendRequest
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "authentication/index.html")

def homepage(request):
    return render(request, "authentication/homepage.html")

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
        profile_image = request.FILES.get('profileImage')  # Get the uploaded image file

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose another.")
            return redirect('home')
        
        if CustomUser.objects.filter(email=email).exists():
            mailto_link = f"mailto:{email}?subject=OTP%20Request&body=Please%20send%20me%20the%20OTP%20for%20my%20account."
            messages.info(request, f"An account with this email already exists. Please check your email for the OTP. If you haven't received it, click <a href='{mailto_link}'>here</a> to send a request.", extra_tags='safe')
            return render(request, "authentication/signup.html")
        
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
            country=country, location=location, institution=institution,
            profile_picture=profile_image  # Save the uploaded image
        )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.generate_otp()
        myuser.save()
        
        # Create the UserProfile automatically
        UserProfile.objects.create(
            user=myuser,
            country=country,
            location=location,
            institution=institution
        )

        # Generate the OTP verification URL
        otp_verification_url = f"{request.scheme}://{request.get_host()}{reverse('verify_otp')}?email={email}"

        # Send OTP email with link
        subject = "Your OTP for StudentKonnect"
        message = (
            f"Hello {myuser.first_name},\n\n"
            f"Your OTP is {myuser.otp}. It is valid for 10 minutes.\n\n"
            f"Click this link to enter your OTP: {otp_verification_url}\n\n"
            "Thank You,\n ELaine"
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        messages.success(request, "Your account has been successfully created. Please check your email for the OTP.")
        
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
            return redirect('homepage')
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
    with open("data/world_universities_and_domains.json", "r") as json_file:
        universities_data = json.load(json_file)

    return JsonResponse(universities_data, safe=False)

def profile_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)  # Access the user profile
        return render(request, "profile.html", {'profile': user_profile})
    else:
        return redirect('login')  # Redirect to login if not authenticated

def friends(request):
    if request.user.is_authenticated:
        user_profile = request.user
        # Get friends from the same institution and country of origin
        friends_from_school = CustomUser.objects.filter(
            institution=user_profile.institution,
            country=user_profile.country
        ).exclude(id=request.user.id)
        # If no friends found from the same institution, get friends from the same location
        if not friends_from_school.exists():
            friends_from_country = CustomUser.objects.filter(
                location=user_profile.location,
                country=user_profile.country
            ).exclude(id=request.user.id)
            friends = friends_from_country
        else:
            friends = friends_from_school

        return render(request, "authentication/friends.html", {'friends': friends})
    else:
        return redirect('login')  # Redirect to login if not authenticated


def friend_suggestions(request):
    if request.user.is_authenticated:
        user_profile = request.user

        # Get friends from the same institution and country of origin
        friends_from_school = CustomUser.objects.filter(
            institution=user_profile.institution,
            country=user_profile.country
        ).exclude(id=request.user.id)

        # If no friends found from the same institution, get friends from the same location
        if not friends_from_school.exists():
            friends_from_country = CustomUser.objects.filter(
                location=user_profile.location,
                country=user_profile.country
            ).exclude(id=request.user.id)
            friends = friends_from_country
        else:
            friends = friends_from_school

        return render(request, 'friend_suggestions.html', {'friends': friends})
    else:
        return redirect('login')  # Redirect to login if not authenticated

def send_friend_request(request, user_id):
    if request.user.is_authenticated:
        to_user = get_object_or_404(CustomUser, id=user_id)
        
        # Check if the user is not trying to send a friend request to themselves
        if to_user != request.user:
            # Create a friend request if it doesn't already exist
            friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
            
            if created:
                messages.success(request, f"Friend request sent to {to_user.username}!")
            else:
                messages.info(request, f"You have already sent a friend request to {to_user.username}.")
        else:
            messages.error(request, "You cannot send a friend request to yourself.")
        
        return redirect('friend_suggestions')  # Redirect back to friend suggestions
    else:
        return redirect('login')  # Redirect to login if not authenticated

def your_django_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        country_code = data.get('country')
        location_code = data.get('location')

        # Create a mapping of country codes to names
        country_mapping = {
            'AF': 'Afghanistan',
            'AU': 'Australia',
            # Add more countries as needed
        }

        country_name = country_mapping.get(country_code, 'Unknown Country')
        location_name = country_mapping.get(location_code, 'Unknown Location')

        # Return the full names as JSON response
        return JsonResponse({
            'country_name': country_name,
            'location_name': location_name
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)