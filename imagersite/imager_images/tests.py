class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
    title = factory.Sequence(
        lambda n: 'Photo{}'.format(n))
    )
    description = fake.words(100)
    date_modified = datetime.datetime.now()
    photo = SimpleUploadedFile(
        name='example.jpg'
        content=open(os.path.join(HERE, 'static', 'malcomx.jpg', rb).read(),
        content_type='image/jpeg'
        )
    date_published
    )

class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album
    title = factory.Sequence(
        lambda n: 'Album{}'.format(n))
    )
    description = fake.words(100)
    date_modified = datetime.datetime.now()
    photo = SimpleUploadedFile(
        name='example.jpg'
        content=open(os.path.join(HERE, 'static', 'malcomx.jpg', rb).read(),
        content_type='image/jpeg'
        )
    date_published
    )

class PhotoTestCases(TestCase):
    def setUp(self):
        user = User(
            username='morgan',
            email='morgan@morgan.com'
            )
        user.set_password='morgaaan'
        user.save()
        self.user= user
        #more here...
    def test_upload_image_adds_new_photo_instance(self):
        self.assertEqual(Photo.objects.count(), 0)
        photo = PhotoFactory.build()
        photo.user=self.user()
        photo.save()
        self.assertEqual(Photo.objects.count(), 1)
    def test_new_photo_is_private_by_default(self):
        self.assertEqual(self.photo.published, 'PV')
    def test_delete_user_with_photos_photos_die(self):
        self.user.delete()
        self.assertTrue(Photo.objects.count() == 0)

class AlbumTestCases(TestCase):
    def setUp(self):
        user = User(
            username='morgan',
            email='morgan@morgan.com'
            )
        user.set_password='morgaaan'
        user.save()
        self.user= user
