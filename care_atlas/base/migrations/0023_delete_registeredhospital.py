# Generated by Django 5.0 on 2024-01-09 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_alter_registeredhospital_street_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RegisteredHospital',
        ),
    ]
