# Generated by Django 5.0 on 2023-12-15 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_patientrecord_test_for'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientVital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('time_added', models.TimeField(auto_now_add=True)),
                ('pulse_bpm', models.IntegerField(null=True)),
                ('temperature', models.IntegerField(null=True)),
                ('weight', models.IntegerField(null=True)),
                ('systolic_blood_pressure', models.IntegerField(null=True)),
                ('diastolic_blood_pressure', models.IntegerField(null=True)),
            ],
        ),
    ]
