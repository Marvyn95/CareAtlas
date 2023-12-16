from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import HospitalProfile
from .forms import UserRegistrationForm, HospitalProfileForm
from django.contrib.auth import authenticate, login, logout
from .utils import *
from django.contrib.auth.hashers import make_password

# Create your views here.
def register(request):
    form1 = UserRegistrationForm()
    form2 = HospitalProfileForm()
    approve_reg_application(form1, form2)
    
    if request.method == "POST":
        form1 = UserRegistrationForm(request.POST)
        form2 = HospitalProfileForm(request.POST)
        
        if form1.is_valid() and form2.is_valid():
            # saving user profile
            user_instance = User(
                username=form1.cleaned_data.get('first_name') + form1.cleaned_data.get('last_name'),
                first_name = form1.cleaned_data.get('first_name'),              
                last_name = form1.cleaned_data.get('last_name'),              
                email = form1.cleaned_data.get('email'),              
                password = make_password(form1.cleaned_data.get('password1'))          
            )
            user_instance.save()
            
            # getting users profile from database to access id
            user = User.objects.filter(email = form1.cleaned_data.get('email'),
                                       first_name = form1.cleaned_data.get('first_name'),
                                       last_name = form1.cleaned_data.get('last_name')
                                       ).first()
            
            # saving hospital profile
            hospital = HospitalProfile(
                user = user,
                hospital_name = form2.cleaned_data.get('hospital_name')
            )
            hospital.save()
            
            messages.success(request, "Your CareAtlas Account Has Been Created! You May Log In")
            return redirect("login")
        else:
            form1 = UserRegistrationForm(request.POST)
            form2 = HospitalProfileForm(request.POST)

    return render(request, 'users/registration_page.html', {'form1': form1, "form2": form2})


def login_page(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email']).first()
        if user:
            username = user.username
            password = request.POST['password']
            # authenticating and logging in user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                messages.success(request, 'Your Login Was Succesful')
                return redirect('application-page')
            else:
                messages.warning(request, 'Login Denied!, Please Check Login Credentials')
                return redirect('login')
        else:
            messages.warning(request, 'Login Denied!, Please Check Login Credentials')
            return redirect('login')
    return render(request, 'users/login_page.html')

def logout_page(request):
    logout(request)
    messages.success(request, "You Have Been Successfully Logged Out")
    return redirect('login')
