"""."""
from imager_images.models import Photo, Album
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from imagersite.forms import PhotoForm, AlbumForm
from imager_profile.models import UserProfile
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
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

class PhotoUpdate(UpdateView):
    """."""

    model = Photo
    form_class = PhotoForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """docstring."""

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(UpdateView, self).form_valid(form)


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


class AlbumUpdate(UpdateView):
    """."""

    model = Album
    form_class = AlbumForm
    success_url = reverse_lazy('library')

    def form_valid(self, form):
        """docstring."""

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(UpdateView, self).form_valid(form)


class TagIndexView(ListView):
    """."""

    model = Photo
    template_name = 'imagersite/photos.html'
    context_object_name = 'tags'

    def get_queryset(self):
        tag_object = Photo.objects.filter(tags__slug=self.kwargs.get('slug'))
        tag_object.name = self.kwargs.get('slug')
        return tag_object


class AlbumView(DetailView):
    """."""
    model = Album

    def get_object(self, queryset=None):
        """."""
        if queryset is None:
            queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        obj.tag_list = []
        for photo in obj.photo.all():
            for tag in photo.tags.all():
                if tag not in obj.tag_list:
                    obj.tag_list.append(tag)
        return obj


class PhotoView(DetailView):
    """."""
    model = Album

    def get_object(self, queryset=None):
        """."""
        if queryset is None:
            queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        obj.related_photos = []
        for tag in obj.tags.all():
            for photo in (Photo.objects.filter(tags__slug=tag.slug)):
                if photo not in obj.related_photos and photo != obj:
                    obj.related_photos.append(photo)
        indexnumber = 5 if len(obj.related_photos) > 5 else len(obj.related_photos)
        obj.related_photos = random.sample(obj.related_photos, indexnumber)
        return obj

class PhotosetView(ListView):

    def get_context_data(self, **kwargs):
        """Code gained from docs. https://docs.djangoproject.com/en/1.10/topics/pagination/"""
        context = super(PhotosetView, self).get_context_data(**kwargs)
        request = context['view'].request
        photo_list = Photo.objects.all()
        paginator = Paginator(photo_list, 4) 
        page = request.GET.get('page')
        try:
            context['photos'] = paginator.page(page)
        except PageNotAnInteger:
            context['photos'] = paginator.page(1)
        except EmptyPage:
            context['photos'] = paginator.page(paginator.num_pages)
        return context


class AlbumsetView(ListView):

    def get_context_data(self, **kwargs):
        """Code gained from docs. https://docs.djangoproject.com/en/1.10/topics/pagination/"""
        context = super(AlbumsetView, self).get_context_data(**kwargs)
        request = context['view'].request
        Album_list = Album.objects.all()
        paginator = Paginator(Album_list, 4) 
        page = request.GET.get('page')
        try:
            context['Albums'] = paginator.page(page)
        except PageNotAnInteger:
            context['Albums'] = paginator.page(1)
        except EmptyPage:
            context['Albums'] = paginator.page(paginator.num_pages)
        return context
