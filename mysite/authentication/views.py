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
from .models import CustomUser, UserProfile, FriendRequest
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
from .models import Message
import uuid


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

        # Define a regex pattern for institutional email domains
        institutional_email_pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.)+(edu|ac|org|[a-z]{2})$'

        # Initialize a flag for errors
        has_error = False

        # Check if the email matches the institutional email pattern
        if not re.match(institutional_email_pattern, email):
            messages.error(request, "Please use a valid institutional email address.")
            has_error = True

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose another.")
            has_error = True
        
        if CustomUser.objects.filter(email=email).exists():
            mailto_link = f"mailto:{email}?subject=OTP%20Request&body=Please%20send%20me%20the%20OTP%20for%20my%20account."
            messages.info(request, f"An account with this email already exists. Please check your email for the OTP. If you haven't received it, click <a href='{mailto_link}'>here</a> to send a request.", extra_tags='safe')
            has_error = True
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")
            has_error = True
        
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            has_error = True
        
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric.")
            has_error = True

        # If there are errors, render the signup page again
        if has_error:
            return render(request, "authentication/signup.html")

        # Check if the profile image is provided; if not, set a default image
        if not profile_image:
            profile_image = staticfiles_storage.url('images/woman.jpg') 

        # Create a new user instance
        myuser = CustomUser.objects.create_user(
            username=username, email=email, password=pass1, 
            country=country, location=location, institution=institution,
            profile_picture=profile_image  # Save the uploaded image or the default
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

        # Store the profile picture URL in the session
        request.session['profile_picture'] = myuser.profile_picture.url if myuser.profile_picture else None

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
        # Check if the OTP is provided
        if 'otp' in request.POST:
            otp = request.POST['otp']
            try:
                user = CustomUser.objects.get(email=email)
                if user.is_otp_valid(otp):  # Pass the OTP to the method
                    user.otp = None
                    user.otp_created_at = None
                    user.save()
                    messages.success(request, "OTP verified successfully. You can now log in.")
                    
                    # Store the profile picture URL in the session
                    request.session['profile_picture'] = user.profile_picture.url if user.profile_picture else None
                    
                    return redirect('signin')  # Redirect to the sign-in page
                else:
                    messages.error(request, "Invalid or expired OTP.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            messages.error(request, "OTP is required.")
    
    return render(request, "authentication/verify_otp.html", {'email': email})

def resend_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            user.generate_otp()  # Generate a new OTP
            
            # Send the new OTP email
            send_mail(
                'Your New OTP',
                f'Your new OTP is {user.otp}. It is valid for 10 minutes.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "A new OTP has been sent to your email.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
    
    return redirect('verify_otp')  # Redirect back to the OTP verification page

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            # No OTP check here, since the user has already verified their OTP during signup
            login(request, user)
            return redirect('homepage')  # Redirect to the homepage after successful login
        else:
            messages.error(request, "Invalid username or password")  # Invalid username or password
            return redirect('signin')  # Redirect back to the sign-in page
    
    # If the request method is GET, retrieve the profile picture for display
    profile_picture = None
    if 'username' in request.GET:
        username = request.GET['username']
        try:
            user = CustomUser.objects.get(username=username)
            profile_picture = user.profile_picture.url if user.profile_picture else None
        except CustomUser.DoesNotExist:
            profile_picture = None

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

def profile_view(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)  # Access the user profile
        return render(request, "authentication/profile.html", {'profile': user_profile})
    else:
        return redirect('login')  # Redirect to login if not authenticated

def friends(request):
    if request.user.is_authenticated:
        user_profile = request.user
        
        # Fetch accepted friends
        accepted_friends = CustomUser.objects.filter(
            id__in=FriendRequest.objects.filter(
                accepted=True,
                from_user=request.user
            ).values_list('to_user', flat=True)
        ).union(
            CustomUser.objects.filter(
                id__in=FriendRequest.objects.filter(
                    accepted=True,
                    to_user=request.user
                ).values_list('from_user', flat=True)
            )
        )

        # Fetch incoming friend requests
        incoming_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)

        # Fetch friend suggestions based on institution or location
        friend_suggestions = CustomUser.objects.exclude(id=request.user.id).exclude(id__in=accepted_friends.values_list('id', flat=True))

        # Suggest friends from the same institution or location
        suggestions_from_school = friend_suggestions.filter(
            institution=user_profile.institution
        )
        suggestions_from_location = friend_suggestions.filter(
            location=user_profile.location
        )

        # Combine suggestions if needed
        suggestions = suggestions_from_school | suggestions_from_location

        return render(request, "authentication/friends.html", {
            'incoming_requests': incoming_requests,
            'friends': accepted_friends,
            'suggestions': suggestions
        })
    else:
        return redirect('signin')  # Redirect to sign-in if not authenticated

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

@login_required
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        print("Form submitted")  # Debugging line
        print(request.POST)  # Print the POST data for debugging

        # Update user information
        request.user.first_name = request.POST.get('fname', request.user.first_name)  # Ensure 'fname' matches your form
        request.user.last_name = request.POST.get('lname', request.user.last_name)  # Ensure 'lname' matches your form
        request.user.email = request.POST.get('email', request.user.email)

        # Update profile information
        user_profile.country = request.POST.get('country', user_profile.country)
        user_profile.location = request.POST.get('location', user_profile.location)
        user_profile.institution = request.POST.get('institution', user_profile.institution)

        # Handle profile picture upload
        profile_image = request.FILES.get('profile_picture')
        if profile_image:
            user_profile.profile_picture = profile_image  # Update the profile picture

        # Save changes
        request.user.save()
        user_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect('profile_view')  # Redirect to the profile view after saving

    return render(request, 'authentication/edit_profile.html', {'user_profile': user_profile})

def chat_view(request, friend_id):
    if request.user.is_authenticated:
        friend = get_object_or_404(CustomUser, id=friend_id)
        
        # Fetch messages between the two users
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=friend)) | 
            (Q(sender=friend) & Q(recipient=request.user))
        ).order_by('timestamp')

        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                Message.objects.create(sender=request.user, recipient=friend, content=content)
                return redirect('chat', friend_id=friend.id)  # Redirect to the same chat view

        return render(request, 'authentication/chat.html', {
            'friend': friend,
            'messages': messages,
        })
    else:
        return redirect('signin')  # Redirect to sign-in if not authenticated

@login_required
def chat_list_view(request, friend_id=None):
    # Get the list of friends based on accepted friend requests
    friends = CustomUser.objects.filter(
        Q(friend_requests_received__from_user=request.user, friend_requests_received__accepted=True) |
        Q(friend_requests_sent__to_user=request.user, friend_requests_sent__accepted=True)
    )

    messages = []
    friend = None

    if friend_id:
        friend = get_object_or_404(CustomUser, id=friend_id)  # Get the friend by ID
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=friend)) |
            (Q(sender=friend) & Q(recipient=request.user))
        ).order_by('timestamp')  # Order messages by timestamp
        
    return render(request, 'authentication/chat_list.html', {
        'friends': friends,
        'messages': messages,
        'friend': friend,
    })


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


