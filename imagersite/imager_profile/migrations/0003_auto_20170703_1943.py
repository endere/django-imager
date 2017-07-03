# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0002_auto_20170627_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='blood_type',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='citizenship',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='country_of_origin',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='home_address_security_countermeasures',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='life_style',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='next_of_kin',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='social_security_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='social_status',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='camera_type',
            field=models.CharField(default='Beseler', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='photo_style',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='royalty_fees',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='self_description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]