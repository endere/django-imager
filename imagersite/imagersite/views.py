"""."""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.core.exceptions import ObjectDoesNotExist
from imager_images.models import Photo, Album
from django.views.generic import DetailView, ListView
import datetime


def home_view(request):
    return render(
        request,
        'imagersite/home.html',
        context={}
    )

class ProfileView(DetailView):

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get().user



def account_view(request):
    return render(request, 'registration/registration_form.html')


def library_view(request):
    user = request.user
    try:
        photos = user.uphotos.all()
        albums = user.ualbums.all()
        return render(request, 'imagersite/library.html', context={'user': user, 'photos': photos, "albums": albums})
    except AttributeError:
        return auth_views.login(request)


def photo_gallery_view(request):
    photos = list(Photo.objects.all())
    for photo in photos:
        if photo.published != 'pub':
            photos.remove(photo)
    return render(
        request,
        'imagersite/photos.html',
        context={'photos': photos})


def album_view(request, album_id):
    albums = list(Album.objects.all())
    for i in albums:
        if i.id == int(album_id):
            album = i
    photos = list(album.photo.all())
    return render(
        request,
        'imagersite/albumview.html',
        context={'album': album, 'photos': photos}
    )


def album_gallery_view(request):
    albums = list(Album.objects.all())
    for album in albums:
        if album.published != 'pub':
            albums.remove(album)
    return render(
        request,
        'imagersite/albums.html',
        context={'albums': albums})
