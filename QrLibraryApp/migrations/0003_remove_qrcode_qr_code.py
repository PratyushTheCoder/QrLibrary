# Generated by Django 3.2.15 on 2023-05-28 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QrLibraryApp', '0002_auto_20230528_0530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcode',
            name='qr_code',
        ),
    ]