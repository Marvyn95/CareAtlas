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
    test_for = models.TextField(null=True)
    test_method = models.TextField(null=True)
    results = {"Positive": "Positive", "Negative": "Negative"}
    test_result = models.CharField(choices=results, null=True, max_length=20)
    prescriptions = models.TextField(blank=False)
    
class PatientVital(models.Model):
    date_added = models.DateField(auto_now_add=True)
    time_added = models.TimeField(auto_now_add=True)
    pulse_bpm = models.IntegerField(null=True)
    temperature = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    systolic_blood_pressure = models.IntegerField(null=True)
    diastolic_blood_pressure = models.IntegerField(null=True)
        
    
    
    
    
    
    
    
    