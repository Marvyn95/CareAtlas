from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank = False)
    nationality = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    sex_type = {"Male": "Male", "Female": "Female", "Complicated": "Complicated"}
    sex = models.CharField(blank=False, choices=sex_type, max_length=15)
    phone_number = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        patient = f"{self.first_name} {self.last_name}, {self.nationality}, {self.sex}, DOB: {self.date_of_birth}, TEL: {self.phone_number}"
        return (patient)
    
    
class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    signs_and_symptoms = models.TextField(blank=False)
    tests_for = models.TextField(null=True)
    test_methods = models.TextField(null=True)
    test_results = models.TextField(null=True)
    prescriptions = models.TextField(blank=False)
    
    def __str__(self):
        record = f"signs: {self.signs_and_symptoms}, Tests: {self.tests_for}, Test Results: {self.test_results}, Test Methods: {self.test_methods}, Prescriptions: {self.prescriptions}"
        return record
    
    
class PatientVital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    pulse_bpm = models.IntegerField(null=True)
    temperature = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    systolic_blood_pressure = models.IntegerField(null=True)
    diastolic_blood_pressure = models.IntegerField(null=True)
    
    def __str__(self):
        patient_vital = f"Patient: {self.patient.first_name} {self.patient.last_name} Doc: {self.doctor}, Pulse: {self.pulse_bpm}, Temp: {self.temperature}, Weight: {self.weight}, BP: {self.systolic_blood_pressure} / {self.diastolic_blood_pressure}"
        return (patient_vital)
    
class PatientBill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    medical_record = models.OneToOneField(PatientRecord, on_delete=models.DO_NOTHING, null=True)
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    consultation_fees = models.IntegerField(null=True)
    diagnostic_test_fees = models.IntegerField(null=True)
    nursing_care_fees = models.IntegerField(null=True)
    medication_fees = models.IntegerField(null=True)
    specific_charges = models.TextField(null=True)
    specific_charge_fees = models.IntegerField(null=True)
    total_charges = models.IntegerField(null=True)
    
    def __str__(self):
        patient_bill = f"Consultation: {self.consultation_fees}, Tests: {self.diagnostic_test_fees}, Nursing: {self.nursing_care_fees}, Medication: {self.medication_fees}, Other Charges: {self.specific_charge_fees}, Total: {self.total_charges}"
        return patient_bill
    
    
        
    
    
    
    
    
    
    
    