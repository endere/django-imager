from django.test import TestCase, Client
from django.contrib.auth.models import User
from imager_profile.models import UserProfile
from django.urls import reverse_lazy




import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.Sequence(
        lambda n: "user{}@example.com".format(n)
    )


class ProfileTestCase(TestCase):
    """Tests for the profile model."""

    def setUp(self):
        users = [UserFactory.create() for i in range(20)]

        for user in users:
            user.set_password('foo')
            user.save()

        self.users = users

    def test_every_profile_must_have_a_user(self):
        """The name says it all."""

        with self.assertRaises(Exception):
            patron = UserProfile()
            patron.save()

    def test_profile_with_user_prints_username(self):
        """."""
        some_profile = UserProfile.objects.first()
        self.assertTrue(str(some_profile), some_profile.user.username)

    def test_new_user_has_a_profile(self):
        """."""
        user = UserFactory.create()
        profile = UserProfile.objects.last()
        self.assertTrue(profile.user == user)

    def test_there_are_as_many_users_as_profile(self):
        """."""
        self.assertEquals(len(User.objects.all()), len(UserProfile.objects.all()))


#---------------------------nick tests---------


class ProfilePageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User(username='blerg', email='flerg@blerg.klerg')
        self.user.set_password('potato')
        self.user.save()

    def test_users_profile_info_on_profile_page(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('imager_profile:profile'))
        self.assertTrue(self.user.username.encode('utf8') in resp.content)
        self.assertTrue(b'<p>somestuff</p>' in resp.content)
        self.assertTrue(b'<p>morstuf</p>' in resp.content)
        self.assertTrue(b'<p>otre stuf</p>' in resp.content)
        self.assertTrue(b'<p>dsi stuf</p>' in resp.content)
        self.assertTrue(b'<p>dat stuf</p>' in resp.content)

    def test_users_profile_page_has_link_to_library_page(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse_lazy('imager_profile:profile')) 
        self.assertTrue(bytes(reverse_lazy('imager_images:library').encode('utf8')) in resp.content)


    def test_when_user_logs_in_redicrect_to_profile_page(self):
        resp = self.client.post(reverse_lazy('login'), {
            'username': self.user.username, 'password': 'scrtscrtsRnofun'
        })
        self.assertTrue(resp.url == reverse_lazy('imager_profile:profile'))
        