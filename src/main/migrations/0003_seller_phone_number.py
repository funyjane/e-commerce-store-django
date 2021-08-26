# Generated by Django 3.2.5 on 2021-08-26 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_smslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='phone_number',
            field=models.CharField(blank=True, default='', error_messages={'invalid': 'Phone number must be valid'}, max_length=12, null=True, unique=True, verbose_name='Phone'),
        ),
    ]
