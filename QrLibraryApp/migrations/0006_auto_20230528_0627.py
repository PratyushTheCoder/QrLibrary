# Generated by Django 3.2.15 on 2023-05-28 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QrLibraryApp', '0005_alter_qrcode_material_other'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcode',
            name='id',
        ),
        migrations.AlterField(
            model_name='qrcode',
            name='material_special_code',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
