# Generated by Django 5.0 on 2024-01-10 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_registeredhospital_hospital_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalprofile',
            name='role',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='hospitalprofile',
            name='telephone_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]