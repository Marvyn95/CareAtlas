# Generated by Django 5.0 on 2024-02-03 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Medications',
            new_name='Medication',
        ),
    ]
