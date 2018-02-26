"""Unit tests for the CityHall API v1 Service endpoint"""
from tinydb import TinyDB
import os
import json
import unittest

import maintenance_api

test_person_data = [
    {
        'id': 1,
        'name': 'John Doe',
        'age': 20
    },
    {
        'id': 2,
        'name': 'Jane Doe',
        'age': 21
    }
]

test_person_insert = '''
    {
        "name": "Jason Sweeney",
        "age": 30
    }
'''

test_task_data = [
    {
        'id': 1,
        'name': 'Lawncare',
    },
    {
        'id': 2,
        'name': 'Bathrom Cleaning',
    }
]

test_task_insert = '''
    {
        "name": "Auditorium Cleaning"
    }
'''


class V1ServiceTest(unittest.TestCase):
    '''Tests for the Person endpoint'''
    def setUp(self):
        '''Set some state for each test in this class'''
        maintenance_api.app.testing = True
        self.app = maintenance_api.app.test_client()
        db = TinyDB('db.json')
        person_table = db.table('person')
        task_table = db.table('task')

        for item in test_person_data:
            person_table.insert(item)
        for item in test_task_data:
            task_table.insert(item)

    def tearDown(self):
        '''clean up the state after each test'''
        os.unlink('db.json')

    def test_people_get(self):
        '''Test the get method on the /v1/person endpoint returns all data'''
        response = self.app.get('/v1/person/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)[0]['id'], 1)

    def test_people_put(self):
        '''Test the put method on the /v1/person endpoint returns all data'''
        response = self.app.post(
            'v1/person/',
            data=test_person_insert,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/v1/person/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)[2]['id'], 3)
        response = self.app.post(
            'v1/person/',
            data=test_person_insert,
            content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_people_put_works_at_zero_index(self):
        '''Test that index doesn't fail if theres nothing in the database'''
        db = TinyDB('db.json')
        db.table('person').purge()
        response = self.app.post(
            'v1/person/',
            data=test_person_insert,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_people_get_detail(self):
        ''' Test the /v1/person/1 endpoint'''
        data = self.app.get('/v1/person/1').data
        self.assertEqual(json.loads(data)[0], test_person_data[0])

    def test_people_delete(self):
        '''Test the v1/person/id delete endpoint'''
        response = self.app.delete('v1/person/1')
        self.assertEqual(response.status_code, 200)

    def test_task_get(self):
        '''Test the get method on the /v1/task endpoint returns all data'''
        response = self.app.get('v1/task/')
        self.assertEqual(response.status_code, 200)

    def test_task_put(self):
        '''Test the put method on the /v1/task endpoint returns all data'''
        response = self.app.post(
            'v1/task/',
            data=test_task_insert,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.app.get('/v1/task/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)[2]['id'], 3)
        response = self.app.post(
            'v1/task/',
            data=test_task_insert,
            content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_task_put_works_at_zero_index(self):
        '''Test that task doesn't fail if theres nothing in the database'''
        db = TinyDB('db.json')
        db.table('task').purge()
        response = self.app.post(
            'v1/task/',
            data=test_task_insert,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_task_get_detail(self):
        data = self.app.get('/v1/task/1').data
        self.assertEqual(json.loads(data)[0], test_task_data[0])

    def test_task_delete(self):
        '''Test the v1/task/id delete endpoint'''
        response = self.app.delete('v1/task/1')
        self.assertEqual(response.status_code, 200)
