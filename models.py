from sqlalchemy import Column
from flask_sqlalchemy import SQLAlchemy
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class InheritedMethods(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


read = db.Table('read',
                db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class User(InheritedMethods):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    age = Column(db.Integer)
    book_read = db.relationship("Book", secondary='read', backref=db.backref('user'))

    def __init__(self, name, age, book_read):
        self.name = name
        self.age = age
        self.book_read.id = book_read

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'book_read': [book.id for book in self.book_read]
        }


class Book(InheritedMethods):
    __tablename__ = 'book'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    pages = Column(db.Integer)
    author = db.Column(db.Integer, db.ForeignKey('author.id'))
    reader = db.relationship("User", secondary='read', backref=db.backref('book'))

    def __init__(self, name, pages, author, reader):
        self.name = name
        self.pages = pages
        self.author = author
        self.reader.id = reader

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'pages': self.pages,
            'author': self.author,
            'reader': [book.id for book in self.reader]
        }

    def delete(self):
        self.reader = []
        db.session.commit()
        db.session.delete(self)
        db.session.commit()


class Author(InheritedMethods):
    __tablename__ = 'author'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    books = db.relationship("Book")

    def __init__(self, name, books):
        self.name = name
        self.books.id = books

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [book.format()['id'] for book in self.books]
        }
