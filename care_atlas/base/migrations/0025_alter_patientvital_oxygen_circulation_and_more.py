# Generated by Django 5.0 on 2024-01-13 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_rename_test_methods_patientrecord_conclusions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientvital',
            name='oxygen_circulation',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='patientvital',
            name='temperature',
            field=models.FloatField(null=True),
        ),
    ]
