from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from base.models import Patient, PatientRecord, PatientVital
import math
from django.core.paginator import Paginator
from django.urls import reverse


date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_page(request, page=1):
    all_patients = Patient.objects.all()
    patients = Paginator(all_patients, 24)
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patients": patients.page(page)
    }
    return render(request, 'base/application_page.html', context)



def new_patient_page(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        sex = request.POST["sex"]
        nationality = request.POST["nationality"]
        phone_number = request.POST["phone_number"]
        date_of_birth = request.POST["date_of_birth"]
        
        days=(datetime.datetime.now() - datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")).days
        age = math.floor(days/365)
        
        patient1 = Patient(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            nationality=nationality,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            age=age
        )
        
        patient1.save()
        messages.success(request, "Patient Profile Created Successfully")
        redirect_url=reverse('application-page', args=(1,))
        return redirect(redirect_url)
    else:
        return render(request, 'base/new_patient.html', date)



def new_patient_vital_page(request, patient_id):
    if request.method == "POST":
        patient = Patient.objects.get(id=patient_id)
        temperature = request.POST["temperature"]
        weight = request.POST["weight"]
        pulse = request.POST["pulse"]
        bp_sys = request.POST["systolic_blood_pressure"]
        bp_dias = request.POST["diastolic_blood_pressure"]
        
        if temperature == "" and weight=="" and pulse=="" and bp_sys=="" and bp_dias == "":
            redirect_url=reverse('patient-page', args=(patient_id,))
            return redirect(redirect_url)
        
        if temperature=="":
            temperature=None
        if weight=="":
            weight=None
        if pulse=="":
            pulse=None
        if bp_sys=="":
            bp_sys=None
        if bp_dias=="":
            bp_dias=None
        
        vitals = PatientVital(patient=patient,
                              doctor=request.user,
                              pulse_bpm=pulse,
                              temperature=temperature,
                              weight=weight,
                              systolic_blood_pressure=bp_sys,
                              diastolic_blood_pressure=bp_dias)
        vitals.save()
        messages.success(request, "Vital Record Has Been Added")
    redirect_url=reverse('patient-page', args=(patient_id,))
    return redirect(redirect_url)


def edit_vitals_page(request, patient_id, vital_id):
    vital = PatientVital.objects.get(id=vital_id)
    patient = Patient.objects.get(id=patient_id)
    
    if request.method == "POST":
        temperature = request.POST["temperature"]
        weight = request.POST["weight"]
        pulse = request.POST["pulse"]
        bp_sys = request.POST["systolic_blood_pressure"]
        bp_dias = request.POST["diastolic_blood_pressure"]
        
        if temperature == "" and weight=="" and pulse=="" and bp_sys=="" and bp_dias == "":
            redirect_url=reverse('patient-page', args=(patient_id,))
            return redirect(redirect_url)
        
        if temperature=="":
            temperature=None
        if weight=="":
            weight=None
        if pulse=="":
            pulse=None
        if bp_sys=="":
            bp_sys=None
        if bp_dias=="":
            bp_dias=None
        
        vital.temperature = temperature
        vital.weight = weight
        vital.pulse_bpm = pulse
        vital.systolic_blood_pressure = bp_sys
        vital.diastolic_blood_pressure = bp_dias
        vital.save()
        messages.success(request, "Vitals Have Been Updated Successfully")
        redirect_url=reverse('patient-page', args=(patient_id,))
        return redirect(redirect_url)
    else:
        context = {
            "vital": vital
        }
        return render(request, 'base/edit_vitals_record.html', context)



def new_patient_record_page(request, patient_id):
    if request.method == "POST":
        signs_and_symptoms = ", ".join(request.POST["signs_and_symptoms"].split("\r\n"))
        tests_for = ", ".join(request.POST["tests_for"].split("\r\n"))
        test_methods = ", ".join(request.POST["test_methods"].split("\r\n"))
        test_results = ", ".join(request.POST["test_results"].split("\r\n"))
        prescriptions = ", ".join(request.POST["prescriptions"].split("\r\n"))
        patient=Patient.objects.get(id=patient_id)
        
        if tests_for=="":
            test_for = None
        if test_methods=="":
            test_methods=None
            
        medical_record = PatientRecord(patient=patient,
                                       doctor=request.user,
                                       signs_and_symptoms=signs_and_symptoms,
                                       tests_for=tests_for,
                                       test_methods=test_methods,
                                       test_results=test_results,
                                       prescriptions=prescriptions)
        medical_record.save()
        redirect_url = reverse('patient-page', args=(patient_id,))
        return redirect(redirect_url)
    
def edit_patient_record_page(request, patient_id, record_id):
    record = PatientRecord.objects.get(id=record_id)
    
    if request.method == "POST":
        signs_and_symptoms = ", ".join(request.POST["signs_and_symptoms"].split("\r\n"))
        tests_for = ", ".join(request.POST["tests_for"].split("\r\n"))
        test_methods = ", ".join(request.POST["test_methods"].split("\r\n"))
        test_results = ", ".join(request.POST["test_results"].split("\r\n"))
        prescriptions = ", ".join(request.POST["prescriptions"].split("\r\n"))
        
        if tests_for=="":
            test_for = None
        if test_methods=="":
            test_methods=None
        
        record.signs_and_symptoms = signs_and_symptoms
        record.tests_for = tests_for
        record.test_methods = test_methods
        record.test_results = test_results
        record.prescriptions = prescriptions
        record.save()
        messages.success(request, "Your Record Has Been Updated Successfully")    
        redirect_url = reverse('patient-page', args=(patient_id,))
        return redirect(redirect_url)
    else:
        context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record
        }
        return render(request, 'base/edit_medical_record.html', context)


def patient_page(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    
    vitals = list(PatientVital.objects.filter(patient=patient).order_by("date_added", "time_added"))[-5:]
    medical_records = PatientRecord.objects.filter(patient=patient).order_by("-date_added", "-time_added")
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patient": patient,
        "vitals": vitals,
        "medical_records": medical_records
    }
    return render(request, 'base/patient_page.html', context)


def patient_vitals_page(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    vitals = PatientVital.objects.filter(patient=patient).order_by('-date_added')
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patient": patient,
        "vitals": vitals
    }
    
    return render(request, 'base/vitals_page.html', context)

def medical_record_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "patient": patient
    }
    
    return render(request, 'base/medical_record_page.html', context)

def bill_patient_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "patient": patient
    }
    return render(request, 'base/bill_patient_page.html', context)