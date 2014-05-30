

from django.test import TestCase
from django.core.urlresolvers import reverse
from selenium import webdriver

"""browser = webdriver.Firefox()
browser.get('http://54.187.196.187/')

body = browser.find_element_by_tag_name('body')
assert 'Global' in body.text

browser.quit()"""


class SDSIndexTestCase(TestCase):
    def test_index(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

