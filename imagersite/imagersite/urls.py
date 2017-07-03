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
from django.conf.urls.static import static
from imagersite.views import home_view, profile_view, other_profile_view, library_view, photo_view, photo_gallery_view, album_view, album_gallery_view
from django.contrib.auth import views as auth_views
# from imagersite.imagersite import views as core_views
urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', profile_view, name='profile'),
    url(r'^images/photos/$', photo_gallery_view, name='photo_gallery'),
    url(r'^images/photos/(?P<photo_id>\w+)/$', photo_view, name='photo'),
    url(r'^images/albums/$', album_gallery_view, name='album_gallery'),
    url(r'^images/albums/(?P<album_id>\w+)/$', album_view, name='album'),
    url(r'^accounts/profile/(?P<name>\w+)/$', other_profile_view, name='other_profile'),
    url(r'^library/$', library_view, name='library'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
