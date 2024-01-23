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
from base.models import PatientRecord



date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def register(request):
    form1 = UserRegistrationForm()
    registered_hospitals = RegisteredHospital.objects.all()
    
    if request.method == "POST":
        hospital_name = request.POST['hospital_name']
        role = request.POST['role']
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
            hospital_profile = HospitalProfile(user = user_instance, hospital_name = hospital_name, role=role)
            
            user_instance.save()
            hospital_profile.save()
            
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
    form1 = UserRegistrationForm()
    registered_hospitals = RegisteredHospital.objects.all()
    
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status="Awaiting Test Results")
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "form1": form1,
        "registered_hospitals": registered_hospitals,
        "test_notifications": test_notifications
    }
    return render(request, 'users/profile_page.html', context)

def edit_user_profile_page(request):
    if request.method == "POST":
        hospital_name = request.POST['hospital_name']
        role = request.POST['role']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        
        user = request.user
        hospital_profile = HospitalProfile.objects.filter(user=user).first()
        
        hospital_profile.hospital_name = hospital_name
        hospital_profile.role = role
        hospital_profile.phone_number = phone_number
        user.first_name = first_name
        user.last_name = last_name
        user.email = email  
              
        user.save()
        hospital_profile.save()
        
        redirect_url = reverse('profile-page')
        return redirect(redirect_url)
