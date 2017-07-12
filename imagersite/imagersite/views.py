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
from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse_lazy
import datetime


class ProfileView(DetailView):

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get().user


class PhotoCreate(CreateView):

    model = Photo
    fields = ['title', 'image', 'description', "published"]
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """docstring"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)


class AlbumCreate(CreateView):

    model = Album
    fields = ['title', 'cover', 'description', "published"]
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """docstring"""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)

        