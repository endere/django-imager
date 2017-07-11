# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 21:15
from __future__ import unicode_literals

from django.db import migrations, models
import imager_images.models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='profile_pics/default_prof.jpg', upload_to='profile_pics', verbose_name=imager_images.models.Photo),
        ),
    ]
