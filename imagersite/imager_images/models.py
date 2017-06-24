from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
import datetime

ava = [
    ('prv', 'private'),
    ('pub', 'public'),
    ('sha', 'shared')
]
# Create your models here.


class Photo(models.Model):
    """A photo model."""
    user = models.ForeignKey(User)
    date_uploaded = models.ImageField(upload_to='media')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=ava, max_length=7)
    pass


class Album(models.Model):
    """A album model"""
    user = models.ForeignKey(User)
    photo = models.ManyToManyField(Photo)
    cover = models.ImageField(upload_to='AlbumCover', null=True)
    published = models.CharField(choices=ava, max_length=7)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=ava, max_length=7)
    pass
