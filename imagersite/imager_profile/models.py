from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import uuid


class UserProfile(models.Model):
    """A user profile."""
    user = models.OneToOneField(User)
    social_status = models.CharField(max_length=100)
    social_security_number = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=100)
    life_style = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)
    home_address = models.CharField(max_length=100)
    home_address_security_countermeasures = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=100)

    def __repr__(self):
        return self.user.username


@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = UserProfile(user=kwargs['instance'])
        new_profile.save()
