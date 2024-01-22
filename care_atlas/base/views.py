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


date_1 = datetime.datetime.now().strftime("%a %d %b %Y, %I:%M%p").split(" ")
date = {"day": date_1[0],  "day_of_month": date_1[1], "month": date_1[2], "year": date_1[3].replace(",", "")}

# Create your views here.
def home_page(request):
    return render(request, 'base/home_page.html')

def application_patient_page(request, page=1):
    all_patients = Patient.objects.all().order_by('-date_added')
    patients = Paginator(all_patients, 24)
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "patients": patients.page(page)
    }
    return render(request, 'base/application_patient_page.html', context)


def application_home_page(request):
    user = request.user
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    today_records = PatientRecord.objects.filter(doctor__in=doctors).filter(date_added=datetime.datetime.now().date())
    all_records = PatientRecord.objects.filter(doctor__in=doctors)
        
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
            if i.patient.date_of_birth != 'null':
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
                      
        context = {
            "day": date_1[0],
            "day_of_month": date_1[1],
            "month": date_1[2],
            "year": date_1[3].replace(",", ""),
            "date": date,
            "days_patient_num": len(list(today_records)),
            "male_rep": male_rep,
            "female_rep": female_rep,
            "average_age": int(sum(ages)/len(ages)),
            "last_six_months": json.dumps(last_six_months, ensure_ascii=False),
            "client_totals": json.dumps(client_totals)
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
            "client_totals": json.dumps(client_totals)
        }
    return render(request, 'base/application_home_page.html', context)


def new_patient_page(request):
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
        
        
        if date_of_birth == "":
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
        else:
            patient1 = Patient(
                first_name=first_name,
                last_name=last_name,
                sex=sex,
                nationality=nationality,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                address=address,
                next_of_kin=next_of_kin,
                next_of_kin_contact=next_of_kin_contact,
                religion=religion
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
            "vital": vital
        }
        return render(request, 'base/edit_vitals_record.html', context)



def new_patient_record_page(request, patient_id):
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
        test_results = ", ".join(request.POST["test_results"].split("\r\n"))
        conclusions = ", ".join(request.POST["conclusions"].split("\r\n"))
        management = ", ".join(request.POST["management"].split("\r\n"))        
        
        patient=Patient.objects.get(id=patient_id)
            
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
        test_results = ", ".join(request.POST["test_results"].split("\r\n"))
        conclusions = ", ".join(request.POST["conclusions"].split("\r\n"))
        management = ", ".join(request.POST["management"].split("\r\n"))
        
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
        "medical_records": medical_records,
        "patient_age": patient_age
    }
    return render(request, 'base/patient_page.html', context)


def patient_vitals_page(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    vitals = PatientVital.objects.filter(patient=patient).order_by('-date_added')
    
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
        "patient_age": patient_age
    }
    
    return render(request, 'base/vitals_page.html', context)

def medical_record_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    bill = PatientBill.objects.filter(medical_record=record).first()
    
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
        "patient_age": patient_age
    }
    
    return render(request, 'base/medical_record_page.html', context)

def bill_patient_page(request, patient_id, record_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    bill_rec = list(PatientBill.objects.filter(medical_record=record))
    
    if patient.date_of_birth != None:
        patient_age = int((datetime.datetime.now().date() - patient.date_of_birth).days/365)
    else:
        patient_age = 'Unknown'
    
    if len(bill_rec) != 0:
        redirect_url = reverse('medical-record-page', args=(patient_id, record_id))
        return redirect(redirect_url)
    
    
    if request.method == "POST":
        consultation_fees = int(request.POST['consultation_fees'])
        diagnostic_test_fees = int(request.POST['diagnostic_test_fees'])
        nursing_care_fees = int(request.POST['nursing_care_fees'])
        medication_fees = int(request.POST['medication_fees'])
        specific_charges = request.POST['specific_charges']
        specific_charge_fees = int(request.POST['specific_charge_fees'])
        total_charges = consultation_fees+diagnostic_test_fees+nursing_care_fees+medication_fees+specific_charge_fees
        
        patient_bill = PatientBill(
            patient = patient,
            doctor = request.user,
            medical_record = record,
            consultation_fees = consultation_fees,
            diagnostic_test_fees = diagnostic_test_fees,
            nursing_care_fees = nursing_care_fees,
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
            "patient_age": patient_age
        }
        return render(request, 'base/bill_patient_page.html', context)

def patient_bill_page(request, patient_id, record_id, bill_id):
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    bill = PatientBill.objects.get(id=bill_id)
    
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
        "patient_age": patient_age
        
    }
    return render(request, 'base/patient_bill_page.html', context)

def edit_patient_bill_page(request, patient_id, record_id, bill_id):
    bill = PatientBill.objects.get(id=bill_id)
    patient = Patient.objects.get(id=patient_id)
    record = PatientRecord.objects.get(id=record_id)
    
    if request.method == "POST":
        consultation_fees = int(request.POST['consultation_fees'])
        diagnostic_test_fees = int(request.POST['diagnostic_test_fees'])
        nursing_care_fees = int(request.POST['nursing_care_fees'])
        medication_fees = int(request.POST['medication_fees'])
        specific_charges = request.POST['specific_charges']
        specific_charge_fees = int(request.POST['specific_charge_fees'])
        
        bill.consultation_fees = consultation_fees
        bill.diagnostic_test_fees = diagnostic_test_fees
        bill.nursing_care_fees = nursing_care_fees
        bill.medication_fees = medication_fees
        bill.specific_charges = specific_charges
        bill.specific_charge_fees = specific_charge_fees
        bill.total_charges = consultation_fees+diagnostic_test_fees+nursing_care_fees+medication_fees+specific_charge_fees
        
        bill.save()
        
        redirect_url = reverse('patient-bill-page', args=(patient.id, record.id, bill.id))
        return redirect(redirect_url)
    

def bills_page(request, page):
    #getting bills for users hospital
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    all_bills = PatientBill.objects.filter(doctor__in=doctors).order_by("-date_added", "-time_added")
    
    bills = Paginator(all_bills, 10)
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "all_bills": bills.page(page)
    }
    return render(request, 'base/bills_page.html', context)


def records_page(request, page=1):
    doctor_hospitalprofiles  = HospitalProfile.objects.filter(hospital_name=request.user.hospitalprofile.hospital_name)
    doctors = [x.user for x in doctor_hospitalprofiles]
    records_ = PatientRecord.objects.filter(doctor__in=doctors).order_by("-date_added", "-time_added")
    
    records = Paginator(records_, 10)
    
    context = {
        "day": date_1[0],
        "day_of_month": date_1[1],
        "month": date_1[2],
        "year": date_1[3].replace(",", ""),
        "date": date,
        "medical_records": records.page(page)
        }
    return render(request, 'base/records_page.html', context)


def search_page(request, page=1, search_string=""):
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
        "search_text": search_string     
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

    #send notification to Lab Technicians in Facility
    messages.success(request, "Tests Have Been Requested Successfully")
    redirect_url = reverse('patient-page', args=(patient_id, ))
    return redirect(redirect_url)
    