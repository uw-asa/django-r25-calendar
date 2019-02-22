import unittest

from django.contrib.auth.models import User
from django.test import Client


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception:
        user = User.objects.create_user(username, password='pass')
        return user


def get_user_pass(username):
    return 'pass'


class R25CALTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def set_user(self, username):
        get_user(username)
        self.client.login(username=username,
                          password=get_user_pass(username))

    def test_space_reservations(self):
        self.set_user('javerage')

        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
