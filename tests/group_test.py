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
            'name': 'Group2'
        }
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
