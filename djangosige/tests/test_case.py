# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.db.models.fields.files import FieldFile

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

    def check_user_get_permission(self, url, permission_codename):
        if not isinstance(permission_codename, list):
            permission_codename = [permission_codename]
        self.user.is_superuser = False
        perms = Permission.objects.get(codename__in=permission_codename)
        self.user.user_permissions.remove(perms)
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

        response = self.client.get(url, follow=True)
        message_tags = " ".join(str(m.tags)
                                for m in list(response.context['messages']))
        self.assertIn("permission_warning", message_tags)
        self.user.is_superuser = True
        self.user.save()
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)

    def check_list_view_delete(self, url, deleted_object, context_object_key='object_list'):
        # Testar GET request lista
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(deleted_object in response.context[context_object_key])

        # Deletar objeto criado por POST request
        data = {
            deleted_object.pk: 'on',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(deleted_object in response.context[
                         context_object_key])

    def check_json_response(self, url, post_data, obj_pk, model):
        response = self.client.post(url, post_data, follow=True)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        for c in response_content:
            if c['model'] == model:
                self.assertEqual(c['pk'], obj_pk)


def replace_none_values_in_dictionary(dictionary):
    for key, value in dictionary.items():
        if value is None or isinstance(value, FieldFile):
            dictionary[key] = ''
