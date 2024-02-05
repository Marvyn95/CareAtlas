from django.db import models

# Create your models here.
class Medication(models.Model):
    name = models.CharField(max_length=40, blank=False)
    brand = models.CharField(max_length=40, blank=False)
    formulation_list = {
        "Injectable": "Injectable",
        "Tablets": "Tablets",
        "Capsules": "Capsules",
        "Syrup": "Syrup",
        "Cream": "Cream",
        "Pessary": "Pessary",
        "Drops": "Drops",
        "Lozenge": "Lozenge"
    }
    formulation = models.CharField(blank=False, choices=formulation_list, max_length=20)
    strength_value = models.IntegerField(null=True)
    strength_value_units_choices = {
        "mg": "mg",
        "g": "g",
        "ml": "ml"
    }
    strength_value_units = models.CharField(blank=False, choices=strength_value_units_choices, max_length=10)
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        medication = f"Name: {self.name}, Brand: {self.brand}, Quantity: {self.quantity}, Strength: {self.strength_value} {self.strength_value_units}"
        return medication