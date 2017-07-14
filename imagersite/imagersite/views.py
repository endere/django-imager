"""."""
from imager_images.models import Photo, Album
from django.views.generic import DetailView, CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from imagersite.forms import PhotoForm, AlbumForm
from imager_profile.models import UserProfile
from random import randint
import datetime


class HomeView(DetailView):
    """."""
    model = Photo

    def get_object(self, queryset=None):
        """."""
        # import pdb; pdb.set_trace()
        if queryset is None:
            queryset = Photo.objects.all()
            y = queryset.count()
            if y == 0:
                queryset = None
            else:
                # x = randint(1, y)
                queryset = queryset.order_by('?').first()
        return queryset


class ProfileView(DetailView):
    """."""
    model = UserProfile

    def get_object(self, queryset=None):
        """."""
        if queryset is None:
            queryset = self.get_queryset()
        # import pdb; pdb.set_trace()
        return queryset.get(user=self.request.user)

class OtherProfileView(DetailView):
    """."""
    model = UserProfile

    def get_object(self, queryset=None):
        """."""
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(user__username=self.kwargs['username'])



class PhotoCreate(CreateView):
    """."""

    model = Photo
    form_class = PhotoForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """docstring."""

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)


class AlbumCreate(CreateView):
    """."""

    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """docstring."""

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)

