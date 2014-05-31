

from django.test import TestCase
from django.core.urlresolvers import reverse
import factory
from sds.models import Music
from django_webtest import WebTest

#Test song uploads
class MusicFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Music
    uploadedSong = factory.django.FileField(filename='song.mp3')

class SDSIndexTestCase(TestCase):
    def test_index(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

"""class SongUploadTestCase(TestCase):
    def test_upload_no_data(self):
        song = MusicFactory.create(email="martin.clyde.weiss@gmail.com")
        self.assertEqual(song.email, "martin.clyde.weiss@gmail.com")
"""
    #def test_upload_song_mp3(self):
    #    song = MusicFactory.create(email="martin.clyde.weiss@gmail.com")
    #    self.assertEqual(song.uploadedSong, factory.django.FileField(filename='song.mp3'))


"""class MyTestCase(WebTest):

    # optional: we want some initial data to be able to login
    #fixtures = ['users', 'blog_posts']

    # optional: default extra_environ for this TestCase
    #extra_environ = {'HTTP_ACCEPT_LANGUAGE': 'ru'}

    def testBlog(self):
        # pretend to be logged in as user `kmike` and go to the index page
        index = self.app.get('/', user='kmike')

        # All the webtest API is available. For example, we click
        # on a <a href='/tech-blog/'>Blog</a> link, check that it
        # works (result page doesn't raise exceptions and returns 200 http
        # code) and test if result page have 'My Article' text in
        # it's body.
        assert 'My Article' in index.click('Blog')
exceptions"""
#Test Song downloads


#Test page redirect for future


#Test Email signups
