# Generated by Django 3.2.15 on 2023-05-28 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QrLibraryApp', '0004_qrcode_material_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='material_other',
            field=models.CharField(max_length=200, null=True),
        ),
    ]