import unittest
import json
import os
from flask_sqlalchemy import SQLAlchemy
from app import app
from models import setup_db, Book, User, Author, database_path


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        # JWT from environment variable
        self.user_jwt = {'Authorization': 'Bearer {}'.format(os.environ['user_token'])}
        self.author_jwt = {'Authorization': 'Bearer {}'.format(os.environ['author_token'])}
        self.invalid_token = {'Authorization': 'Bearer {}'.format(os.environ['invalid_token'])}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_author(self):
        res = self.client().post('/author/create', json={'name': "Jhon Burgos"}, headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['author'])

    def test_create_book(self):
        author_id = Author.query.first().id
        res = self.client().post('/book/create',
                                 json={'name': "War Is Close", 'pages': 250, 'author': author_id},
                                 headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['book'])

    def test_create_user(self):
        book_id = Book.query.first().id
        res = self.client().post('/user/create',
                                 json={'name': "Yousif Shafee", 'age': 25, 'book_read': [book_id]},
                                 headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['user'])

    def test_edit_user(self):
        user_id = User.query.first().id
        book_id = Book.query.order_by(Book.id.desc()).first().id
        res = self.client().patch('/user/{}/book_read'.format(user_id), json={'book_read': [book_id]},
                                  headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['user'])

    def test_get_book(self):
        res = self.client().get('/book', headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['books'])

    def test_get_author(self):
        res = self.client().get('/author', headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['authors'])

    def test_get_user(self):
        res = self.client().get('/user', headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['users'])

    def test_get_spec_user(self):
        first_id = User.query.first().id
        res = self.client().get('/user/{}'.format(first_id), headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['user'])

    def test_delete_user(self):
        user_id = User.query.order_by(User.id.desc()).first().id
        res = self.client().delete('/user/{}/delete'.format(user_id), headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_delete_author(self):
        author_id = Author.query.order_by(Author.id.desc()).first().id
        res = self.client().delete('/author/{}/delete'.format(author_id), headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['Success'])

    def test_error_create_author(self):
        res = self.client().post('/author/create', json={}, headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['error'])

    def test_error_create_book(self):
        res = self.client().post('/book/create', json={'name': "War Is Close", 'pages': 250, 'author': 1000},
                                 headers=self.author_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['error'])

    def test_error_create_user(self):
        res = self.client().post('/user/create', headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['error'])

    def test_error_edit_user(self):
        user_id = User.query.first().id
        res = self.client().patch('/user/{}/book_read'.format(user_id), json={'book_read': [1000]},
                                  headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['error'])

    def test_error_get_book(self):
        res = self.client().get('/book')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'])

    def test_error_get_spec_user(self):
        res = self.client().get('/user/1000', headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def test_error_delete_user(self):
        res = self.client().delete('/user/1000/delete', headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['error'])

    def test_error_delete_author(self):
        author_id = Author.query.order_by(Author.id.desc()).first().id
        res = self.client().delete('/author/{}/delete'.format(author_id), headers=self.user_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue(data['code'])

    def test_invalid_token(self):
        author_id = Author.query.order_by(Author.id.desc()).first().id
        res = self.client().delete('/user/{}/delete'.format(author_id), headers=self.invalid_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['message'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
