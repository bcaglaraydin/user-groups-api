import unittest
import requests
from flask_api import status


class GroupApiTest(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/api"
    GROUPS_URL = "{}/group".format(API_URL)

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

    def test1_create_group_correct(self):
        r = requests.post("{}/{}".format(GroupApiTest.GROUPS_URL,
                          'create'), json=GroupApiTest.GROUP_OBJ1)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.GROUP_OBJ1_EXPECT)

    def test2_create_group_name_confict(self):
        r = requests.post("{}/{}".format(GroupApiTest.GROUPS_URL,
                          'create'), json=GroupApiTest.GROUP_OBJ2)
        print(r.json())
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Name already exists"})

    def test3_create_group_correct(self):
        r = requests.post("{}/{}".format(GroupApiTest.GROUPS_URL,
                          'create'), json=GroupApiTest.GROUP_OBJ3)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.json(), self.GROUP_OBJ3_EXPECT)

    def test4_get_all_groups(self):
        r = requests.get(GroupApiTest.GROUPS_URL)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.GROUP_LIST_OBJ1_EXPECT)

    def test5_get_group(self):
        id = 1
        r = requests.get("{}/{}".format(GroupApiTest.GROUPS_URL, id))
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.GROUP_GET_OBJ1_EXPECT)

    def test6_get_group_not_found(self):
        id = 9
        r = requests.get("{}/{}".format(GroupApiTest.GROUPS_URL, id))
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(r.json(), {'error': "Group not found!"})

    def test10_edit_group(self):
        id = 1
        r = requests.put("{}/{}".format(GroupApiTest.GROUPS_URL,
                                        id), json=GroupApiTest.GROUP_UPDATE_OBJ1)
        self.assertTrue(status.is_success(r.status_code))
        self.assertEqual(r.json(), self.GROUP_OBJ1_UPDATE_EXPECT)

    def test11_edit_group_email_conflict(self):
        id = 1
        r = requests.patch("{}/{}".format(GroupApiTest.GROUPS_URL,
                                          id), json=GroupApiTest.GROUP_UPDATE_OBJ2)
        self.assertEqual(r.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(r.json(), {'error': "Name already exists"})
