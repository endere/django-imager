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


def profile_view(request):
    user = request.user
    try:
        photo_count_pub = user.uphotos.filter(published='pub').count
        album_count_pub = user.ualbums.filter(published='pub').count
        # curr_date = str(datetime.datetime.now()).split(' ')[0].split('-')
        number_of_published_photos = 0
        for i in user.uphotos.all():
            x = i.date_published
            if (datetime.date.today() - x).days < 7:
                number_of_published_photos += 1
    except AttributeError:
        return auth_views.login(request)
    return render(
        request,
        'imagersite/profile.html',
        context={'user': request.user, 'photo_num': user.uphotos.count,
                 'album_num': user.ualbums.count,
                 'album_num_pub': album_count_pub,
                 'photo_num_pub': photo_count_pub,
                 'recent': number_of_published_photos,
                 'profile_pic': user.profile.profile_pic})


def other_profile_view(request, name):
    try:
        user = User.objects.get(username=name)
        photo_count = user.uphotos.filter(published='pub').count
        album_count = user.ualbums.filter(published='pub').count
        return render(
            request,
            'imagersite/other_profile.html',
            context={'user': user, 'photo_num': photo_count, 'album_num': album_count}
        )
    except ObjectDoesNotExist:
        return redirect(home_view)


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


# class photo_view(DetailView):
#     def get(request, photo_id):
#         print(photo_id)
#         photos = list(Photo.objects.all())
#         photo = ''
#         for i in photos:
#             if i.id == int(photo_id):
#                 photo = i
#         return render(
#             request,
#             'imagersite/photoview.html',
#             context={'photo': photo}
#         )

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
