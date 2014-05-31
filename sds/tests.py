

from django.test import TestCase
from django.core.urlresolvers import reverse
import factory
from sds.models import Music


class MusicFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Music
    uploadedSong = factory.django.FileField(filename='the_file.dat')

class SDSIndexTestCase(TestCase):
    def test_index(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

class SongUploadTestCase(TestCase):
    def test_upload_no_data(self):
        song = MusicFactory.create(email="martin.clyde.weiss@gmail.com")
        self.assertEqual(song.email, "martin.clyde.weiss@gmail.com")

    """def test_upload_song_mp3(self):
        song = MusicFactory.create(email="martin.clyde.weiss@gmail.com")
        self.assertEqual(song.uploadedSong, factory.django.FileField(filename='the_file.dat'))"""


