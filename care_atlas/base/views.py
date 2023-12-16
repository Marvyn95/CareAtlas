from django.shortcuts import render
from base.forms import PatientForm, PatientRecordForm, PatientVitalForm
import datetime


date_1 = datetime.datetime.now().strftime("%A %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "date": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_page(request):
    return render(request, 'base/application_page.html', date)

def new_patient_page(request):
    return render(request, 'base/new_patient.html', date)

def new_patient_vital_page(request):
    return render(request, 'base/new_patient_vital.html', date)

def new_patient_record_page(request):
    return render(request, 'base/new_patient_record.html', date)