from django.shortcuts import render, redirect
from base.forms import PatientForm, PatientRecordForm, PatientVitalForm
import datetime
from django.contrib import messages
from base.models import Patient, PatientRecord, PatientVital


date_1 = datetime.datetime.now().strftime("%A %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "date": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_page(request):
    return render(request, 'base/application_page.html', date)

def new_patient_page(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        sex = request.POST["sex"]
        nationality = request.POST["nationality"]
        phone_number = request.POST["phone_number"]
        date_of_birth = request.POST["date_of_birth"]
        
        print(first_name)
        
        patient1 = Patient(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            nationality=nationality,
            phone_number=phone_number,
            date_of_birth=date_of_birth
        )
        patient1.save()
        messages.success(request, "Patient Profile Created Successfully")
        return redirect("new-patient")
    return render(request, 'base/new_patient.html', date)

def new_patient_vital_page(request):
    return render(request, 'base/new_patient_vital.html', date)

def new_patient_record_page(request):
    return render(request, 'base/new_patient_record.html', date)