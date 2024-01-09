from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import HospitalProfile

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
        
    class Meta:
        model = User
        fields  = ['first_name', 'last_name', 'email', 'password1', 'password2']
        
