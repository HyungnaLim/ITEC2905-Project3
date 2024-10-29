import unittest
from unittest import TestCase
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

# https://flask.palletsprojects.com/en/stable/testing/

class TestWebApp(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # self.fake_api = FakeAPI()


    # https://flask.palletsprojects.com/en/stable/testing/#sending-requests-with-the-test-client
    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # check that any html is present
        self.assertIn(b'<!DOCTYPE html>', response.data)
        # check "essential" html
        self.assertIn(b'<h1>Discover Artists!</h1>', response.data)
        self.assertIn(b'<form method="GET" action="get_artist">', response.data)
        self.assertIn(b'<form method="POST" action="/bookmark">', response.data)


    def test_get_artist_info(self):
        response = self.app.get('/get_artist')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()