from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import datetime
def home_view(request):
    return render(
        request,
        'imagersite/home.html',
        context={}
    )


def profile_view(request):
    user = request.user
    photo_count_pub = user.uphotos.filter(published='pub').count
    album_count_pub = user.ualbums.filter(published='pub').count
    # curr_date = str(datetime.datetime.now()).split(' ')[0].split('-')
    number_of_published_photos = 0
    for i in user.uphotos.all():
        x = i.date_published
        if (datetime.date.today() - x).days < 7:
            number_of_published_photos += 1
            # print(curr_date)


    return render(
        request,
        'imagersite/profile.html',
        context={'user': request.user, 'photo_num': user.uphotos.count, 'album_num': user.ualbums.count, 'album_num_pub':album_count_pub, 'photo_num_pub': photo_count_pub, 'recent': number_of_published_photos}
    )


def other_profile_view(request, name):
    user = User.objects.get(username=name)
    photo_count = user.uphotos.filter(published='pub').count
    album_count = user.ualbums.filter(published='pub').count
    return render(
        request,
        'imagersite/other_profile.html',
        context={'user': user, 'photo_num': photo_count, 'album_num': album_count}
    )

def account_view(request):
    return render(request, 'registration/registration_form.html')


def library_view(request):
    user = request.user
    photos = user.uphotos.all()
    albums = user.ualbums.all()
    return render(request, 'imagersite/library.html', context={'user': user, 'photos': photos, "albums": albums})

