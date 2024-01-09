from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HospitalProfile(models.Model):
    hospital_name = models.CharField(max_length=50)
    # telephone_number = models.CharField(max_length=20, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class RegisteredHospital(models.Model):
        
    hospital_name = models.CharField(max_length=100, null=False)
    tin_number = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=25, default='Uganda')
    town_or_state = models.CharField(max_length=25, default='Kampala')
    street_name = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        hospital_details = f"{self.hospital_name}, {self.town_or_state}, {self.country}"
        return hospital_details
    
    
