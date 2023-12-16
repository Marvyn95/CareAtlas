from django import forms
from base.models import Patient, PatientRecord, PatientVital


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "sex", "nationality", "date_of_birth", "phone_number"]
        labels = {}
        
class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = ["signs_and_symptoms", "test_for", "test_method", "test_result", "prescriptions"]
        labels = {}
        
class PatientVitalForm(forms.ModelForm):
    class Meta:
        model = PatientVital
        fields = ["weight", "temperature", "pulse_bpm", "systolic_blood_pressure", "systolic_blood_pressure"]
        labels = {}