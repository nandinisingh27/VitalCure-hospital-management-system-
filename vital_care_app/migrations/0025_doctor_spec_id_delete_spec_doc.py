# Generated by Django 5.0 on 2024-10-11 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vital_care_app', '0024_specialist_spec_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='spec_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vital_care_app.specialist'),
        ),
        migrations.DeleteModel(
            name='Spec_doc',
        ),
    ]
