# Generated by Django 5.0 on 2024-01-09 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_registeredhospitals_registeredhospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredhospital',
            name='country',
            field=models.CharField(default='Uganda', max_length=25),
        ),
        migrations.AlterField(
            model_name='registeredhospital',
            name='hospital_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='registeredhospital',
            name='street',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='registeredhospital',
            name='town_or_state',
            field=models.CharField(default='Kampala', max_length=25),
        ),
    ]
