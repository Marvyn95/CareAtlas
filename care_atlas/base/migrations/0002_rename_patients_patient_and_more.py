# Generated by Django 5.0 on 2023-12-14 18:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Patients',
            new_name='Patient',
        ),
        migrations.RenameModel(
            old_name='PatientRecords',
            new_name='PatientRecord',
        ),
    ]
