# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User


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
