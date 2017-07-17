# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User

import json

TEST_USERNAME = "test"
TEST_PASSWORD = "testpass"
TEST_EMAIL = "test@test.com"


class BaseTestCase(TestCase):
    fixtures = ["initial_user.json", "test_db_backup.json", ]

    def setUp(self):
        try:
            self.user = User.objects.get(
                username=TEST_USERNAME, email=TEST_EMAIL)
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)

        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def check_list_view_delete(self, url, object):
        # Testar GET request lista
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(object in response.context['object_list'])

        # Deletar objeto criado por POST request
        data = {
            object.pk: 'on',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(object in response.context['object_list'])

    def check_json_response(self, url, post_data, obj_pk, model):
        response = self.client.post(url, post_data, follow=True)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        for c in response_content:
            if c['model'] == model:
                self.assertEqual(c['pk'], obj_pk)
