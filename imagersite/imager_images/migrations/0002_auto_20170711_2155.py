# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='imager_images.Photo'),
        ),
        migrations.AlterField(
            model_name='album',
            name='photo',
            field=models.ManyToManyField(blank=True, related_name='albums', to='imager_images.Photo'),
        ),
    ]
