"""."""
from django import forms
from imager_images.models import Photo, Album


class PhotoForm(forms.ModelForm):
    """."""

    class Meta:
        """."""

        model = Photo
        exclude = ['user']
        widgets = {
            'description': forms.Textarea()
        }


class AlbumForm(forms.ModelForm):
    """."""

    class Meta:
        """."""

        model = Album
        exclude = ['user', 'date_published']
        widgets = {
            'description': forms.Textarea()
        }
