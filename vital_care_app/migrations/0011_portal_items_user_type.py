# Generated by Django 5.0 on 2024-10-10 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vital_care_app', '0010_portal_portal_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal_items',
            name='user_type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
