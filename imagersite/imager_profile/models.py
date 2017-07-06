from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


class ImageActiveProfile(models.Manager):
    def get_queryset(self):
        return super(ImageActiveProfile, self).get_queryset().filter(is_active=True)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """A user profile."""
    user = models.OneToOneField(User, related_name='profile')
    camera_type = models.CharField(max_length=50, default='Beseler')
    self_description = models.CharField(max_length=200, null=True)
    photo_style = models.CharField(max_length=50, null=True)
    royalty_fees = models.CharField(max_length=50, null=True)
    objects = models.Manager()
    active = ImageActiveProfile()
    # email_confirmed = models.BooleanField(default=False)

    @property
    def is_active(self):
        return self.user.is_active

    def __repr__(self):
        return """
    username: {}
    camera_type: {}
    self_description: {}
    photo_style: {}
    royalty_fees: {}
        """.format(self.user.username, self.camera_type, self.self_description, self.photo_style, self.royalty_fees)

        

@receiver(post_save, sender=User)
def make_profile_for_new_user(sender, **kwargs):
    if kwargs['created']:
        new_profile = UserProfile(user=kwargs['instance'])
        new_profile.save()
