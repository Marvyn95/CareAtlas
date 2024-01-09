# Generated by Django 5.0 on 2024-01-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_remove_patient_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredHospitals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.TextField()),
                ('tin_number', models.BigIntegerField(null=True)),
                ('country', models.TextField(default='Uganda')),
                ('town_or_state', models.TextField(default='Kampala')),
                ('street', models.TextField(null=True)),
            ],
        ),
    ]
