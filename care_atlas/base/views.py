from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from base.models import Patient, PatientRecord, PatientVital, PatientBill
from users.models import HospitalProfile
import math
from django.core.paginator import Paginator
from django.urls import reverse
import json
from fractions import Fraction
from base.utils import file_handler
import os
from django.conf import settings
from stock.models import Medication

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}



# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_patient_page(request, page=1):
    all_patients = Patient.objects.all().order_by('-date_added')
    patients = Paginator(all_patients, 24)
    
    #getting records awaiting results
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
        "patients": patients.page(page),
        "test_notifications": test_notifications
    }
    return render(request, 'base/application_patient_page.html', context)


def application_home_page(request):
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    today_records = PatientRecord.objects.filter(doctor__in=doctors).filter(date_added=datetime.datetime.now().date())
    all_records = PatientRecord.objects.filter(doctor__in=doctors)
    
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
        
    #getting monthly number of clients for past 6 months
    _date = datetime.datetime.now().date()
    client_totals = []
    for i in range(6):
        count = 0
        for j in all_records:
            if j.date_added.month == _date.month:
                count += 1
        client_totals.append(count)
        _date = _date - datetime.timedelta(days=_date.day) 
    client_totals.reverse()
    
    #getting list of previous six months
    months = ['JUL', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
    current_month = datetime.datetime.now().month - 1
    current_month_index = current_month + 6
    last_six_months = months[(current_month_index-5):current_month_index+1]
    
    # getting male clients, female clients, client ages in current year
    current_year_records = [j for j in all_records if j.date_added.year == datetime.datetime.now().year]
    if current_year_records != []:
        male_clients = [x for x in current_year_records if x.patient.sex == 'Male']
        female_clients = [x for x in current_year_records if x.patient.sex == 'Female']
    
        ages = []
        for i in current_year_records:
            if i.patient.date_of_birth:
                patient_age = int((datetime.datetime.now().date() - i.patient.date_of_birth).days/365)
                ages.append(patient_age)
                
        
        if len(female_clients) == 0 and len(male_clients) != 0:
            male_rep = 1
            female_rep = 0
        elif len(male_clients) == 0 and len(female_clients) !=0:
            female_rep = 1
            male_rep = 0
        elif len(male_clients) == 0 and len(female_clients) == 0:
            male_rep = 0
            female_rep = 0
        elif len(male_clients) != 0 and len(female_clients) != 0:
            gender_ratio = Fraction(len(male_clients), len(female_clients))
            male_rep = gender_ratio.numerator
            female_rep = gender_ratio.denominator       
        
        average_age = int(sum(ages)/len(ages)) if len(ages) != 0 else "CBD" 
                    
        context = {
            "day": date_1[0],
            "day_of_month": date_1[1],
            "month": date_1[2],
            "year": date_1[3].replace(",", ""),
            "date": date,
            "days_patient_num": len(list(today_records)),
            "male_rep": male_rep,
            "female_rep": female_rep,
            "average_age": average_age,
            "last_six_months": json.dumps(last_six_months, ensure_ascii=False),
            "client_totals": json.dumps(client_totals),
            "test_notifications": test_notifications
        }
    else:        
        context = {
            "day": date_1[0],
            "day_of_month": date_1[1],
            "month": date_1[2],
            "year": date_1[3].replace(",", ""),
            "date": date,
            "days_patient_num": len(list(today_records)),
            "male_ratio": 0,
            "female_ratio": 0,
            "average_age": 0,
            "last_six_months": json.dumps(last_six_months, ensure_ascii=False),
            "client_totals": json.dumps(client_totals),
            "test_notifications": test_notifications
        }
    return render(request, 'base/application_home_page.html', context)


def new_patient_page(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        sex = request.POST["sex"]
        nationality = request.POST["nationality"]
        phone_number = request.POST["phone_number"]        
        date_of_birth = request.POST["date_of_birth"] if date_of_birth != "" else "null"
        address = request.POST["address"]
        next_of_kin = request.POST["next_of_kin"]
        next_of_kin_contact = request.POST["next_of_kin_contact"]
        religion = request.POST["religion"]
        
        
        patient1 = Patient(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            nationality=nationality,
            phone_number=phone_number,
            address=address,
            next_of_kin=next_of_kin,
            next_of_kin_contact=next_of_kin_contact,
            religion=religion
        )
        
        if date_of_birth != "":
                patient1.date_of_birth=date_of_birth
                patient1.save()
            
        patient1.save()
        messages.success(request, "Patient Profile Created Successfully")
        redirect_url=reverse('application-page', args=(1,))
        return redirect(redirect_url)
    else:
        #getting records awaiting results
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
            "test_notifications": test_notifications
        }
        return render(request, 'base/new_patient.html', context)

   
def edit_patient_profile_page(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
     
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        sex = request.POST["sex"]
        nationality = request.POST["nationality"]
        phone_number = request.POST["phone_number"]        
        date_of_birth = request.POST["date_of_birth"]
        address = request.POST["address"]
        next_of_kin = request.POST["next_of_kin"]
        next_of_kin_contact = request.POST["next_of_kin_contact"]
        religion = request.POST["religion"]
        
        patient.first_name=first_name
        patient.last_name=last_name
        patient.sex=sex
        patient.nationality=nationality
        patient.phone_number=phone_number
        patient.address=address
        patient.next_of_kin=next_of_kin
        patient.next_of_kin_contact=next_of_kin_contact
        patient.religion=religion
        
        if date_of_birth != "":
            patient.date_of_birth=date_of_birth
            
        patient.save()
        
        messages.success(request, "Patient Profile Updated Successfully")
        redirect_url=reverse('patient-page', args=(patient_id,))
        return redirect(redirect_url)    
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patient": patient,
        "test_notifications": test_notifications
    }
    return render(request, 'base/edit_patient_profile.html', context)



def new_patient_vital_page(request, patient_id):
    if request.method == "POST":
        patient = Patient.objects.get(id=patient_id)
        temperature = request.POST["temperature"]
        weight = request.POST["weight"]
        pulse = request.POST["pulse"]
        bp_sys = request.POST["systolic_blood_pressure"]
        bp_dias = request.POST["diastolic_blood_pressure"]
        oxygen_saturation = request.POST["oxygen_saturation"]
        
        if temperature == "" and weight=="" and pulse=="" and bp_sys=="" and bp_dias == "" and oxygen_saturation == "":
            redirect_url=reverse('patient-page', args=(patient_id,))
            return redirect(redirect_url)
        
        if temperature=="":
            temperature = 0
        if weight=="":
            weight=None
        if pulse=="":
            pulse=None
        if bp_sys=="":
            bp_sys=None
        if bp_dias=="":
            bp_dias=None
        if oxygen_saturation == "":
            oxygen_saturation = 0
        
        vitals = PatientVital(patient=patient,
                              doctor=request.user,
                              pulse_bpm=pulse,
                              temperature=float(temperature),
                              weight=weight,
                              systolic_blood_pressure=bp_sys,
                              diastolic_blood_pressure=bp_dias,
                              oxygen_saturation=float(oxygen_saturation)
                              )
        vitals.save()
        messages.success(request, "Vital Record Has Been Added")
    redirect_url=reverse('patient-page', args=(patient_id,))
    return redirect(redirect_url)


def edit_vitals_page(request, patient_id, vital_id):
    vital = PatientVital.objects.get(id=vital_id)
    patient = Patient.objects.get(id=patient_id)
    
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if request.method == "POST":
        temperature = request.POST["temperature"]
        weight = request.POST["weight"]
        pulse = request.POST["pulse"]
        bp_sys = request.POST["systolic_blood_pressure"]
        bp_dias = request.POST["diastolic_blood_pressure"]
        oxygen_saturation = request.POST["oxygen_saturation"]
        
        if temperature == "" and weight=="" and pulse=="" and bp_sys=="" and bp_dias == "" and oxygen_saturation=="":
            redirect_url=reverse('patient-page', args=(patient_id,))
            return redirect(redirect_url)
        
        if temperature=="":
            temperature = 0
        if weight=="":
            weight=None
        if pulse=="":
            pulse=None
        if bp_sys=="":
            bp_sys=None
        if bp_dias=="":
            bp_dias=None
        if oxygen_saturation == "":
            oxygen_saturation = 0
        
        vital.temperature = float(temperature)
        vital.weight = weight
        vital.pulse_bpm = pulse
        vital.systolic_blood_pressure = bp_sys
        vital.diastolic_blood_pressure = bp_dias
        vital.oxygen_saturation = float(oxygen_saturation)
        vital.save()
        messages.success(request, "Vitals Have Been Updated Successfully")
        redirect_url=reverse('patient-page', args=(patient_id,))
        return redirect(redirect_url)
    else:
        context = {
            "vital": vital,
            "test_notifications": test_notifications
        }
        return render(request, 'base/edit_vitals_record.html', context)



def new_patient_record_page(request, patient_id):
    if request.method == "POST":
        # getting medical history data from form
        medical_history = ", ".join(request.POST["medical_history"].split("\r\n")) if request.POST["medical_history"] != "" else "None"
        surgical_history = ", ".join(request.POST["surgical_history"].split("\r\n")) if request.POST["surgical_history"] != "" else "None"
        gyn_obs_history = ", ".join(request.POST["gyn_obs_history"].split("\r\n")) if request.POST["gyn_obs_history"] != "" else "None"
        family_history = ", ".join(request.POST["family_history"].split("\r\n")) if request.POST["family_history"] != "" else "None"
        social_history = ", ".join(request.POST["social_history"].split("\r\n")) if request.POST["social_history"] != "" else "None"
        
        # getting medical record data from form
        signs_and_symptoms = ", ".join(request.POST["signs_and_symptoms"].split("\r\n")) if request.POST["signs_and_symptoms"] != "" else "None"
        impressions = ", ".join(request.POST["impressions"].split("\r\n")) if request.POST["impressions"] != "" else "None"
        investigations = ", ".join(request.POST["investigations"].split("\r\n")) if request.POST["investigations"] != "" else "None"
        test_results = ", ".join(request.POST["test_results"].split("\r\n")) if request.POST["test_results"] != "" else "None"
        
        if "test_attachments" in request.FILES:
            test_attachments = request.FILES.getlist("test_attachments")
            test_attachments_name_s = file_handler(test_attachments)
            test_attachments_name_s_string = "---".join(test_attachments_name_s)
        
        conclusions = ", ".join(request.POST["conclusions"].split("\r\n")) if request.POST["conclusions"] != "" else "None"
        
        #obtaining management information
        mgt_meds = ", ".join(request.POST["mgt_meds"].split("\r\n")) if request.POST["mgt_meds"] != "" else "None"    
        mgt_surg = ", ".join(request.POST["mgt_surg"].split("\r\n")) if request.POST["mgt_surg"] != "" else "None"     
        mgt_ther = ", ".join(request.POST["mgt_ther"].split("\r\n")) if request.POST["mgt_ther"] != "" else "None"     
        mgt_other = ", ".join(request.POST["mgt_other"].split("\r\n")) if request.POST["mgt_other"] != "" else "None"     
                
        management = "---".join([mgt_meds, mgt_surg, mgt_ther, mgt_other])
        
        patient=Patient.objects.get(id=patient_id)
         
        if "test_attachments" in request.FILES:
            medical_record = PatientRecord(patient=patient,
                                        doctor=request.user,
                                        signs_and_symptoms=signs_and_symptoms,
                                        impressions=impressions,
                                        investigations=investigations,
                                        test_results=test_results,
                                        conclusions=conclusions,
                                        management=management,
                                        medical_history=medical_history,
                                        surgical_history=surgical_history,
                                        gyn_obs_history=gyn_obs_history,
                                        family_history=family_history,
                                        social_history=social_history,
                                        test_attachments=test_attachments_name_s_string
                                        )
        else:
            medical_record = PatientRecord(patient=patient,
                            doctor=request.user,
                            signs_and_symptoms=signs_and_symptoms,
                            impressions=impressions,
                            investigations=investigations,
                            test_results=test_results,
                            conclusions=conclusions,
                            management=management,
                            medical_history=medical_history,
                            surgical_history=surgical_history,
                            gyn_obs_history=gyn_obs_history,
                            family_history=family_history,
                            social_history=social_history
                            )
        medical_record.save()
        redirect_url = reverse('patient-page', args=(patient_id,))
        return redirect(redirect_url)
    
def edit_patient_record_page(request, patient_id, record_id):
    record = PatientRecord.objects.get(id=record_id)
    
    #separating record management field into groups / list
    mgt = record.management.split("---") if record.management not in ["Awaiting Test Results", "Awaiting Doctors Recommendations"] else ["TBD", "TBD", "TBD", "TBD"]
    
    #accessing records pending doctors conclusions or awaiting test results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    #creating list of record test attachments paths
    test_attachments_list = (record.test_attachments).split("---") if record.test_attachments != None else []
    attachment_paths = []
    for k in test_attachments_list:
        path_1 = f"base/files/{k}"
        attachment_paths.append(path_1)
    
    if request.method == "POST":
        # getting medical history data from form
        medical_history = ", ".join(request.POST["medical_history"].split("\r\n")) if request.POST["medical_history"] != "" else "None"
        surgical_history = ", ".join(request.POST["surgical_history"].split("\r\n")) if request.POST["surgical_history"] != "" else "None"
        gyn_obs_history = ", ".join(request.POST["gyn_obs_history"].split("\r\n")) if request.POST["gyn_obs_history"] != "" else "None"
        family_history = ", ".join(request.POST["family_history"].split("\r\n")) if request.POST["family_history"] != "" else "None"
        social_history = ", ".join(request.POST["social_history"].split("\r\n")) if request.POST["social_history"] != "" else "None"
        
        # getting medical record data from form
        signs_and_symptoms = ", ".join(request.POST["signs_and_symptoms"].split("\r\n")) if request.POST["signs_and_symptoms"] != "" else "None"
        impressions = ", ".join(request.POST["impressions"].split("\r\n")) if request.POST["impressions"] != "" else "None"
        investigations = ", ".join(request.POST["investigations"].split("\r\n")) if request.POST["investigations"] != "" else "None"
        test_results = ", ".join(request.POST["test_results"].split("\r\n")) if     request.POST["test_results"] != "" else "None"

        #getting attachments uploaded
        if "test_attachments" in request.FILES:
            test_attachments = request.FILES.getlist("test_attachments")
            test_attachments_name_s = file_handler(test_attachments)
            test_attachments_name_s_string = "---".join(test_attachments_name_s)
        else:
            test_attachments_name_s_string = None
        
        conclusions = ", ".join(request.POST["conclusions"].split("\r\n")) if request.POST["conclusions"] != "" else "None"
        
        #getting management data
        mgt_meds = ", ".join(request.POST["mgt_meds"].split("\r\n")) if request.POST["mgt_meds"] != "" else "None"    
        mgt_surg = ", ".join(request.POST["mgt_surg"].split("\r\n")) if request.POST["mgt_surg"] != "" else "None"     
        mgt_ther = ", ".join(request.POST["mgt_ther"].split("\r\n")) if request.POST["mgt_ther"] != "" else "None"     
        mgt_other = ", ".join(request.POST["mgt_other"].split("\r\n")) if request.POST["mgt_other"] != "" else "None"     
                
        management = "---".join([mgt_meds, mgt_surg, mgt_ther, mgt_other])
        
        # editing / updating medical record
        record.medical_history = medical_history
        record.surgical_history = surgical_history
        record.gyn_obs_history = gyn_obs_history
        record.family_history = family_history
        record.social_history = social_history
        record.signs_and_symptoms = signs_and_symptoms
        record.impressions = impressions
        record.investigations = investigations
        record.test_results = test_results
        record.conclusions = conclusions
        record.management = management
        
        #updating attachment list
        if test_attachments_name_s_string != None:
            if record.test_attachments != None:
                record.test_attachments = record.test_attachments + f"---{test_attachments_name_s_string}"
            else:
                record.test_attachments = test_attachments_name_s_string
        
        record.save()
        
        if record.test_results != "Awaiting Test Results" or record.conclusions != "Awaiting Test Results" or record.management != "Awaiting Test Results":
            record.record_status = None
            record.save()
        
        messages.success(request, "Your Record Has Been Updated Successfully")    
        redirect_url = reverse('medical-record-page', args=(patient_id, record_id))
        return redirect(redirect_url)
    else:
        context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "test_notifications": test_notifications,
        "mgt_meds": mgt[0],
        "mgt_surg": mgt[1],
        "mgt_ther": mgt[2],
        "mgt_other": mgt[3],
        "attachment_paths": attachment_paths,
        "test_attachments_list": test_attachments_list
        }
        return render(request, 'base/edit_medical_record.html', context)


def patient_page(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    
    vitals = list(PatientVital.objects.filter(patient=patient).order_by("date_added", "time_added"))[-5:]
    medical_records = PatientRecord.objects.filter(patient=patient).order_by("-date_added", "-time_added")
    medications = Medication.objects.filter(hospital=request.user.hospitalprofile.hospital_name).order_by("name")
    medical_records_edited = []
    for rec in medical_records:
        mgt_list = rec.management.split("---") if rec.management not in ["Awaiting Test Results", "Awaiting Doctors Recommendations"] else ["TBD", "TBD", "TBD", "TBD"]
        mgt = f"Medical: {mgt_list[0]}, Surgical: {mgt_list[1]}, Therapy: {mgt_list[2]}, Other: {mgt_list[3]}"
        rec.management = mgt
        medical_records_edited.append(rec)
    
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = ''
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patient": patient,
        "vitals": vitals,
        "medical_records": medical_records_edited,
        "patient_age": patient_age,
        "test_notifications": test_notifications,
        "medications": medications,
        "vitals_length": len(vitals),
        "medical_records_length": len(medical_records_edited)
    }
    return render(request, 'base/patient_page.html', context)


def patient_vitals_page(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    vitals = PatientVital.objects.filter(patient=patient).order_by('-date_added')
    
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patient": patient,
        "vitals": vitals,
        "patient_age": patient_age,
        "test_notifications": test_notifications
    }
    
    return render(request, 'base/vitals_page.html', context)

def medical_record_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    bill = PatientBill.objects.filter(medical_record=record).first()
    
    mgt = record.management.split("---") if record.management not in ["Awaiting Test Results", "Awaiting Doctors Recommendations"] else ["TBD", "TBD", "TBD", "TBD"]
    
    #getting records awaiting results or awaiting doctors conclusions
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    #creating list of record test attachments paths
    test_attachments_list = (record.test_attachments).split("---") if record.test_attachments != None else []

    attachment_paths = []
    for k in test_attachments_list:
        path_1 = os.path.join(settings.BASE_DIR, "media", k)
        attachment_paths.append(path_1)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "patient": patient,
        "bill": bill,
        "patient_age": patient_age,
        "test_notifications": test_notifications,
        "mgt_meds": mgt[0],
        "mgt_surg": mgt[1],
        "mgt_ther": mgt[2],
        "mgt_other": mgt[3],
        "attachment_paths": attachment_paths,
        "attachment_number": len(test_attachments_list),
        "test_attachments_list": test_attachments_list
    }
    
    return render(request, 'base/medical_record_page.html', context)

def bill_patient_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    bill_rec = list(PatientBill.objects.filter(medical_record=record))
    
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
    
    if len(bill_rec) != 0:
        redirect_url = reverse('medical-record-page', args=(patient_id, record_id))
        return redirect(redirect_url)
    
    
    if request.method == "POST":
        consultation_fees = int(request.POST['consultation_fees']) if request.POST['consultation_fees'] !="" else 0
        
        #getting diagnostic tests and their fees
        test_1 = request.POST['test_1']
        test_cost_1 = int(request.POST['test_cost_1']) if request.POST['test_cost_1'] != "" else 0
                
        test_2 = request.POST['test_2']
        test_cost_2 = int(request.POST['test_cost_2']) if request.POST['test_cost_2'] != "" else 0
        
        test_3 = request.POST['test_3']
        test_cost_3 = int(request.POST['test_cost_3']) if request.POST['test_cost_3'] != "" else 0
        
        test_4 = request.POST['test_4']
        test_cost_4 = int(request.POST['test_cost_4']) if request.POST['test_cost_4'] != "" else 0
        
        test_5 = request.POST['test_5']
        test_cost_5 = int(request.POST['test_cost_5']) if request.POST['test_cost_5'] != "" else 0
        
        test_list = ", ".join([test_1, test_2, test_3, test_4, test_5])
        test_cost_list = ", ".join([str(test_cost_1), str(test_cost_2), str(test_cost_3), str(test_cost_4), str(test_cost_5)])

        diagnostic_test_fees = test_cost_1 + test_cost_2 + test_cost_3 + test_cost_4 + test_cost_5
        
        #getting remaining bill inputs       
        nursing_care_fees = int(request.POST['nursing_care_fees']) if request.POST['nursing_care_fees'] != "" else 0
        
        #getting medication fees
        md_fees = int(request.POST['md_fees']) if request.POST['md_fees'] != "" else 0
        sg_fees = int(request.POST['sg_fees']) if request.POST['sg_fees'] != "" else 0
        th_fees = int(request.POST['th_fees']) if request.POST['th_fees'] != "" else 0
        medication_fees_list = str(md_fees) + "---" + str(sg_fees) + "---" + str(th_fees)
        medication_fees = md_fees + sg_fees + th_fees
        
        
        specific_charges = request.POST['specific_charges'] if request.POST['specific_charges'] != "" else "Other Charges"
        specific_charge_fees = int(request.POST['specific_charge_fees']) if request.POST['specific_charge_fees'] != "" else 0
        total_charges = consultation_fees+diagnostic_test_fees+nursing_care_fees+medication_fees+specific_charge_fees
        
        patient_bill = PatientBill(
            patient = patient,
            doctor = request.user,
            medical_record = record,
            consultation_fees = consultation_fees,
            test_list = test_list,
            test_cost_list = test_cost_list,
            diagnostic_test_fees = diagnostic_test_fees,
            nursing_care_fees = nursing_care_fees,
            medication_fees_list = medication_fees_list,
            medication_fees = medication_fees,
            specific_charges = specific_charges,
            specific_charge_fees = specific_charge_fees,
            total_charges = total_charges
        )
        patient_bill.save()
        messages.success(request, "your Bill Was Generated Succesfully")
        redirect_url = reverse('patient-bill-page', args=(patient_id, record_id, patient_bill.id))
        return redirect(redirect_url)
    else:    
        context = {
            "day": date_1[0],
            "day_of_month": date_1[1],
            "month": date_1[2],
            "year": date_1[3].replace(",", ""),
            "date": date,
            "record": record,
            "patient": patient,
            "patient_age": patient_age,
            "test_notifications": test_notifications
        }
        return render(request, 'base/bill_patient_page.html', context)

def patient_bill_page(request, patient_id, record_id, bill_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    bill = PatientBill.objects.get(id=bill_id)
    
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
    
    test_list = bill.test_list.split(", ")
    test_list_filtered = [i for i in test_list if i != ""]
    
    test_cost_list = bill.test_cost_list.split(", ")
    test_cost_list_filtered = [j for j in test_cost_list if j != "0"]
    
    test_dict = dict(zip(test_list, test_cost_list))

    medication_fees_list = (bill.medication_fees_list).split("---") if bill.medication_fees_list != None else []
    medication_fees_dict = {"meds": medication_fees_list[0], "surg": medication_fees_list[1], "ther": medication_fees_list[2]}
        
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "patient": patient,
        "bill": bill,
        "patient_age": patient_age,
        "test_notifications": test_notifications,
        "test_list_filtered": test_list_filtered,
        "test_cost_list_filtered": test_cost_list,
        "test_1": test_list[0],
        "test_2": test_list[1],
        "test_3": test_list[2],
        "test_4": test_list[3],
        "test_5": test_list[4],
        "test_cost_1": test_cost_list[0],
        "test_cost_2": test_cost_list[1],
        "test_cost_3": test_cost_list[2],
        "test_cost_4": test_cost_list[3],
        "test_cost_5": test_cost_list[4],
        "medication_fees_list": medication_fees_list,
        "medication_fees_dict": medication_fees_dict
    }
    return render(request, 'base/patient_bill_page.html', context)

def edit_patient_bill_page(request, patient_id, record_id, bill_id):
    bill = PatientBill.objects.get(id=bill_id)
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    if request.method == "POST":
        consultation_fees = int(request.POST['consultation_fees']) if request.POST['consultation_fees'] !="" else 0
        
        #getting diagnostic tests and their fees
        test_1 = request.POST['test_1']
        test_cost_1 = int(request.POST['test_cost_1']) if request.POST['test_cost_1'] != "" else 0
                
        test_2 = request.POST['test_2']
        test_cost_2 = int(request.POST['test_cost_2']) if request.POST['test_cost_2'] != "" else 0
        
        test_3 = request.POST['test_3']
        test_cost_3 = int(request.POST['test_cost_3']) if request.POST['test_cost_3'] != "" else 0
        
        test_4 = request.POST['test_4']
        test_cost_4 = int(request.POST['test_cost_4']) if request.POST['test_cost_4'] != "" else 0
        
        test_5 = request.POST['test_5']
        test_cost_5 = int(request.POST['test_cost_5']) if request.POST['test_cost_5'] != "" else 0
        
        test_list = ", ".join([test_1, test_2, test_3, test_4, test_5])
        test_cost_list = ", ".join([str(test_cost_1), str(test_cost_2), str(test_cost_3), str(test_cost_4), str(test_cost_5)])

        diagnostic_test_fees = test_cost_1 + test_cost_2 + test_cost_3 + test_cost_4 + test_cost_5
        
        #getting remaining bill inputs       
        nursing_care_fees = int(request.POST['nursing_care_fees']) if request.POST['nursing_care_fees'] != "" else 0
        
        #getting medication fees        
        md_fees = int(request.POST['md_fees']) if request.POST['md_fees'] != "" else 0
        sg_fees = int(request.POST['sg_fees']) if request.POST['sg_fees'] != "" else 0
        th_fees = int(request.POST['th_fees']) if request.POST['th_fees'] != "" else 0
        medication_fees_list = str(md_fees) + "---" + str(sg_fees) + "---" + str(th_fees)
        medication_fees = md_fees + sg_fees + th_fees
        
        specific_charges = request.POST['specific_charges'] if request.POST['specific_charges'] != "" else "Other Charges"
        specific_charge_fees = int(request.POST['specific_charge_fees']) if request.POST['specific_charge_fees'] != "" else 0
        
        #updating bill record
        bill.consultation_fees = consultation_fees
        bill.diagnostic_test_fees = diagnostic_test_fees
        bill.nursing_care_fees = nursing_care_fees
        bill.medication_fees = medication_fees
        bill.specific_charges = specific_charges
        bill.specific_charge_fees = specific_charge_fees
        bill.total_charges = consultation_fees+diagnostic_test_fees+nursing_care_fees+medication_fees+specific_charge_fees
        bill.test_list = test_list
        bill.test_cost_list = test_cost_list
        bill.medication_fees_list = medication_fees_list
        
        bill.save()
        
        redirect_url = reverse('patient-bill-page', args=(patient.id, record.id, bill.id))
        return redirect(redirect_url)
    

def bills_page(request, page):
    #getting bills for users hospital
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    all_bills = PatientBill.objects.filter(doctor__in=doctors).order_by("-date_added", "-time_added")
    
    bills = Paginator(all_bills, 10)
    
    #getting records awaiting results
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "all_bills": bills.page(page),
        "test_notifications": test_notifications
    }
    return render(request, 'base/bills_page.html', context)


def records_page(request, page=1):
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    records_ = PatientRecord.objects.filter(doctor__in=doctors).order_by("-date_added", "-time_added")
    
    for rec in records_:
        mgt_list = rec.management.split("---") if rec.management not in ["Awaiting Test Results", "Awaiting Doctors Recommendations"] else ["TBD", "TBD", "TBD", "TBD"]
        mgt = f"Medical: {mgt_list[0]}, Surgical: {mgt_list[1]}, Therapy: {mgt_list[2]}, Other: {mgt_list[3]}"
        rec.management = mgt
    
    records = Paginator(records_, 10)
    
    #getting records awaiting results
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "medical_records": records.page(page),
        "test_notifications": test_notifications
        }
    return render(request, 'base/records_page.html', context)


def search_page(request, page=1, search_string=""):
    #getting records awaiting results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if request.method == "POST":
        search_string = request.POST['search_string']
        if search_string == "":
            redirect_url=reverse('application-page', args=(1,))
            return redirect(redirect_url)
    else:
        search_string = search_string
    names = search_string.split(' ')
    search_results = []
    if len(names) > 1:
        search_results.extend(Patient.objects.filter(first_name__icontains=names[0], last_name__icontains=names[1]))
        search_results.extend(Patient.objects.filter(last_name__icontains=names[0], first_name__icontains=names[1]))
    else:
        search_results.extend(Patient.objects.filter(first_name__icontains=names[0]))
        search_results.extend(Patient.objects.filter(last_name__icontains=names[0]))            
            
    patients = Paginator(search_results, 12)
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patients": patients.page(page),
        "number_found": len(list(search_results)),
        "search_text": search_string,
        "test_notifications":  test_notifications
    }
    return render(request, 'base/search_result.html', context)

def order_tests_page(request, patient_id):
    if request.method == "POST":
        # getting medical history data from form
        medical_history = ", ".join(request.POST["medical_history"].split("\r\n"))
        surgical_history = ", ".join(request.POST["surgical_history"].split("\r\n"))
        gyn_obs_history = ", ".join(request.POST["gyn_obs_history"].split("\r\n"))
        family_history = ", ".join(request.POST["family_history"].split("\r\n"))
        social_history = ", ".join(request.POST["social_history"].split("\r\n"))
        
        # getting medical record data from form
        signs_and_symptoms = ", ".join(request.POST["signs_and_symptoms"].split("\r\n"))
        impressions = ", ".join(request.POST["impressions"].split("\r\n"))
        investigations = ", ".join(request.POST["investigations"].split("\r\n"))      
        
        patient=Patient.objects.get(id=patient_id)
            
        medical_record = PatientRecord(patient=patient,
                                    doctor=request.user,
                                    signs_and_symptoms=signs_and_symptoms,
                                    impressions=impressions,
                                    investigations=investigations,
                                    test_results="Awaiting Test Results",
                                    conclusions="Awaiting Test Results",
                                    management="Awaiting Test Results",
                                    medical_history=medical_history,
                                    surgical_history=surgical_history,
                                    gyn_obs_history=gyn_obs_history,
                                    family_history=family_history,
                                    social_history=social_history,
                                    record_status="Awaiting Test Results"
                                    )
        medical_record.save()    
    
    messages.success(request, "Tests Have Been Requested Successfully")
    redirect_url = reverse('patient-page', args=(patient_id, ))
    return redirect(redirect_url)

def investigations_update_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    #getting records awaiting test results
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    
    values = ["Tests Done Successfully!", "Awaiting Test Results"]
    test_notifications = PatientRecord.objects.filter(doctor__in=doctors).filter(record_status__in=values)
    
    if request.method == 'POST':
        test_results = ", ".join(request.POST["test_results"].split("\r\n"))
        
        if "test_attachments" in request.FILES:
            test_attachments = request.FILES.getlist("test_attachments")
            test_attachments_name_s = file_handler(test_attachments)
            test_attachments_name_s_string = "---".join(test_attachments_name_s)
        else:
            test_attachments_name_s_string = None
        
        record.test_results = test_results
        record.test_attachments=test_attachments_name_s_string
        record.conclusions = "Awaiting Doctors Conclusion"
        record.management = "Awaiting Doctors Recommendations"
        record.record_status = "Tests Done Successfully!"
        record.save()
        
        messages.success(request, "Tests Results Updated Successfully")
        redirect_url = reverse('patient-page', args=(patient_id, ))
        return redirect(redirect_url)

        
    context = {
            "day": date_1[0],
            "day_of_month": date_1[1],
            "month": date_1[2],
            "year": date_1[3].replace(",", ""),
            "date": date,
            "record": record,
            "patient": patient,
            "test_notifications": test_notifications
    }
    return render(request, 'base/investigations_update.html', context)


def delete_attachment(request, patient_id, record_id, attachment):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
      
    #getting list attachments from database
    attachment_list = (record.test_attachments).split("---") if record.test_attachments != None else []
    
    #removing attachmemnt name from database and server
    for i in attachment_list:
        if i == attachment:
            # removing attachment name from list of attachments
            attachment_list.remove(attachment)
            #removing attachment from server
            os.remove(os.path.join(settings.BASE_DIR, "media", attachment))
            break
    
    attachment_string = "---".join(attachment_list)
    if attachment_string != "":
        record.test_attachments = attachment_string
        record.save()
    else:
        record.test_attachments = None
        record.save()
    
    messages.success(request, "Attachment Deleted Successfully")
    redirect_url = reverse('edit-patient-record', args=(patient_id, record_id))
    return redirect(redirect_url)

def render_medical_report(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
        
    mgt = record.management.split("---") if record.management not in ["Awaiting Test Results", "Awaiting Doctors Recommendations"] else ["TBD", "TBD", "TBD", "TBD"]
    
    template_path = 'base/medical_report_pdf.html'
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "patient": patient,
        "patient_age": patient_age,
        "mgt_meds": mgt[0],
        "mgt_surg": mgt[1],
        "mgt_ther": mgt[2],
        "mgt_other": mgt[3],
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
   
    return response

def render_medical_bill(requeust, patient_id, record_id, bill_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    bill = PatientBill.objects.get(id=bill_id)
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
        
    test_list = bill.test_list.split(", ")
    test_list_filtered = [i for i in test_list if i != ""]
    
    test_cost_list = bill.test_cost_list.split(", ")
    test_cost_list_filtered = [j for j in test_cost_list if j != "0"]
    
    test_dict = dict(zip(test_list, test_cost_list))
        
    medication_fees_list = (bill.medication_fees_list).split("---") if bill.medication_fees_list != None else []
    medication_fees_dict = {"meds": medication_fees_list[0], "surg": medication_fees_list[1], "ther": medication_fees_list[2]}
    
    template_path = 'base/medical_bill_pdf.html'
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "record": record,
        "patient": patient,
        "bill": bill,
        "patient_age": patient_age,
        "test_list_filtered": test_list_filtered,
        "test_cost_list_filtered": test_cost_list,
        "test_1": test_list[0],
        "test_2": test_list[1],
        "test_3": test_list[2],
        "test_4": test_list[3],
        "test_5": test_list[4],
        "test_cost_1": test_cost_list[0],
        "test_cost_2": test_cost_list[1],
        "test_cost_3": test_cost_list[2],
        "test_cost_4": test_cost_list[3],
        "test_cost_5": test_cost_list[4],
        "medication_fees_list": medication_fees_list,
        "medication_fees_dict": medication_fees_dict
    }
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="bill.pdf"'
    
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
   
    return response