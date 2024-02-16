from django.shortcuts import render, redirect
from users.models import HospitalProfile
from base.models import PatientRecord
from stock.models import Medication
import datetime
from django.contrib import messages
from django.urls import reverse

date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def medication_list_page(request):
    medication_list = Medication.objects.filter(hospital=request.user.hospitalprofile.hospital_name).order_by('name')
    
    edited_medication_list = []
    k = 1
    for med in medication_list:
        edited_medication_list.append({
            "id": k,
            "name": med.name,
            "brand": med.brand,
            "formulation": med.formulation,
            "strength_value": med.strength_value,
            "strength_value_units": med.strength_value_units,
            "quantity": med.quantity,
            "db_id": med.id
        })
        k +=1
        
    #getting notifications for pending results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    #handling post requests
    if request.method == "POST":
        name = request.POST["name"]
        brand = request.POST["brand"] if request.POST["brand"] != "" else "None"
        formulation = request.POST["formulation"]
        strength = request.POST["strength"]
        units = request.POST["units"]
        
        #adding entry to the database
        medication = Medication(
            name=name,
            brand=brand,
            formulation=formulation,
            strength_value=strength,
            strength_value_units=units,
            quantity=0,
            hospital=request.user.hospitalprofile.hospital_name
        )
        medication.save()
        
        messages.success(request, "Your Medication Has Been Entered Into The System")
        redirect_url=reverse("medication-list", args=())
        return redirect(redirect_url)
        
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "medication_list": edited_medication_list,
        "test_notifications": test_notifications
    }
    return render(request, 'stock/medication_list.html', context)

def edit_medication_entry(request, med_id):
    medication = Medication.objects.get(id=med_id)
    
    if request.method == "POST":
        name = request.POST["name"]
        brand = request.POST["brand"] if request.POST["brand"] != "" else "None"
        formulation = request.POST["formulation"]
        strength = request.POST["strength"]
        units = request.POST["units"]
        
        #updating and saving the medication entry
        medication.name = name
        medication.brand = brand
        medication.formulation = formulation
        medication.strength_value = strength
        medication.strength_value_units = units
        medication.save()
        
        messages.success(request, "Medication Updated Successfully")
        redirect_url=reverse("edit-medication", args=(med_id, ))
        return redirect(redirect_url)
        

    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "medication": medication 
    }
    print(medication)
    return render(request, 'stock/edit_medication_entry.html', context)

def update_quantity_page(request, med_id):
    medication = Medication.objects.get(id=med_id)
    
    if request.method == "POST":
        quantity = request.POST["quantity"]
        medication.quantity += int(quantity)
        medication.save()
        
        messages.success(request, "Quantity Updated Successfully")
        redirect_url=reverse("edit-medication", args=(med_id, ))
        return redirect(redirect_url)
        
        