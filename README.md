# Udactity-Capstone
Udacity Nano Degree Capston Casting Agency

## Motivation
The motivation for this project was to demonstrate my ability to build a Full Stack Web Application with the knowledge gained during the course. This final project encompasses the following technical topics:
  1. Database Modeling(PostgreSQL and SQLAlchemy)
  2. API to perform CRUD operations on the Database using Flask
  3. Authorization of the API endpoints as well as RBAC and Authentication with Auth0
  4. Automated Testing
  5. Deployment to Heroku

##Running Locally
In order to run the application you must be in the same directory as app.py. Python3 and Postgres are required to run this project.

###Set Up environment
To start the server locally following the instructions below:

  1. Create and Activate Virtual Environment:
    ```
    virtualenv --no-site-packages casting_agency
    souce casting_agency/bin/activate
    ```

  2. Install the Dependencies:
    ```
    pip install -r requirements.txt
    ```

  3. Setup Database(only necessary to run locally):
    * Access config.py and edit the following dictionary
      ```
      database_info = {
       "db_name" : "db_name",
       "db_user" : "use_name", # default postgres user name
       "db_password" : None, # if applicable. If no password, just type in None
       "db_location": "localhost:5432",
      }
      ```

  4. Setup Auth0:
    * Note: For those reviewing the project, there are tokens below to assist in testing the API
    * To set up Auth0 for your own app edit the following dict
      ```
      auth0_info={
        "AUTH0_DOMAIN" : "jamie-merriam.auth0.com",
        "ALGORITHMS" : ["RS256"],
        "API_AUDIENCE": "casting_agency"
      }
      ```

  5. Start the Server:
    ```
    export FLASK_APP=app.py
    flask run
    ```

  6. Run Tests:
    ```
    python test_agency.py
    ```

##API Documentation
###1. GET /actors
Queries the Database for all Actors
  * Require permission: 'get:actors'
  * Returns:
    - List of actors in dict form with fields:
      * Id: Integer
      * Name: String
      * Age: Integer
      * Gender: String
    - Success: Boolean

Example Response
  {
    "actors": [
        {
            "age": 33,
            "gender": "Male",
            "id": 1,
            "name": "Udacity"
        }
    ],
    "success": true
}

Errors
  * Attempting to GET /actors/ will result in the following error
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }

###2. POST /actors
Insert new Actor in to the Database
  * Require permission: 'post:actors'
  * Request Header:
    - Application/JSON
      * Name: String
      * Age: Integer
      * Gender: String
  * Returns:
    - Actor in dict form with fields:
      * Id: Integer
      * Name: String
      * Age: Integer
      * Gender: String
    - Success: Boolean

Example Response
{
    "actor": [
        {
            "age": 22,
            "gender": "Male",
            "id": 3,
            "name": "Curious Case of FSND"
        }
    ],
    "success": true
}

Errors
  * Attempting to POST /actors with incomplete information will result in the following error
    {
      "error": 422,
      "message": "unprocessable",
      "success": false
    }

###3. PATCH /actors
Update Actor in the Database
  * Require permission: 'patch:actors'
  * Requires Request Arguments:
    - Actor ID: Integer
  * Requires Data to Update Request Header:
    - Application/JSON
      * Name: String
      * Age: Integer
      * Gender: String
  * Returns:
    - Actor in dict form with fields:
      * Id: Integer
      * Name: String
      * Age: Integer
      * Gender: String
    - Success: Boolean

Example Response
{
    "actor": [
        {
            "age": 22,
            "gender": "Male",
            "id": 3,
            "name": "Curious Case of FSND"
        }
    ],
    "success": true
}

Errors
  * Attempting to PATCH /actors/'id' with invalid id will result in the following error
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }

###4. DELETE /actors
Delete Actor in the Database
  * Require permission: 'delete:actors'
  * Requires Request Arguments:
    - Actor ID: Integer
  * Returns:
    * Id: Integer
    * Success: Boolean

Example Response
{
    "delete": "3",
    "success": true
}

Errors
  * Attempting to DELETE /actors/'id' with invalid id will result in the following error
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }


###5. GET /movies
Queries the Database for all Movies
  * Require permission: 'get:movies'
  * Returns:
    - List of movies in dict form with fields:
      * Id: Integer
      * Title: String
      * Release_date: Date
    - Success: Boolean

Example Response
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 19 May 2020 00:00:00 GMT",
            "title": "Curious Case of FSND"
        }
    ],
    "success": true
}

Errors
  * Attempting to GET /movies/ will result in the following error
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }

###6. POST /movies
Insert new Movie in to the Database
  * Require permission: 'post:movies'
  * Request Header:
    - Application/JSON
      * Title: String
      * Release_date: Date
  * Returns:
    - Movie in dict form with fields:
      * Id: Integer
      * Title: String
      * Release_date: Date
    - Success: Boolean

Example Response
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 19 May 2020 00:00:00 GMT",
            "title": "Curious Case of FSND"
        }
    ],
    "success": true
}

Errors
  * Attempting to POST /movies with incomplete information will result in the following error
    {
      "error": 422,
      "message": "unprocessable",
      "success": false
    }

###7. PATCH /movies
Update Movie in the Database
  * Require permission: 'patch:movies'
  * Requires Request Arguments:
    - Movie ID: Integer
  * Requires Data to Update Request Header:
    - Application/JSON
      * Title: String
      * Release_date: Date
  * Returns:
    - Movie in dict form with fields:
      * Id: Integer
      * Title: String
      * Release_date: Date
    - Success: Boolean

Example Response
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 19 May 2020 00:00:00 GMT",
            "title": "Curious Case of FSND"
        }
    ],
    "success": true
}

Errors
  * Attempting to PATCH /movies/'id' with invalid id will result in the following error
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }

###8. DELETE /movies
Delete Movie in the Database
  * Require permission: 'delete:movies'
  * Requires Request Arguments:
    - Movie ID: Integer
  * Returns:
    * Id: Integer
    * Success: Boolean

Example Response
{
    "delete": "3",
    "success": true
}

Errors
  * Attempting to DELETE /movies/'id' with invalid id will result in the following error
    {
      "error": 404,
      "message": "resource not found",
      "success": false
    }

