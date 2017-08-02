"""Test for Django-Imager"""
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, reverse_lazy
import factory
from imager_profile.models import UserProfile
from imager_images.models import Photo
from imager_images.models import Album
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from imagersite.settings import MEDIA_ROOT


class UserFactory(factory.django.DjangoModelFactory):
    """Making users for tests."""
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class PhotoFactory(factory.django.DjangoModelFactory):
    """Create photos for testing."""
    class Meta:
        model = Photo
    title = factory.Sequence(lambda n: "photo{}".format(n))
    image = SimpleUploadedFile(
        name="testing.png",
        content=open(MEDIA_ROOT + '/test/testing.png', 'rb').read(),
        content_type="image/png"
    )


class AlbumFactory(factory.django.DjangoModelFactory):
    """Create albums for testing."""
    class Meta:
        model = Album
    title = factory.Sequence(lambda n: "album{}".format(n))


class ProfileTestCase(TestCase):
    """Test suite for creating new users."""
    def setUp(self):
        """Set up users for testing."""
        users = [UserFactory.create() for _ in range(20)]
        self.users = users

    def test_number_of_users_equals_number_of_profiles(self):
        """
        Test that the same amount of users
        and profiles have been created in db.
        """
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        self.assertTrue(user_count == profile_count)

    def test_every_profile_must_have_a_user(self):
        """Test that every profile has a user."""
        with self.assertRaises(Exception):
            imager = UserProfile()
            imager.save()

    def test_profile_with_user_prints_username(self):
        """Test that profile with user prints username."""
        profile = UserProfile.objects.first()
        self.assertTrue(str(profile), profile.user.username)

    def test_new_user_has_a_profile(self):
        """Test new user has a profile."""
        user = UserFactory.create()
        profile = UserProfile.objects.last()
        self.assertTrue(profile.user == user)

    def test_profile_with_user_photog_level_beginner(self):
        """Test that photography level could be begginer."""
        profile = UserProfile.objects.last()
        profile.photog_level = "Beginner"
        profile.save()
        self.assertEqual(profile.photog_level, 'Beginner')

    def test_profile_with_user_photog_level_hobbyist(self):
        """Test that photography level could be hobbyist."""
        profile = UserProfile.objects.last()
        profile.photog_level = "Hobbyist"
        profile.save()
        self.assertEqual(profile.photog_level, 'Hobbyist')

    def test_profile_with_user_photog_level_professional(self):
        """Test that photography level could be professional."""
        profile = UserProfile.objects.last()
        profile.photog_level = "Professional"
        profile.save()
        self.assertEqual(profile.photog_level, 'Professional')

    def test_profiles_equals_users(self):
        """Every created user has a profile."""
        self.assertTrue(UserProfile.objects.count() == User.objects.count())

    def test_is_active_method(self):
        """Test newly created users are active."""
        self.assertTrue(UserProfile.objects.first().is_active is True)


class ProfileViewTests(TestCase):
    """A class to run tests on the profile view."""

    def setUp(self):
        """Set up for profile view tests."""
        self.client = Client()
        self.req_factory = RequestFactory()

    def test_if_user_isnt_authenticated_shows_login(self):
        """Test that login is available when user isn't authenticated."""
        response = self.client.get(reverse('home'))
        self.assertTrue(b'login' in response.content.lower())

    def test_if_user_is_authenticated_shows_logout(self):
        """Test that logout is available when user is logged in."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        response = self.client.get(reverse('home'))
        self.assertFalse(b'login' in response.content.lower())
        self.assertTrue(b'logout' in response.content.lower())

    def test_if_user_is_authenticated_and_logout_no_longer_authenticated(self):
        """Test that logout properly logs out the user."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        response = self.client.get(reverse('logout'), follow=True)
        self.assertTrue(b'login' in response.content.lower())


class ProfileTests(TestCase):
    """Profile tests."""

    def setUp(self):
        """Set up for testing."""
        user = UserFactory.create()
        user.set_password('caaarlos')
        user.save()
        self.user = user
        photos = [PhotoFactory.create(profile=user.profile) for i in range(20)]
        album = AlbumFactory.build()
        album.profile = user.profile
        album.save()
        for photo in photos:
            album.photos.add(photo)
        album.cover_photo = photos[0]
        self.photos = photos
        self.album = album
        self.client = Client()

    def tearDown(self):
        """Teardown when tests complete."""
        to_delete = os.path.join(MEDIA_ROOT, 'photos', 'testing*.png')
        os.system('rm -rf ' + to_delete)

    def test_profile_route_not_logged_in_redirects_home(self):
        """Test that the profile route directs home when not logged in."""
        response = self.client.get(reverse('user_profile'), follow=True)
        self.assertTrue(b'Django Imager' in response.content)

    def test_upload_image_add_new_photo_instance(self):
        """Test uploading images adds new photo instance."""
        self.assertEqual(Photo.objects.count(), 20)

    def test_new_photo_is_public_by_default(self):
        """Test that default privacy for photos is Private."""
        self.assertEqual(self.photos[0].published, "PU")

    def test_delete_user_with_photos_photos_die(self):
        """Test that deletion of user also deletes that user's photos."""
        self.user.delete()
        self.assertTrue(Photo.objects.count() == 0)

    def test_uploaded_photo_lives_in_media_user_photos(self):
        """Test that uploaded photo is saved in media folder"""
        upload_dir = os.path.join(MEDIA_ROOT, 'photos')
        directory_contents = os.listdir(upload_dir)
        name = self.photos[1].image.name.split('/')[1]
        self.assertTrue(name in directory_contents)

    def test_delete_user_with_albums_albums_die(self):
        """Test that the deletion of a user also deletes their albums."""
        self.assertTrue(Album.objects.count() == 1)
        self.user.delete()
        self.assertTrue(Album.objects.count() == 0)

    def test_delete_user_also_deletes_profile(self):
        """Test that deletion of user also deletes that user's profile."""
        self.user.delete()
        self.assertTrue(UserProfile.objects.count() == 0)

    def test_profile_view_photo_count(self):
        """Test that the profile view lists correct number of photos."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        response = self.client.get(
            reverse_lazy('user_profile')
        )
        self.assertTrue(b'<p>Public: 0<p>' in response.content)

    def test_profile_view_has_link_to_library(self):
        """Test that the link to the library is in the photo view."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        response = self.client.get(
            reverse_lazy('user_profile')
        )
        self.assertTrue(b'href="/images/library/1/1"' in response.content)

    def test_profile_link_to_library_directs_to_library_view(self):
        """Test profile page library links redirects to library."""
        response = self.client.get(
            reverse_lazy(
                'library',
                kwargs={'album_page_num': 1, 'photo_page_num': 1}
            )
        )
        self.assertTrue(
            b'All Publicly Available Albums' in response.content and b'All Publicly Available Photos' in response.content
        )

    def test_logged_in_user_redirects_to_profile(self):
        """Test when user logs in is directed to profile."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        response = self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        self.assertTrue(response.status_code == 302)

    def test_logged_in_profile_url_is_correct(self):
        """Test logged in user profile url is /profile/."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        response = self.client.post(
            reverse('login'),
            {'username': 'bob', 'password': 'bobberton'}
        )
        self.assertTrue(response.url == '/profile')

    def test_other_user_profile_url_is_correct(self):
        """Test other profile url is correct."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        response = self.client.get(
            reverse_lazy('profile', kwargs={'username': 'bob'})
        )
        self.assertTrue(response.request['PATH_INFO'] == '/profile/bob/')

    def test_private_info_not_shown_in_profile(self):
        """Test private info is not shown in profile."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        response = self.client.get(
            reverse_lazy('profile', kwargs={'username': 'bob'})
        )
        self.assertTrue(b'Private:' not in response.content)

    def test_public_info_is_displayed(self):
        """Test public info is displayed."""
        test_bob = User(username='bob')
        test_bob.set_password('bobberton')
        test_bob.save()
        response = self.client.get(
            reverse_lazy('profile', kwargs={'username': 'bob'})
        )
        self.assertTrue(b'Public:' in response.content)
