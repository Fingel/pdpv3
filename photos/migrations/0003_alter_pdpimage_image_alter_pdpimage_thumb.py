# Generated by Django 5.0.3 on 2024-03-11 04:45

import photos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_alter_pdpimage_options_alter_pdpimage_thumb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdpimage',
            name='image',
            field=models.ImageField(upload_to=photos.models.image_upload_salt),
        ),
        migrations.AlterField(
            model_name='pdpimage',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to=photos.models.thumb_upload_salt),
        ),
    ]
