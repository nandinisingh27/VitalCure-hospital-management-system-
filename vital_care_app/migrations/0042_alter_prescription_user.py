# Generated by Django 5.0 on 2024-10-16 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vital_care_app', '0041_prescription_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vital_care_app.patient'),
        ),
    ]
