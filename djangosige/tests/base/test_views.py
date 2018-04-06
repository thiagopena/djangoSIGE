# -*- coding: utf-8 -*-

from djangosige.tests.test_case import BaseTestCase
from django.urls import resolve, reverse
from djangosige.apps.base.views import IndexView


class BaseViewsTestCase(BaseTestCase):

    def test_home_page_resolves(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__,
                         IndexView.as_view().__name__)

    def test_home_page_get_request(self):
        url = reverse('base:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        response = self.client.get("/404/")
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.status_code, 404)

    def test_500_page(self):
        response = self.client.get("/500/")
        self.assertTemplateUsed(response, '500.html')
        self.assertEqual(response.status_code, 500)
