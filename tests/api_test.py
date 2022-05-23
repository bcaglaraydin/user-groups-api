import unittest
import requests
from flask_api import status


class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/api"
    USERS_URL = "{}/user".format(API_URL)

    def test_get_all_users(self):
        r = requests.get(ApiTest.USERS_URL)
        self.assertTrue(status.is_success(r.status_code))
