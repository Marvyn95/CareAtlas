# Generated by Django 5.0 on 2024-01-09 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_registeredhospital_street_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredhospital',
            name='tin_number',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]