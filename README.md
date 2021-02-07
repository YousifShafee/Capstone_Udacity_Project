# 2 Read

To Read books this application help user to creating an account and mark the books he was read.

This application allows to add new author and his books, get list of all author, books and users data. Update read books and delete authors accounts and users accounts.

This project is the Capstone project for (full stack nanodegree program at Udacity).


## Getting Started

I have created a REST API 2 Read.
This API is implemented using following:

 - Python3, Flask
 - SQLAlchemy ORM
 - PostgreSQL Database

## Pre-requisites

Python3, pip should be installed on local machine.

### Backend

From the root folder run requirements.txt.

    pip install -r requirements.txt

#### Database Setup
Database is hosted live via Heroku

#### Run Application

To run the application, execute:

First setup the environment variable by running following command:

    setup_test.sh

in linux

    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run

in windows

    set FLASK_APP=app.py
    set FLASK_ENV=development
    flask run


## Testing
To run the tests navigate to root folder and run the following commands:

    setup.sh
    python3 test_app.py



## API Reference

### Getting Started

    1. Base URL: Application is hosted on Heroku. Application also runs locally.
        Application is hosted at :
        https://capstoneudacityproject.herokuapp.com/

    2. Authentication: Application uses auth0 API for authentication.

      Application has tow roles with their respective RBAC:
          * User
              * Get all Users data
              * Add new User
              * Edit Books as read for users
              * Delete Users
          * Author
              * Add new Books
              * Add new Authors
              * Delete Authors
      
      To test the end points using curl first run the setup.sh file to setup the environment variables.

      $ setup.sh
      setup.sh has tokens for all roles.

      example:
      curl -H "Authorization: Bearer ${user_token}" https://capstoneudacityproject.herokuapp.com/user/create


### Error Handling

  Errors are returned as json objects:
    {
        "success": False,
        "description": "Page Not Found",
        "error": 404
    }

  Application returns following errors:

  - 200 - Success

  - 400 - Bad Request

  - 401 - Authorization header is expected

  - 403 - Payload does not contain "permissions" string.

  - 404 - Page Not Found

  - 405 - Method not allowed

  - 422 - Not processable

### End Points

Application has following end points.

    - GET
      - /book
      - /author
      - /user
      - /user/{user_id}
    - POST
      - /author/create
      - /book/create
      - /user/create
    - PATCH
      - /user/{user_id}/book_read
    - DELETE
      - /user/{user_id}/delete
      - /author/{author_id}/delete


##### GET /book

     Its public which get a list of books without authorization.
     data:
        Book id,
        list of Author id who write this Book,
        name of book,
        number of book pages
        Users id Who mark this Book as read
        

###### Sample

      curl https://capstoneudacityproject.herokuapp.com/book

      {
        "books": [
            {
                "author": 2,
                "id": 3,
                "name": "War Is Close",
                "pages": 200,
                "reader": [4]
            },
            {
                "author": 3,
                "id": 4,
                "name": "The Love",
                "pages": 200,
                "reader": []
            }]
      }

##### GET /author

      Its public which get a list of Authors without authorization.
      data:
        Author id,
        Author name,
        list of Books id authored by him
        

###### Sample

      curl https://capstoneudacityproject.herokuapp.com/author

        {
        "authors": [
            {
                "books": [3],
                "id": 2,
                "name": "Mohamed Aly"
            },
            {
                "books": [4,6,8],
                "id": 3,
                "name": "Mohamed Aly"
            }]
        }

##### GET /user

      Return a list of Users by User role authorization.
      data:
        User id,
        User age,
        User name,
        list of Books id which mark as read by this User

###### Sample

      curl -H "Authorization: Bearer ${user_token}" https://capstoneudacityproject.herokuapp.com/user

        {
        "users": [
            {
                "age": 19,
                "book_read": [3,8],
                "id": 4,
                "name": "Shafee"
            },
            {
                "age": 19,
                "book_read": [],
                "id": 5,
                "name": "Yousif"
            }]
        }

##### GET /user/{user_id}

      Return User by User id and User role authorization.
      data:
        User id,
        User age,
        User name,
        list of Books id which mark as read by this User

###### Sample

      curl -H "Authorization: Bearer ${user_token}" https://capstoneudacityproject.herokuapp.com/user/{user_id}

        {
        "user": {
            "age": 19,
            "book_read": [3,8],
            "id": 4,
            "name": "Shafee"
            }
        }

##### POST /user/create

      Create new User by User role authorization.
      Return data of new user.
      
      required data:
        User age,
        User name,
        [optional] list of Books id which mark as read by this User

###### Sample

      curl -d '{"name":"Ahmed Khalifa","book":[1],"age": 19}'
      -H "Content-Type: application/json"
      -H "Authorization: Bearer ${user_token}"
      -X POST https://capstoneudacityproject.herokuapp.com/user/create

        {
         "user": {
            "age": 19,
            "book_read": [1],
            "id": 4,
            "name": "Ahmed Khalifa"
            }
        }

##### POST /author/create

      Create new Author by Author role authorization.
      Return data of new Author.
      
      required data:
        Author name,
        [optional] list of Books id which authored by this Author.

###### Sample

      curl -d '{"name":"Jhon","book":[1]}'
      -H "Content-Type: application/json"
      -H "Authorization: Bearer ${author_token}"
      -X POST https://capstoneudacityproject.herokuapp.com/author/create

        {
         "author": {
            "books": [1],
            "id": 13,
            "name": "Jhon"
            }
        }


##### POST /book/create

      Create new Book by Author role authorization.
      Return data of new Book.
      
      required data:
        Book name,
        number of Book pages,
        Author id who write this Book

###### Sample

      curl -d '{"name": "Finaly","pages": 200,"author":4}'
      -H "Content-Type: application/json"
      -H "Authorization: Bearer ${author_token}"
      -X POST https://capstoneudacityproject.herokuapp.com/book/create

        {
         "book": {
            "author": 4,
            "id": 11,
            "name": "Finaly",
            "pages": 200,
            "reader": []
            }
        }

##### PATCH /user/{user_id}/book_read

      Add new Book as read in User data by User role authorization.
      Return data of User.
      
      required data:
        List of Books id which want to add it as read
    
      Note: this endpoint to only add books as read in user data,
          so the previous Books will still mark as read and can't delete it from user data.

###### Sample

      curl -d '{"book_read": [3]}'
      -H "Content-Type: application/json"
      -H "Authorization: Bearer ${user_token}"
      -X POST https://capstoneudacityproject.herokuapp.com/user/{user_id}/book_read

        {
            "user": {
                "age": 19,
                "book_read": [3,8],
                "id": 4,
                "name": "Shafee"
            }
        }


##### DELETE /user/{user_id}/delete

      Delete User data by User id and User role authorization.
      Return Success message.

###### Sample

      curl -H "Authorization: Bearer ${user_token}"
      -X POST https://capstoneudacityproject.herokuapp.com/user/{user_id}/delete

        {"Success": True}

##### DELETE /author/{author_id}/delete

      Delete Author and his Books data by Author id and Author role authorization.
      Return Success message.

###### Sample

      curl -H "Authorization: Bearer ${author_token}"
      -X POST https://capstoneudacityproject.herokuapp.com/author/{author_id}/delete

        {"Success": True}
