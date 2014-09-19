from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.core.files import File as DjangoFile
import factory, datetime
from sds.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from sds.factories import *
from sds.forms import *
from sds.views import * 

class SDSIndexTestCase(TestCase):
    def test_index(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

"""class organizeTestCase(TestCase):
    def test_upload_no_data(self):
        fp = SimpleUploadedFile('best_file_eva.txt', 'these are the file contents!')
        user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        photo = Photos.objects.create(user=user,photoFile=fp, title="title")
        cityObj = city.objects.create(cityName="bangkok", cityImage=photo)
        e = Events.objects.create(
            title="",
            eventCity=cityObj,
            arrive_start_time=datetime.now(),
            music_start_time=datetime.now(),
            location = "",
            google_map_link = "",
            fbEvent = "",
            )
        response = self.client.post('/organize.html/', {"user":user, "photo":photo, "e":e, "city":cityObj})

        self.assertEqual(resp.status_code, 200)


"""

class SongUploadTestCase(TestCase):
    fixtures = ["sds/fixtures/sds_testdata.json",]   
    def test_upload_song(self):
        with open('sds/test_data/test_song.mp3', 'rb') as song:
            rf = RequestFactory()
            post_request = rf.post('/future.html/?id=10', {'uploadedSong': song, 'email': 'martin.clyde.weiss@gmail.com', 'song_name_or_link':"", 'intention':''})
            response = future(post_request)
            print >>sys.stderr, response
            self.assertTrue(response)


