from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import HospitalProfile, RegisteredHospital
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from .utils import *
from django.contrib.auth.hashers import make_password
from django.urls import reverse
import datetime



date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def register(request):
    form1 = UserRegistrationForm()
    registered_hospitals = RegisteredHospital.objects.all()
    print(registered_hospitals)
    
    if request.method == "POST":
        hospital_name = request.POST['hospital_name']
        form1 = UserRegistrationForm(request.POST)        
        approve_reg_application()
                
        if form1.is_valid():
            # saving user profile
            user_instance = User(
                username=form1.cleaned_data.get('first_name') + form1.cleaned_data.get('last_name'),
                first_name = form1.cleaned_data.get('first_name'),              
                last_name = form1.cleaned_data.get('last_name'),              
                email = form1.cleaned_data.get('email'),              
                password = make_password(form1.cleaned_data.get('password1'))          
            )            
            hospital = HospitalProfile(user = user_instance, hospital_name = hospital_name)
            user_instance.save()
            hospital.save()
            messages.success(request, "Your CareAtlas Account Has Been Created! You May Log In")
            return redirect("login")
        else:
            form1 = UserRegistrationForm(request.POST)
        
    context = {
        "registered_hospitals": registered_hospitals,
        "form1": form1,
    }

    return render(request, 'users/registration_page.html', context)


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
                return redirect('application-home')
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

def user_profile_page(request):
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date
    }
    return render(request, 'users/profile_page.html', context)
