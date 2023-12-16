from django.contrib import admin
from .models import Patient, PatientRecord, PatientVital

# Register your models here.
admin.site.register(Patient)
admin.site.register(PatientRecord)
admin.site.register(PatientVital)
