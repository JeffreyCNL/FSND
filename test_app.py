import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import sys

from app import create_app
from models import setup_db, Actor, Movie, drop_and_create_all
from datetime import date
from config import TOKENS
# CASTING_ASSISTANT_AUTH_HEADER = {
#     'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNidUcxblJ4VzhDVFNPYkMyanJHZiJ9.eyJpc3MiOiJodHRwczovL2plZmZyZXlmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjIyY2VjZjU4ZTI4NjAwMzcyZjU3ZjYiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU5NjExNjgxNSwiZXhwIjoxNTk2MjAzMjE0LCJhenAiOiJ1UXZNNDVPNkZmNGpxWm1GbzhiZ1hCckRKUG5KUDVkayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.dWuG5mhBpOMNUFXDfx2BwHANEuBsT0RpeOBELfsTlfWPLjPUiiqkadvcl34RNowTnkwxkQT4jqn4B0Cl-wM8tW9ZU2D1NMrsY74j10551FhAtz3BCbYOgZuswEn3KzN-VNhoDRua6xUyUNoSZXJQ92fOMNKa0afCKeSxj4VO6G2D3jQYSMEt28RCXFYjAPiNAO4D63RLqdfqY5a7tfSfq5OlaUZdYFV8vUBV3FxsiSBOO9F2D5wA2wE7_6NmPNS_qcWIsgA1gt4J3_4DwUwyLQUG0frYhPz4gaSGsTYJuWfXg1fyVXJMQvQnTYsdwn3AhjVb7VNxqUut1PtsetwssA"
# }
# CASTING_DIRECTOR_AUTH_HEADER = {
#     'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNidUcxblJ4VzhDVFNPYkMyanJHZiJ9.eyJpc3MiOiJodHRwczovL2plZmZyZXlmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWUwOTIwNWYyYTc4MzAwMTk2MTEyZTEiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU5NjExNjU1NCwiZXhwIjoxNTk2MjAyOTUzLCJhenAiOiJ1UXZNNDVPNkZmNGpxWm1GbzhiZ1hCckRKUG5KUDVkayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.s5unjMh1FER-73M3rQX0HE-ERkZuTSMfPfOKMnEreHqAGN2kd1miVwXLn2ezlCconYWbpdAmLRHn-J4STkLGer_DWDN9hImpYQ-NUZu-dGr8leHo7IVgK5vOhqUZQZ6bGPq1WEcwUS5m2OvIOQb50b6oyajfMAcmq-LfoB0P6z8zRY15lCBiacAZXidS2Kh40b0VkXMjDwcya7OugLEdtLVtfAda7JKle4_zAvjGFVLLS0qtRO5MRefUVXWUHzGVUbBE_-MCAjKJSur8I-06Zu6n4TI85ulViCpfS65mb-mTlcn7kM-XKxg8Tf7jS5Zfx5efkSRxDv2q_LKiaMc6Kg"
# }
# EXECUTIVE_PRODUCER_AUTH_HEADER = {
#     'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNidUcxblJ4VzhDVFNPYkMyanJHZiJ9.eyJpc3MiOiJodHRwczovL2plZmZyZXlmc25kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWRiNDJkZTIyOWRjZTAwMTNkNTYzMTYiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU5NjExNjI1NCwiZXhwIjoxNTk2MjAyNjUzLCJhenAiOiJ1UXZNNDVPNkZmNGpxWm1GbzhiZ1hCckRKUG5KUDVkayIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.j9S9QCzIRAxYfPJycXJarYTwnhWCib9apJT5PS8aFotFUmZ8VSS5kh-_zMCwUf86jhpP5_Jg1b6IdkQyYAB9lp8IIBBW-HiHQfNMgR3WF6qE2wHHhvk-lUqY-Squjf_e9vOV1J90XuNwUOFTAjackTpi-CGiJVpeGtSoDpo5gn9QZOsBhHxO3e8QRRGPYIRJ-5mVXIm8yjlihe9CWv1VaEtddmxycIizWSI9lfgU8mTdwXzkeab6_gUhCbFS8j0nu8xUR0OcoHGR_WX2wjPaoeMgL3uhTo5cRhlWCey8PsV-FakDDs9ZPgxfEFv2nKngQNnvKYOvUWHpbib1Lr1EGw"
# }
CASTING_ASSISTANT_AUTH_HEADER = {
    'Authorization': TOKENS['CASTING_ASSISTANT']
}
CASTING_DIRECTOR_AUTH_HEADER = {
    'Authorization': TOKENS['CASTING_DIRECTOR']
}
EXECUTIVE_PRODUCER_AUTH_HEADER = {
    'Authorization': TOKENS['EXECUTIVE_PRODUCER']
}


class CastAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "cast_agency_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = 'postgresql:///cast_agency_test'
        setup_db(self.app, self.database_path)
        drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    # Actors
    '''
    Get actors
    '''
    def test_get_actors(self):
        '''
        normal operation of getting actors
        '''
        res = self.client().get('/actors', headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_get_actors_not_found(self):
        '''
        no actors in the page
        '''
        res = self.client().get('/actors?page=12000000', headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_get_actors_no_authorization(self):
        '''
        no permission provided at all
        '''
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    '''
    create actors
    '''
    def test_create_actor(self):
        '''
        normal operation for posting actor
        '''
        new_actor = {
            'name': 'Jeffrey',
            'age': 20,
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=new_actor, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_actors'])

    def test_create_in_valid_actor(self):
        '''
        no null value in the actor
        '''
        new_actor = {
            'name': '',
            'age': 20,
            'gender': ''
        }
        res = self.client().post('/actors', json=new_actor, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_create_actor_no_permission(self):
        new_actor = {
            'name': 'Jeffrey',
            'age': 20,
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=new_actor, headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    '''
    update actors
    '''
    def test_edit_actor(self):
        '''
        normal operation
        '''
        update_json = {
            'age': 30
        }
        res = self.client().patch("/actors/1", json=update_json, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['edit_actor'])
        self.assertTrue(data['total_actors'])

    def test_edit_actor_not_found(self):
        '''
        no such actor id in the db
        '''
        actor_id = 10000000
        update_json = {
            'age': 30
        }
        res = self.client().patch(f'/actors/{actor_id}', json=update_json, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_edit_actor_no_permission(self):
        update_json = {
            'age': 30
        }
        res = self.client().patch("/actors/1", json=update_json, headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


    '''
    Test delete actor
    '''
    def test_delete_actor(self):
        '''
        normal operation for delete
        '''
        res = self.client().delete('/actors/1', headers = CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_actor_no_permission(self):
        '''
        assistant can't delete actor
        '''
        res = self.client().delete('/actors/1', headers = CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


    def test_delete_actor_unprocessable(self):
        '''
        no such actor id in the db.
        '''
        actor_id = 100000000
        res = self.client().delete(f'/actors/{actor_id}', headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')

    # Movies
    '''
    Get movies
    '''
    def test_get_movies(self):
        '''
        normal operation
        '''
        res = self.client().get('/movies', headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_get_movies_not_found(self):
        '''
        no movies in the page
        '''
        res = self.client().get('/movies?page=123453456', headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    def test_get_movies_no_authorization(self):
        '''
        no permission provided at all
        '''
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    '''
    CREATE movies
    '''
    def test_create_movie(self):
        '''
        normal operation
        '''
        new_movie = {
            'title': 'John Wick 2',
            'release_date': '2017-2-10'
        }
        res = self.client().post('/movies', json=new_movie, headers=EXECUTIVE_PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    def test_create_in_valid_movie(self):
        '''
        null value in the movies. Can't process
        '''
        new_movie = {
            'title': '',
            'release_date': ''
        }
        res = self.client().post('/movies', json=new_movie, headers=EXECUTIVE_PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_create_movie_no_permission(self):
        '''
        director has no permission to create movie
        '''
        new_movie = {
            'title': 'John Wick 2',
            'release_date': '2017-2-10'
        }
        res = self.client().post('/movies', json=new_movie, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_create_movie_no_authorization(self):
        '''
        no authorizatoin at all.
        '''
        new_movie = {
            'title': 'John Wick 2',
            'release_date': '2017-2-10'
        }
        res = self.client().post('/movies', json=new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    '''
    Edit movies
    '''
    def test_edit_movie(self):
        '''
        normal operation
        '''
        update_json = {
            'title': 'John Wick 100'
        }
        res = self.client().patch("/movies/1",json=update_json, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['edit_movie'])
        self.assertTrue(data['total_movies'])

    def test_edit_movie_unprocessable(self):
        '''
        No such movie to update
        '''
        update_json = {
            'title': 'John Wick 100'
        }
        res = self.client().patch('/movies/1000000', json=update_json, headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_edit_movie_no_permission(self):
        '''
        assistant has no right to edit the movie
        '''
        update_json = {
            'title': 'John Wick 100'
        }
        res = self.client().patch("/movies/1",json=update_json, headers=CASTING_ASSISTANT_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


    '''
    DElETE movies
    '''
    def test_delete_movie(self):
        '''
        normal operation
        '''
        res = self.client().delete('/movies/1', headers=EXECUTIVE_PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_movie_unprocessable(self):
        '''
        no such movie in the db
        '''
        movie_id = 100000000
        res = self.client().delete(f'/movies/{movie_id}', headers=EXECUTIVE_PRODUCER_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable entity')

    def test_delete_movie_no_permission(self):
        '''
        director has no right to delete the movie
        '''
        res = self.client().delete('/movies/1', headers=CASTING_DIRECTOR_AUTH_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

if __name__ == '__main__':
    unittest.main()




