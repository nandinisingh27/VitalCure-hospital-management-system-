# Generated by Django 5.0 on 2024-10-11 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vital_care_app', '0014_doctor_consultation_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.CharField(max_length=10),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=80)),
                ('patientID', models.CharField(max_length=5)),
                ('phone_number', models.CharField(max_length=10)),
                ('height', models.CharField(max_length=4)),
                ('weight', models.CharField(max_length=4)),
                ('age', models.CharField(max_length=3)),
                ('preferred_date', models.CharField(max_length=10)),
                ('symptoms', models.CharField(max_length=255, null=True)),
                ('blood_group', models.CharField(max_length=3)),
                ('doctor_selected', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vital_care_app.patient')),
            ],
        ),
    ]
