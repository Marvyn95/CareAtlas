from django import forms
from base.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "sex", "nationality", "date_of_birth", "phone_number"]
        labels = {}