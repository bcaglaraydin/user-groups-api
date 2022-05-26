import unittest
import requests
from flask_api import status

API_URL = "http://localhost/api"
GROUPS_URL = "{}/group".format(API_URL)
USERS_URL = "{}/user".format(API_URL)


class GroupCreateTest(unittest.TestCase):

    GROUP_OBJ1 = {
        'name': 'Group1'
    }

    GROUP_OBJ1_EXPECT = {
        'message': "Group created",
        'group': {
            'id': 1,
            'name': 'Group1'
        }
    }

    GROUP_OBJ2 = {
        'name': 'Group1'
    }

    GROUP_OBJ3 = {
        'name': 'Group2'
    }

    GROUP_OBJ3_EXPECT = {
        'message': "Group created",
        'group': {
            'id': 2,
            'name': 'Group2'
        }
    }

    def test1_create_group_correct(self):
        r = requests.post("{}/{}".format(GROUPS_URL,
                          'create'), json=GroupCreateTest.GROUP_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.GROUP_OBJ1_EXPECT)

    def test2_create_group_name_confict(self):
        r = requests.post("{}/{}".format(GROUPS_URL,
                          'create'), json=GroupCreateTest.GROUP_OBJ2)
        print(r.json())
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Name already exists"})

    def test3_create_group_correct(self):
        r = requests.post("{}/{}".format(GROUPS_URL,
                          'create'), json=GroupCreateTest.GROUP_OBJ3)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.GROUP_OBJ3_EXPECT)


class GroupListTest(unittest.TestCase):

    GROUP_LIST_OBJ1_EXPECT = {
        "groups": [
            {
                "id": 1,
                "name": "Group1"
            },
            {
                "id": 2,
                "name": "Group2"
            }
        ]
    }

    GROUP_GET_OBJ1_EXPECT = {
        'group': {
            'id': 1,
            'name': 'Group1'
        }
    }

    def test4_get_all_groups(self):
        r = requests.get(GROUPS_URL)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.GROUP_LIST_OBJ1_EXPECT)

    def test5_get_group(self):
        id = 1
        r = requests.get("{}/{}".format(GROUPS_URL, id))
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.GROUP_GET_OBJ1_EXPECT)

    def test6_get_group_not_found(self):
        id = 9
        r = requests.get("{}/{}".format(GROUPS_URL, id))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.json(), {'error': "Group not found!"})


class GroupUpdateTest(unittest.TestCase):

    GROUP_UPDATE_OBJ1 = {
        "name": "Çilekler"
    }

    GROUP_OBJ1_UPDATE_EXPECT = {
        "message": "Group updated",
        "group": {
            "id": 1,
            "name": "Çilekler"
        }
    }

    GROUP_UPDATE_OBJ2 = {
        "name": "Group2"
    }

    def test10_edit_group(self):
        id = 1
        r = requests.put("{}/{}".format(GROUPS_URL,
                                        id), json=GroupUpdateTest.GROUP_UPDATE_OBJ1)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.GROUP_OBJ1_UPDATE_EXPECT)

    def test11_edit_group_email_conflict(self):
        id = 1
        r = requests.put("{}/{}".format(GROUPS_URL,
                                        id), json=GroupUpdateTest.GROUP_UPDATE_OBJ2)
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Name already exists"})


class GroupGetUsersTest(unittest.TestCase):

    GET_USERS_OBJ1_EXPECT = {
        "group": {
            "id": 1,
            "name": "Çilekler"
        },
        "users": []
    }

    GET_USERS_OBJ2_EXPECT = {
        "group": {
            "id": 1,
            "name": "Çilekler"
        },
        "users": [
            {
                "email": "bcaglaraydin@gmail.com",
                "id": 1,
                "name": "Berdan Çağlar Aydın"
            }
        ]
    }

    USER_ADD_GROUP_OBJ1 = {
        "user_id": 1,
        "group_id": 1
    }

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

    def test12_get_users_from_group_correct(self):
        id = 1
        r = requests.get("{}/{}/{}".format(GROUPS_URL, 'members', id))
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), GroupGetUsersTest.GET_USERS_OBJ1_EXPECT)

    def test13_get_users_from_group_correct(self):

        r = requests.post("{}/{}".format(USERS_URL,
                          'create'), json=GroupGetUsersTest.USER_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.USER_OBJ1_EXPECT)

        r = requests.post("{}/{}".format(USERS_URL,
                                         'add'), json=GroupGetUsersTest.USER_ADD_GROUP_OBJ1)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), {
                         'message': "User " + "Berdan Çağlar Aydın" + " added to group " + "Çilekler"})
        id = 1
        r = requests.get("{}/{}/{}".format(GROUPS_URL, 'members', id))
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), GroupGetUsersTest.GET_USERS_OBJ2_EXPECT)

        r = requests.delete("{}/{}".format(USERS_URL,
                                           id))
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)


class GroupDeleteTest(unittest.TestCase):

    USER_ADD_GROUP_OBJ1 = {
        "user_id": 1,
        "group_id": 1
    }

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

    GROUP_OBJ1 = {
        'name': 'Çilekler'
    }

    GROUP_OBJ1_EXPECT = {
        'message': "Group created",
        'group': {
            'id': 3,
            'name': 'Çilekler'
        }
    }

    def test14_delete_group_correct(self):
        r = requests.post("{}/{}".format(USERS_URL,
                          'create'), json=GroupDeleteTest.USER_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.USER_OBJ1_EXPECT)

        r = requests.post("{}/{}".format(USERS_URL,
                                         'add'), json=GroupDeleteTest.USER_ADD_GROUP_OBJ1)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), {
                         'message': "User " + "Berdan Çağlar Aydın" + " added to group " + "Çilekler"})
        id = 1
        r = requests.delete("{}/{}".format(GROUPS_URL,
                                           id))
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = requests.get("{}/{}".format(GROUPS_URL, id))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.json(), {'error': 'Group not found!'})

        r = requests.delete("{}/{}".format(USERS_URL,
                                           id))
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

        r = requests.post("{}/{}".format(GROUPS_URL,
                          'create'), json=GroupDeleteTest.GROUP_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.GROUP_OBJ1_EXPECT)


test_cases = (GroupCreateTest, GroupListTest,
              GroupUpdateTest, GroupGetUsersTest, GroupDeleteTest)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
