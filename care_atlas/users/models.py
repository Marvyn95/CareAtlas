from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HospitalProfile(models.Model):
    hospital_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)