from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HospitalProfile(models.Model):
    hospital_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=20, null=True)
    role = models.CharField(max_length=50, null=True)
    admin_status_choices = {"Regular": "Regular", "Admin": "Admin"}
    admin_status = models.CharField(max_length=20, choices=admin_status_choices, null=True)
    account_status_choices = {"Active": "Active", "Inactive": "Inactive"}
    account_status = models.CharField(max_length=20, choices=account_status_choices, null=True)
    
    def __str__(self):
        profile = f"{self.user.first_name} {self.user.last_name}, {self.hospital_name}"
        return profile
    


class RegisteredHospital(models.Model):
        
    hospital_name = models.CharField(max_length=100, null=False)
    tin_number = models.BigIntegerField(blank=True, null=True)
    country = models.CharField(max_length=25, default='Uganda')
    town_or_state = models.CharField(max_length=25, default='Kampala')
    street_name = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        hospital_details = f"{self.hospital_name}, {self.town_or_state}, {self.country}"
        return hospital_details