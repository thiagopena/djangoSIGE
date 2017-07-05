from django.test import TestCase
from django.core.urlresolvers import resolve
from djangosige.apps.base.views import IndexView


class HomePageOpenTestCase(TestCase):
    def test_home_page_resolves(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__,
                         IndexView.as_view().__name__)
