import unittest
import requests
from flask_api import status


class UserCreateTest(unittest.TestCase):

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
            'id': 1,
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

    USER_OBJ6 = {
        'name': 'Boran Aydın',
        'email': 'boranaydin@gmail.com',
        'password': 'boransecret'
    }

    USER_OBJ6_EXPECT = {
        'message': "User created",
        'user': {
            'id': 2,
            'name': 'Boran Aydın',
            'email': 'boranaydin@gmail.com'
        }
    }

    def test0_get_all_users(self):
        r = requests.get(UserCreateTest.USERS_URL)
        self.assertTrue(status.is_success(r.status_code))

    def test1_create_user_correct(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                          'create'), json=UserCreateTest.USER_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.USER_OBJ1_EXPECT)

    def test2_create_user_email_confict(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                          'create'), json=UserCreateTest.USER_OBJ2)
        print(r.json())
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Email is taken"})

    def test3_create_user_name_confict(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                          'create'), json=UserCreateTest.USER_OBJ3)
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Name already exists"})

    def test4_create_user_email_notvalid(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                          'create'), json=UserCreateTest.USER_OBJ4)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(r.json(), {'error': "Email is not valid"})

    def test6_create_user_correct(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                          'create'), json=UserCreateTest.USER_OBJ6)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.USER_OBJ6_EXPECT)


class UserListTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/api"
    USERS_URL = "{}/user".format(API_URL)

    USER_LIST_OBJ1_EXPECT = {
        "users": [
            {
                "email": "bcaglaraydin@gmail.com",
                "id": 1,
                "name": "Berdan Çağlar Aydın"
            },
            {
                "email": "boranaydin@gmail.com",
                "id": 2,
                "name": "Boran Aydın"
            }
        ]
    }

    USER_GET_OBJ1_EXPECT = {
        'user': {
            'id': 1,
            'name': 'Berdan Çağlar Aydın',
            'email': 'bcaglaraydin@gmail.com'
        }
    }

    def test7_get_all_users(self):
        r = requests.get(UserListTest.USERS_URL)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.USER_LIST_OBJ1_EXPECT)

    def test8_get_user(self):
        id = 1
        r = requests.get("{}/{}".format(UserListTest.USERS_URL, id))
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.USER_GET_OBJ1_EXPECT)

    def test9_get_user_not_found(self):
        id = 9
        r = requests.get("{}/{}".format(UserListTest.USERS_URL, id))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.json(), {'error': "User not found!"})


class UserUpdateTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/api"
    USERS_URL = "{}/user".format(API_URL)

    USER_UPDATE_OBJ1 = {
        "name": "Çağlar Aydın",
        "email": "bcaglaraydin@gmail.com",
        "password": "secret"
    }

    USER_OBJ1_UPDATE_EXPECT = {
        "message": "User updated",
        "user": {
            "email": "bcaglaraydin@gmail.com",
            "id": 1,
            "name": "Çağlar Aydın"
        }
    }

    USER_UPDATE_OBJ2 = {
        "name": "Çağlar Aydın",
        "email": "boranaydin@gmail.com",
        "password": "secret"
    }

    def test10_edit_user(self):
        id = 1
        r = requests.put("{}/{}".format(UserUpdateTest.USERS_URL,
                                        id), json=UserUpdateTest.USER_UPDATE_OBJ1)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.USER_OBJ1_UPDATE_EXPECT)

    def test11_edit_user_email_conflict(self):
        id = 1
        r = requests.patch("{}/{}".format(UserUpdateTest.USERS_URL,
                                          id), json=UserUpdateTest.USER_UPDATE_OBJ2)
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Email is taken"})


class UserAddToGroupTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/api"
    USERS_URL = "{}/user".format(API_URL)

    USER_ADD_GROUP_OBJ1 = {
        "user_id": 1,
        "group_id": 1
    }

    def test12_user_add_to_group(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                                         'add'), json=UserAddToGroupTest.USER_ADD_GROUP_OBJ1)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), {
                         'message': "User " + "Çağlar Aydın" + " added to group " + "Çilekler"})

    def test13_user_add_to_group_conflict(self):
        r = requests.post("{}/{}".format(UserCreateTest.USERS_URL,
                                         'add'), json=UserAddToGroupTest.USER_ADD_GROUP_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "User is already in this group!"})
