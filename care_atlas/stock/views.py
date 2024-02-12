from django.shortcuts import render
from users.models import HospitalProfile
from base.models import PatientRecord
from stock.models import Medication
import datetime

date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def medication_list_page(request):
    medication_list = Medication.objects.filter(hospital=request.user.hospitalprofile.hospital_name).order_by('name')
    
    #getting notifications for pending results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "medication_list": medication_list,
        "test_notifications": test_notifications    
    }
    return render(request, 'stock/medication_list.html', context)
    
    
    
