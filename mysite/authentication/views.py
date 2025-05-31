from django.db.models import Q
import re
import json
import random
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, FriendRequest
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
from .models import Message
import uuid
from .news_service import NewsService
from django.templatetags.static import static
from .models import Housing, Transport, Culture
from collections import defaultdict
from django.core.files.storage import default_storage
from django.templatetags.static import static
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django_countries import countries
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

def home(request):
    return render(request, "authentication/index.html")

def homepage(request):
    user = request.user
    print(f"User: {user.username}, Location: {user.location}, Institution: {user.institution}")

    # Check if user has location and institution attributes
    if not hasattr(user, 'location') or not hasattr(user, 'institution'):
        return render(request, 'authentication/homepage.html', {'error': 'User information is incomplete.'})

    location = user.location
    institution = user.institution

    categories = ['accommodation', 'transportation', 'student_resources', 'school']
    news_data = {}
    for category in categories:
        news_data[category] = NewsService.get_news_by_category(category, location, institution)

    # Fetch all data without filtering by country
    housing_items = Housing.objects.all()
    transport_items = Transport.objects.all()
    culture_items = Culture.objects.all()

    # Group items by country
    country_data = defaultdict(lambda: {'housing': [], 'transport': [], 'culture': []})

    for item in housing_items:
        country_data[item.country]['housing'].append(item)
    for item in transport_items:
        country_data[item.country]['transport'].append(item)
    for item in culture_items:
        country_data[item.country]['culture'].append(item)

    # Debugging statements
    print(f"Country Data: {country_data}")

    context = {
        'news_data': news_data,
        'country_data': dict(country_data), 
    }

    return render(request, "authentication/homepage.html", context)

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be atleast 8 characters long."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain atleast one lowercase letter"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain atleast one uppercase letter"
    if not re.search(r"[0-9]", password):
        return False, "password must contain atleast one number"
    if not re.search(r"[!@#$%^&*]", password):
        return False, "Password must contain atleast one special character (!@#$%)"
    if re.search(r"\s", password):
        return False, "Passsword must not contain spaces"
    return True, "Password is valid."

def signup(request):
    if request.method == "POST":
        profile_picture = request.FILES.get('profileImage')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        country = request.POST['country']
        location = request.POST['location']
        institution = request.POST['institution']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code'] 
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
      
        
        print("Files in request:", request.FILES)
        print("Profile picture:", profile_picture)

        # Log the incoming data for debugging
        print("Received data:", {
            'username': username,
            'fname': fname,
            'lname': lname,
            'email': email,
            'country': country,
            'location': location,
            'institution': institution,
            'city': city,
            'state': state,
            'zip_code': zip_code,
        })  # Debugging line

        # institutional_email_pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.)+(edu|ac|org|[a-z]{2})$'
        institutional_email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|outlook\.com|net|([a-zA-Z0-9-]+\.)+(edu|ac|org|com|[a-z]{2}))$'
        has_error = False
        error_messages = []

        # Validation checks
        if not re.match(institutional_email_pattern, email):
            error_messages.append("Please use a valid institutional email address.")
            has_error = True

        if CustomUser.objects.filter(username=username).exists():
            error_messages.append("Username already exists. Choose another.")
            has_error = True
        
        if CustomUser.objects.filter(email=email).exists():
            error_messages.append("An account with this email already exists.")
            has_error = True
        
        if len(username) > 10:
            error_messages.append("Username must be under 10 characters.")
            has_error = True
        
        if pass1 != pass2:
            error_messages.append("Passwords do not match.")
            has_error = True
        
        if not username.isalnum():
            error_messages.append("Username must be alphanumeric.")
            has_error = True

        is_valid, message = validate_password(pass1)
        if not is_valid:
            error_messages.append(message)
            has_error = True
        
        if has_error:
            for message in error_messages:
                messages.error(request, message, extra_tags='safe')
            return render(request, "authentication/signup.html", {
                'username': username,
                'fname': fname,
                'lname': lname,
                'email': email,
                'country': country,
                'location': location,
                'institution': institution,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'country_choices': list(countries),
                'profile_picture': profile_picture, 
              
            })

        # Create the user
        myuser = CustomUser.objects.create_user(
            username=username, email=email, password=pass1,
            is_verified=False  # Set to False initially
        )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.country = country
        myuser.location = location
        myuser.institution = institution
        myuser.city = city
        myuser.state = state
        myuser.zip_code = zip_code
        
        if profile_picture:
            myuser.profile_picture = profile_picture
        myuser.save()  # Save the user first
        
        # Debugging: Check if the user was created correctly
        print(f"User created: {myuser.username}, Profile Picture: {myuser.profile_picture}")
        
        if has_error:
            return JsonResponse({'errors': error_messages}, status=400)
        # return JsonResponse({'message': 'Success'})
       
        myuser.generate_otp()  # Generate and save the OTP

        # Send OTP email
        subject = "Your OTP for Verification"
        message = (
            f"Hello {myuser.first_name},\n\n"
            f"Your OTP is {myuser.otp}. It is valid for 10 minutes.\n\n"
            "Thank You,\n Elaine"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

        messages.success(request, "Your account has been successfully created. Please check your email for the OTP.")
        
        return redirect(f"{reverse('verify_otp')}?email={email}")
        # Redirect to the OTP verification page
    
    return render(request, "authentication/signup.html")

def verify_otp(request):
    email = request.GET.get('email') or request.session.get('email')
    if email:
        request.session['email'] = email  # Save email in session for resend_otp

    if request.method == "POST":
        otp = request.POST.get('otp')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_otp_valid(otp):
                    user.is_verified = True
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    messages.success(request, "OTP verified successfully. You can now log in.")
                   
                    del request.session['email']
                    return redirect('signin')
                else:
                    messages.error(request, "Invalid or expired OTP.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            messages.error(request, "Email not found.")

    return render(request, "authentication/verify_otp.html", {'email': email})

def resend_otp(request):
    if request.method == "POST":
        email = request.session.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                user.generate_otp()
                send_mail(
                    'Your New OTP',
                    f'Your new OTP is {user.otp}. It is valid for 10 minutes.',
                    'your_verified_sender@example.com',
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "A new OTP has been sent to your email.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            messages.error(request, "No email found in session.")

    return redirect('verify_otp')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()  
        password = request.POST.get('pass1', '').strip() 
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('signin')
    
    profile_picture = None
    if request.user.is_authenticated:
        profile_picture = request.user.profile_picture.url if request.user.profile_picture else None

    return render(request, "authentication/signin.html", {'profile_picture': profile_picture})

def signout(request):
    logout(request)
    return redirect('home')

def index(request):
    return render(request, 'authentication/index.html')

def about(request):
    return render(request, 'authentication/about.html')

def universities_data(request):
    with open("data/world_universities_and_domains.json", "r") as json_file:
        universities_data = json.load(json_file)

    return JsonResponse(universities_data, safe=False)

def profile(request):
    return render(request, 'authentication/profile.html')

# def profile_view(request):
#     if request.user.is_authenticated:
#         profile = get_object_or_404(UserProfile, user=request.user)
#         return render(request, "authentication/profile.html", {'profile': profile})
#     else:
#         return redirect('login')  


@login_required
def profile_view(request):
    return render(request, "authentication/profile.html", {'user': request.user})

@login_required
def friends(request):
    if request.user.is_authenticated:
        user = request.user  # Use the CustomUser instance directly

        # Fetch accepted friends (unchanged)
        accepted_friends = CustomUser.objects.filter(
            id__in=FriendRequest.objects.filter(
                accepted=True,
                from_user=user
            ).values_list('to_user', flat=True)
        ).union(
            CustomUser.objects.filter(
                id__in=FriendRequest.objects.filter(
                    accepted=True,
                    to_user=user
                ).values_list('from_user', flat=True)
            )
        )

        # Fetch incoming friend requests (unchanged)
        incoming_requests = FriendRequest.objects.filter(to_user=user, accepted=False)

        # Fetch friend suggestions based on institution, location, city, and state
        friend_suggestions = CustomUser.objects.exclude(id=user.id).exclude(id__in=accepted_friends.values_list('id', flat=True))

        # Suggest friends from the same institution
        suggestions_from_school = friend_suggestions.filter(
            institution=user.institution  # <-- Changed
        )
        
        # Suggest friends from the same location
        suggestions_from_location = friend_suggestions.filter(
            location=user.location  # <-- Changed
        )
        
        # Suggest friends from the same city
        suggestions_from_city = friend_suggestions.filter(
            city=user.city  # <-- Changed (no userprofile__)
        )
        
        # Suggest friends from the same state
        suggestions_from_state = friend_suggestions.filter(
            state=user.state  # <-- Changed (no userprofile__)
        )

        # Combine suggestions (unchanged)
        suggestions = (suggestions_from_school | suggestions_from_location |
                       suggestions_from_city | suggestions_from_state).distinct()

        return render(request, "authentication/friends.html", {
            'incoming_requests': incoming_requests,
            'friends': accepted_friends,
            'suggestions': suggestions
        })
    else:
        return redirect('signin')


def send_friend_request(request, user_id):
    if request.user.is_authenticated:
        to_user = get_object_or_404(CustomUser, id=user_id)
        
        if to_user != request.user:
            # Check if they are already friends
            if FriendRequest.objects.filter(
                (Q(from_user=request.user) & Q(to_user=to_user) & Q(accepted=True)) |
                (Q(from_user=to_user) & Q(to_user=request.user) & Q(accepted=True))
            ).exists():
                messages.error(request, f"You are already friends with {to_user.username}.")
            else:
                friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
                
                if created:
                    messages.success(request, f"Friend request sent to {to_user.username}!")
                else:
                    messages.info(request, f"You have already sent a friend request to {to_user.username}.")
        else:
            messages.error(request, "You cannot send a friend request to yourself.")
        
        return redirect('friends')  # Redirect back to friends page
    else:
        return redirect('signin')  # Redirect to login if not authenticated

def accept_friend_request(request, request_id):
    if request.user.is_authenticated:
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
        friend_request.accepted = True
        friend_request.save()
        
        messages.success(request, f"You are now friends with {friend_request.from_user.username}!")
        return redirect('friends')
    else:
        return redirect('signin')

def decline_friend_request(request, request_id):
    if request.user.is_authenticated:
        friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
        friend_request.delete()  # Remove the friend request
        
        messages.success(request, "Friend request declined.")
        return redirect('friends')
    else:
        return redirect('signin')

def friend_requests_view(request):
    if request.user.is_authenticated:
        friend_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        return render(request, 'authentication/friend_requests.html', {'friend_requests': friend_requests})
    else:
        return redirect('signin')  # Redirect to sign-in if not authenticated

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

def how_it_works(request):
    return render(request, 'authentication/how_it_works.html')

def testimonials(request):
    return render(request, "authentication/testimonials.html")

# @login_required
# def edit_profile(request):
#     user_profile = get_object_or_404(UserProfile, user=request.user)

#     if request.method == 'POST':
#         user_profile.country = request.POST.get('country', user_profile.country)
#         user_profile.location = request.POST.get('location', user_profile.location)
#         user_profile.institution = request.POST.get('institution', user_profile.institution)
#         user_profile.city = request.POST.get('city', user_profile.city)
#         user_profile.state = request.POST.get('state', user_profile.state)

#         profile_image = request.FILES.get('profile_picture')
#         if profile_image:
#             user_profile.profile_picture = profile_image
#         user_profile.save()
#         messages.success(request, "Profile updated successfully.")
#         return redirect('profile_view')

#     return render(request, 'authentication/edit_profile.html', {'user_profile': user_profile})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Update profile fields
        user.first_name = request.POST.get('fname', user.first_name)
        user.last_name = request.POST.get('lname', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.country = request.POST.get('country', user.country)
        user.location = request.POST.get('location', user.location)
        user.institution = request.POST.get('institution', user.institution)
        user.city = request.POST.get('city', user.city)
        user.state = request.POST.get('state', user.state)

        profile_image = request.FILES.get('profile_picture')
        if profile_image:
            user.profile_picture = profile_image

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile_view')
    context = {
        'user': user,
    }

    return render(request, 'authentication/edit_profile.html', context)
@receiver(pre_save, sender=CustomUser)
def delete_old_profile_picture(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if new object

    try:
        old_user = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_file = old_user.profile_picture
    new_file = instance.profile_picture
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = CustomUser.objects.get(email=email)
            # Generate a unique token
            token = str(uuid.uuid4())
            user.password_reset_token = token
            user.token_created_at = timezone.now()
            user.save()

            # Send password reset email
            reset_url = f"{request.scheme}://{request.get_host()}{reverse('password_reset_confirm', args=[token])}"
            subject = "Password Reset Request"
            message = f"Hello {user.first_name},\n\nClick the link below to reset your password:\n{reset_url}\n\nThank You!"
            send_mail(subject, message, 'from@example.com', [user.email], fail_silently=False)

            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('home')
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email address.")
    
    return render(request, "authentication/password_reset_request.html")

def password_reset_confirm(request, token):
    try:
        user = CustomUser.objects.get(password_reset_token=token)
        # Check if the token is still valid (e.g., not expired)
        if timezone.now() > user.token_created_at + timezone.timedelta(hours=1):  # Token valid for 1 hour
            messages.error(request, "This password reset link has expired.")
            return redirect('password_reset_request')

        if request.method == "POST":
            new_password = request.POST['new_password']
            user.set_password(new_password)  # Use Django's method to hash the password
            user.password_reset_token = None  # Clear the token after resetting
            user.token_created_at = None  # Clear the token timestamp
            user.save()
            messages.success(request, "Your password has been reset successfully. You can now log in.")
            return redirect('signin')

    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid password reset token.")
    
    return render(request, "authentication/password_reset_confirm.html", {'token': token})

@login_required
def chat_view(request, friend_id):
    friend = get_object_or_404(CustomUser, id=friend_id)
    
    # Fetch the messages between the logged-in user and the friend
    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=friend)) | 
        (Q(sender=friend) & Q(recipient=request.user))
    ).order_by('timestamp')

    # Retrieve the list of friends for the logged-in user
    friends = CustomUser.objects.filter(
        Q(friend_requests_sent__to_user=request.user, friend_requests_sent__accepted=True) | 
        Q(friend_requests_received__from_user=request.user, friend_requests_received__accepted=True)
    ).distinct()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, recipient=friend, content=content)
            return redirect('chat_with_friend', friend_id=friend_id)

    return render(request, 'authentication/chat.html', {
        'friend': friend,
        'messages': messages_list,
        'friends': friends,  # Pass the friends list to the template
    })

# views.py
@login_required
def chat_list_view(request):
    # Retrieve friends for the logged-in user
    friends = CustomUser.objects.filter(
        Q(friend_requests_received__from_user=request.user, friend_requests_received__accepted=True) |
        Q(friend_requests_sent__to_user=request.user, friend_requests_sent__accepted=True)
    ).distinct()

    # Retrieve all messages for the logged-in user
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('timestamp')

    # Create a dictionary to store the last message for each friend
    last_messages = {}
    for friend in friends:
        last_message = messages.filter(
            Q(sender=friend, recipient=request.user) | Q(sender=request.user, recipient=friend)
        ).last()
        last_messages[friend.id] = last_message

    return render(request, 'authentication/chat_list.html', {
        'friends': friends,
        'last_messages': last_messages,
    })



