import json
import os
import sys
from flask import (
  Flask,
  request,
  jsonify,
  abort
)
from models import (
    setup_db,
    Book,
    User,
    Author
)
from flask_cors import CORS
from auth import AuthError, requires_auth

database_path = os.environ['DATABASE_URL']


def data_format(data):
    return [result.format() for result in data]


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app, database_path)
    CORS(app)
    print("API Connected ...")

    @app.route('/book', methods=['GET'])
    def get_books():
        try:
            data = Book.query.order_by('id').all()
            return jsonify({'books': data_format(data)})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/author', methods=['GET'])
    def get_author():
        try:
            data = Author.query.order_by('id').all()
            return jsonify({'authors': data_format(data)})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/user', methods=['GET'])
    @requires_auth('get:user')
    def get_user(payload):
        try:
            data = User.query.order_by('id').all()
            return jsonify({'users': data_format(data)})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/user/<int:user_id>', methods=['GET'])
    @requires_auth('get:user')
    def get_user_by_id(payload, user_id):
        data = User.query.get(user_id)
        if data is None:
            abort(400)
        return jsonify({'user': data.format()})

    @app.route('/author/create', methods=['POST'])
    @requires_auth('create:author')
    def create_author(payload):
        try:
            body = json.loads(request.get_data())
            name = body['name']
            books = body['book']
        except:
            books = []
        try:
            author = Author(name=name, books=books)
            author.insert()
            return jsonify({"author": author.format()})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/book/create', methods=['POST'])
    @requires_auth('create:book')
    def create_book(payload):
        body = json.loads(request.get_data())
        name = body['name']
        pages = body['pages']
        try:
            author_id = body['author']
        except KeyError:
            raise AuthError({"error": "invalid_request", "description": "There is missing author in request"}, 400)
        except:
            abort(422)
        try:
            book = Book(name=name, pages=pages, author=author_id, reader=[])
            book.insert()
            return jsonify({"book": book.format()})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/user/create', methods=['POST'])
    @requires_auth('create:user')
    def create_user(payload):
        try:
            body = json.loads(request.get_data())
            name = body['name']
            age = body['age']
            book_read = body['book_read']
        except:
            book_read = []
        try:
            user = User(name=name, age=age, book_read=book_read)
            user.insert()
            return jsonify({"user": user.format()})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/user/<int:user_id>/book_read', methods=['PATCH'])
    @requires_auth('create:user')
    def read_book(payload, user_id):
        try:
            body = json.loads(request.get_data())
            book_read = body['book_read']
            # get read books by this user
            book = [Book.query.get(book) for book in book_read]
            user = User.query.get(user_id)
        except TypeError:
            abort(400)
        try:
            # to remove duplicated books join new list with current list in set
            books = set(user.book_read + book)
            user.book_read = list(books)
            user.update()
            return jsonify({"user": user.format()})
        except:
            abort(422, sys.exc_info()[0].__name__)

    @app.route('/user/<int:user_id>/delete', methods=['DELETE'])
    @requires_auth('create:user')
    def delete_user(payload, user_id):
        user = User.query.get(user_id)
        if user is None:
            abort(400)
        user.delete()
        return jsonify({"Success": True})

    @app.route('/author/<int:author_id>/delete', methods=['DELETE'])
    @requires_auth('create:author')
    def delete_author(payload, author_id):
        author = Author.query.get(author_id)
        if author is None:
            abort(400)
        [book.delete() for book in author.books]
        author.delete()
        return jsonify({"Success": True})

    return app


app = create_app()


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "description": "Bad Request, Please change your request data",
        "error": 400
    }), 400


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "success": False,
        "description": "Page Not Found, Please change endpoint request",
        "error": 404
    }), 404


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "description": "Method Not Allowed, Please change method",
        "error": 405
    }), 405


@app.errorhandler(422)
def un_processable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Un Processable, It has a/an {}".format(error.description)
    }), 422


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


if __name__ == '__main__':
    app.run()
