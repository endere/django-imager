from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


class ImageActiveProfile(models.Manager):
    def get_queryset(self):
        return super(ImageActiveProfile, self).get_queryset().filter(is_active=True)
BLOOD_TYPES = [
    ("O+", "O+"),
    ("O-", "O-"),
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-")
]

@python_2_unicode_compatible
class UserProfile(models.Model):
    """A user profile."""
    user = models.OneToOneField(User)
    social_status = models.CharField(max_length=100)
    social_security_number = models.CharField(max_length=100)
    blood_type = models.CharField(
        choices=BLOOD_TYPES,
        max_length=3)
    life_style = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)
    home_address = models.CharField(max_length=100)
    home_address_security_countermeasures = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=100)
    objects = models.Manager()
    active = ImageActiveProfile()
    # email_confirmed = models.BooleanField(default=False)

    @property
    def is_active(self):
        return self.user.is_active

    def __repr__(self):
        return """
    username: {}
    social_status: {}
    social_security_number: {}
    blood_type: {}
    life_style: {}
    next_of_kin: {}
    home_address: {}
    home_address_security_countermeasures: {}
    country_of_origin: {}
    citizenship: {}
        """.format(self.user.username, self.social_status, self.social_security_number, self.blood_type, self.life_style, self.next_of_kin, self.home_address, self.home_address_security_countermeasures, self.country_of_origin, self.citizenship)

        

@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = UserProfile(user=kwargs['instance'])
        new_profile.save()
