"""imagersite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import DetailView, ListView, TemplateView
from django.conf.urls.static import static
from imager_images.models import Photo, Album
from django.contrib.auth.models import User
from imager_profile.models import UserProfile
from imagersite.views import ProfileView, PhotoCreate, AlbumCreate
from django.contrib.auth import views as auth_views
# from imagersite.imagersite import views as core_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(
        template_name='imagersite/home.html'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', ProfileView.as_view(
        template_name='imagersite/profile.html',
        model=UserProfile,
        context_object_name="user"), name='profile'),
    url(r'^images/photos/$', ListView.as_view(
        template_name='imagersite/photos.html',
        model=Photo,
        paginate_by='10',
        queryset=Photo.objects.all(),
        context_object_name='photos'), name='photo_gallery'),
    url(r'^images/photos/(?P<pk>\d+)/$', DetailView.as_view(
        template_name="imagersite/photoview.html",
        model=Photo,
        context_object_name="photo"), name="photo"),
    url(r'^images/albums/$', ListView.as_view(
        template_name='imagersite/albums.html',
        model=Album,
        paginate_by='10',
        queryset=Album.objects.all(),
        context_object_name='albums'), name='album_gallery'),
    url(r'^images/albums/(?P<pk>\d+)/$', DetailView.as_view(
        template_name="imagersite/albumview.html",
        model=Album,
        context_object_name="album"), name='album'),
    url(r'^accounts/profile/(?P<username>\w+\d+)/$', ProfileView.as_view(
        template_name='imagersite/other_profile.html',
        model=UserProfile,
        context_object_name="user",
        slug_url_kwarg='username',
        slug_field='username'), name='other_profile'),
    url(r'^library/$', ProfileView.as_view(
        template_name='imagersite/library.html',
        model=UserProfile,
        context_object_name="user"), name='library'),
    url(r'^images/photos/add/$', PhotoCreate.as_view(
        template_name='imagersite/createphoto.html',
        model=Photo,
        context_object_name="photos"), name='photo_create'),
    url(r'^images/albums/add/$', AlbumCreate.as_view(
        template_name='imagersite/create.html',
        model=Album,
        context_object_name="albums"), name='album_create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
