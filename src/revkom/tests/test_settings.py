
from django.core.urlresolvers import resolve
from django.test import TestCase


class FrontPageTest(TestCase):
    def test_root_url_resolves_to_front_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.func_name, 'FrontPageView')
