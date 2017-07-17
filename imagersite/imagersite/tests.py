from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
from django.auth.contrib import User
from imager_images.models import Photo
from faker import Faker
import factory
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    title = factory.Sequence(lambda n: 'photo{}'.format(n))
    image = SimpleUploadedFile(
        name="somephoto.jpg",
        content=open(os.path.join(BASE_DIR, 'MEDIA', 'photos', 'catherrye.png'), 'rb').read(),
        content_type='image/jpeg')


class HomePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='blerg', email='flerg@blerg.klerg')
        self.user.save()

    def add_photos(self):
        photos = [PhotoFactory.build() for _ in range(10)]
        for photo in photos:
            photo.uploaded_by = self.user
            photo.save()

    def test_when_no_image_placeholder_appears(self):
        resp = self.client.get(reverse_lazy('home'))
        # self.assertTrue(b'placehold.it' in resp.content)

        html = BeautifulSoup(resp.content, 'html.parser')
        self.assertTrue(html.find('img', {'src' 'http://placehold.it/200x200'}))

    def test_when_images_exist_one_of_them_is_on_the_page(self):
        self.add_photos()
        resp = self.client.get(reverse_lazy('home'))
        html = BeautifulSoup(resp.content, 'html.parser')
        img_tag = html.find_all('img')
        self.assertTrue(img_tag[0].attrs['src'] == Photo.objects.first().image.url)
