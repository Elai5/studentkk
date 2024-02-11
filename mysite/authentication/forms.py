# Inside forms.py

from django import forms

class UserRegistrationForm(forms.Form):
    fname = forms.CharField(label="First Name", max_length=100)
    lname = forms.CharField(label="Last Name", max_length=100)
    email = forms.EmailField(label="Email Address")
    country = forms.CharField(label="Country of Origin", max_length=100)
    location = forms.CharField(label="Current Location", max_length=100)
    institution = forms.CharField(label="Academic Institution", max_length=200)
    pass1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    pass2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    # Add any other fields you need (e.g., username, additional profile info)

    # You can also add custom validation methods if necessary
