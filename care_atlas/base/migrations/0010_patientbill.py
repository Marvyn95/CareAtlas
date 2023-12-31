# Generated by Django 5.0 on 2023-12-26 08:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_rename_test_for_patientrecord_test_methods_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('time_added', models.TimeField(auto_now_add=True)),
                ('consultation_fees', models.IntegerField(null=True)),
                ('diagnostic_test_fees', models.IntegerField(null=True)),
                ('nursing_care_fees', models.IntegerField(null=True)),
                ('medication_fees', models.IntegerField(null=True)),
                ('specific_charges', models.TextField(null=True)),
                ('specific_charge_fees', models.IntegerField(null=True)),
                ('total_charges', models.IntegerField(null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.patient')),
            ],
        ),
    ]
