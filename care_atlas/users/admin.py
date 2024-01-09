from django.contrib import admin
from .models import HospitalProfile, RegisteredHospital

# Register your models here.
admin.site.register(HospitalProfile)
admin.site.register(RegisteredHospital)
