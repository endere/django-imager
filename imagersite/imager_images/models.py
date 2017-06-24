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
    image = models.ImageField(upload_to='photos', null=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(auto_now_add=True)
    published = models.CharField(choices=ava, max_length=7)

    def __repr__(self):
        return """
    user: {}
    image: {}
    title: {}
    description: {}
    date_uploaded: {}
    date_modified: {}
    date_published: {}
    published: {}
        """.format(self.user, self.image, self.title, self.description, self.date_uploaded, self.date_modified, self.date_published, self.published)



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

    def __repr__(self):
        return """
    user: {}
    photo: {}
    cover: {}
    title: {}
    description: {}
    date_created: {}
    date_modified: {}
    date_published: {}
    published: {}
        """.format(self.user, self.photo, self.cover, self.title, self.description, self.date_created, self.date_modified, self.date_published, self.published)


# @receiver(post_save, sender=User)
# def make_album_for_new_user(sender, **kwargs):
#     if kwargs['created']


# @receiver(post_save, sender=User)
# def make_profile_for_new_user(sender, **kwargs):
#     if kwargs['created']:
#         new_profile = UserProfile(user=kwargs['instance'])
#         new_profile.save()
