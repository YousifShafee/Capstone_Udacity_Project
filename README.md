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

    1. Its public get a list of books without authorization.

###### Sample

      curl https://capstoneudacityproject.herokuapp.com/book

      {
        "movies":
          [
            {
              "id":1,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":2,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":3,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie2"
            },
            {
              "id":4,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":5,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {{
              "id":6,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":7,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            },
            {
              "id":8,
              "release_date":"Wed, 22 May 2019 00:00:00 GMT",
              "title":"Movie1"
            }
          ],
        "success":true,
        "total_movies":8
      }

##### DELETE /movies/{movie_id}

      1. Deletes a movie of the given id.
      2. Returns the success value.

###### Sample

      curl -H "Authorization: Bearer ${auth_token_cast_asst}" -X DELETE https://capstoneudacityproject.herokuapp.com/movies/5

        {
          "success": true
        }

##### POST /movies

      1. Adds a new movie to the movies list.
      2. Returns a newly created Id and success value.

###### Sample

      curl -d '{"title":"Movie1", "release_date":"05-22-2019"}'
      -H "Content-Type: application/json"
      -H "Authorization: Bearer ${auth_token_cast_asst}"
      -X POST https://capstoneudacityproject.herokuapp.com/movies

      {
        "new id":8,
        "success":true
      }

##### PATCH /movies/{movie_id}

      1. Updates a movie data based on given id.
      2. Returns success value.

###### Sample
      curl -d '{"title":"Movie2", "release_date":"02/22/2017"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${auth_token_cast_asst}" -X PATCH https://capstoneudacityproject.herokuapp.com/movies/2

      {
        "success":true
      }

##### GET /actors

    1. Returns a list of actors, success value and total actors.
    <!-- 2. Results are also paginated. -->

###### Sample:
      curl -H "Authorization: Bearer ${auth_token_cast_asst}" https://capstoneudacityproject.herokuapp.com/actors

      {
        "actors":
          [
            {
              "age":24,
              "gender":"F",
              "id":1,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":2,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":3,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":4,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":5,
              "name":"Actor 1"
            },
            {
              "age":24,
              "gender":"F",
              "id":6,
              "name":"Actor 1"
            }
          ],
        "success":true,
        "total_actors":6
      }


##### POST /actors

      1. Adds a new actor to the actors list.
      2. Returns a newly created Id and a success value.

###### Sample
         curl -d '{"name":"Actor 1", "age":"24", "gender":"F"}' -H "Content-Type: application/json" -H "Authorization: Bearer ${auth_token_cast_asst}" -X POST https://capstoneudacityproject.herokuapp.com/actors

        {
          "new id":9,
          "success":true
        }

##### DELETE /actors/{actor_id}

      1. Deletes an actor of the given id.
      2. Returns the success value.

###### Sample

      curl -H "Authorization: Bearer ${auth_token_cast_asst}" -X DELETE https://capstoneudacityproject.herokuapp.com/actors/5

      {
        "success": true
      }

##### PATCH /actors/{actor_id}

      1. Updates an actors data based on given id.
      2. Returns updated actor information and success value.

###### Sample
        curl -d '{"name":"Actor 1 F", "age":"24", "gender":"F"}'
        -H "Content-Type: application/json"
        -H "Authorization: Bearer ${auth_token_cast_asst}"
        -X PATCH https://capstoneudacityproject.herokuapp.com/actors/2

          {
            "updateActor":
            {
              "age":24,
              "gender":"F",
              "id":2,
              "name":"Actor 1 F"
            },
            "success":true
          }