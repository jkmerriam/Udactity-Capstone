import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all, Movies, Actors, Performance
from config import database_info, auth_tokens
from datetime import date

# Set up Authorization Headers for RBAC testing

casting_Assistant = {
        'Authorization': auth_tokens['casting_Assistant']
}

casting_Director = {
        'Authorization': auth_tokens['casting_Director']
}

executive_Producer = {
        'Authorization': auth_tokens['executive_Producer']
}

# Setup of Unittest

class CastingAgencyTestCase(unittest.TestCase):

    #initialize the database for testing
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting_agency'
        self.database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}/{}".format(database_info["db_user"], database_info["db_password"], database_info["db_location"], database_info["db_name"]))
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

# Tests for /actors GET
    def test_get_all_actors(self):
        res = self.client().get('/actors', headers = casting_Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_actors(self):
        res = self.client().get('/actors/', headers = casting_Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')

# # Tests for /actors POST

    def test_create_new_actor(self):
        json_create_actor = {
            'name' : 'Jamie Keegan',
            'age' : 25,
            'gender': 'Male'
        } 

        res = self.client().post('/actors', json = json_create_actor, headers = casting_Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_401_new_actor(self):
        json_create_actor = {
            'name' : 'Jamie Keegan',
            'age' : 25,
            'gender': 'Male'
        } 

        res = self.client().post('/actors', json = json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_422_create_new_actor(self):
        json_create_incomplete_actor = {
            'age' : 25,
            'gender': 'Male'
        } 

        res = self.client().post('/actors', json = json_create_incomplete_actor, headers = casting_Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# Tests for /actors PATCH

    def test_edit_actor(self):
        json_update_actor_age = {
            'age' : 30
        }
        res = self.client().patch('/actors/1', json = json_update_actor_age, headers = casting_Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_422_edit_actor(self):
            res = self.client().patch('/actors/1', headers = casting_Director)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'] , 'unprocessable')

    def test_error_404_edit_actor(self):
        json_update_actor_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/1212', json = json_update_actor_age, headers = casting_Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')

# # Tests for /actors DELETE

    def test_error_401_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):
        res = self.client().delete('/actors/1', headers = casting_Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers = casting_Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_404_delete_actor(self):
        res = self.client().delete('/actors/12', headers = casting_Director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')

# # Tests for /movies GET

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers = casting_Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_401_get_all_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_movies(self):
        res = self.client().get('/movies/', headers = casting_Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')

# # Tests for /movies POST

    def test_create_new_movie(self):
        json_create_movie = {
            'title' : 'Udacity FSND',
            'release_date' : date.today()
        }

        res = self.client().post('/movies', json = json_create_movie, headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_422_create_new_movie(self):
        json_create_incomplete_movie = {
            'release_date' : date.today()
        }

        res = self.client().post('/movies', json = json_create_incomplete_movie, headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

# # Tests for /movies PATCH

    def test_edit_movie(self):
        json_edit_movie = {
            'title' : 'Full Stack Nano Degree'
        }
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_400_edit_movie(self):
        res = self.client().patch('/movies/1', headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'unprocessable')

    def test_error_404_edit_movie(self):
        json_edit_movie = {
            'title' : 'Full Stack Nano Degree'
        }
        res = self.client().patch('/movies/1212', json = json_edit_movie, headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')

# # Tests for /movies DELETE
    def test_error_401_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_movie(self):
        res = self.client().delete('/movies/1', headers = casting_Assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_error_404_delete_movie(self):
        res = self.client().delete('/movies/12', headers = executive_Producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'resource not found')

# To run tests run 'python test_agency.py'
if __name__ == "__main__":
    unittest.main()
