# Generated by Django 4.2.11 on 2024-10-25 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_profile_email_address_alter_profile_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_address',
            field=models.CharField(max_length=55, null=True, unique=True),
        ),
    ]
