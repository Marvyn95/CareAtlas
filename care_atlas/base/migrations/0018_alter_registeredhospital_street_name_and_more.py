# Generated by Django 5.0 on 2024-01-09 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_registeredhospital_street_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredhospital',
            name='street_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='registeredhospital',
            name='tin_number',
            field=models.BigIntegerField(null=True),
        ),
    ]
