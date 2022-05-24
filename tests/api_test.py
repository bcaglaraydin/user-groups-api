import unittest
import requests
from flask_api import status


class ApiTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/api"
    USERS_URL = "{}/user".format(API_URL)

    USER_OBJ1 = {
        'name': 'Berdan Çağlar Aydın',
        'email': 'bcaglaraydin@gmail.com',
        'password': 'secret'
    }

    USER_OBJ1_EXPECT = {
        'message': "User created",
        'user': {
            'name': 'Berdan Çağlar Aydın',
            'email': 'bcaglaraydin@gmail.com'
        }
    }

    USER_OBJ2 = {
        'name': 'Boran Aydın',
        'email': 'bcaglaraydin@gmail.com',
        'password': 'boran1234'
    }

    USER_OBJ3 = {
        'name': 'Berdan Çağlar Aydın',
        'email': 'baydin@gmail.com',
        'password': 'secretpass'
    }

    USER_OBJ4 = {
        'name': 'Boran Aydın',
        'email': 'email',
        'password': 'boransecret'
    }

    USER_OBJ5 = {
        'name': 'Boran Aydın',
        'email': 'boranaydin@gmail.com',
        'password': 'b'
    }

    def test0_get_all_users(self):
        r = requests.get(ApiTest.USERS_URL)
        self.assertTrue(status.is_success(r.status_code))

    def test1_create_user_correct(self):
        r = requests.post("{}/{}".format(ApiTest.USERS_URL,
                          'create'), json=ApiTest.USER_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.USER_OBJ1_EXPECT)

    def test2_create_user_email_confict(self):
        r = requests.post("{}/{}".format(ApiTest.USERS_URL,
                          'create'), json=ApiTest.USER_OBJ2)
        print(r.json())
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Email is taken"})

    def test3_create_user_name_confict(self):
        r = requests.post("{}/{}".format(ApiTest.USERS_URL,
                          'create'), json=ApiTest.USER_OBJ3)
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Name already exists"})

    def test4_create_user_email_notvalid(self):
        r = requests.post("{}/{}".format(ApiTest.USERS_URL,
                          'create'), json=ApiTest.USER_OBJ4)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json(), {'error': "Email is not valid"})

    def test5_create_user_pass_notvalid(self):
        r = requests.post("{}/{}".format(ApiTest.USERS_URL,
                          'create'), json=ApiTest.USER_OBJ5)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json(), {'error': "Password is too short"})
