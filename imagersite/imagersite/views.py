"""."""
from imager_images.models import Photo, Album
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from imagersite.forms import PhotoForm, AlbumForm
import datetime


class ProfileView(DetailView):
    """."""

    def get_object(self, queryset=None):
        """."""
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get().user


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

    def get_form(self, form):
        """docstring."""
        form = super(AlbumCreate, self).get_form()
        uphotos = Photo.objects.filter(user=self.request.user)
        form.fields['photos'].queryset = uphotos
        form.fields['cover'].queryset = uphotos
        return form

    def form_valid(self, form):
        """docstring."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(CreateView, self).form_valid(form)
