# Generated by Django 5.1.3 on 2025-07-11 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_shippingdetails_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingdetails',
            name='save_details',
        ),
        migrations.AddField(
            model_name='shippingdetails',
            name='is_default',
            field=models.BooleanField(default=False, help_text='Save as default shipping address'),
        ),
    ]
