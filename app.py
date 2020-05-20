import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from auth import AuthError, requires_auth

from models import db_drop_and_create_all, setup_db, Movies, Actors, Performance



def create_app(test_config=None):
    '''create and configure the app'''
    app = Flask(__name__)
    setup_db(app)
    '''
    To initialize the database uncomment the following line
    NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
    MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()



    CORS(app)
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response
    '''
    -------------------------------------------------------------------------------
    API ENDPOINTS
    -------------------------------------------------------------------------------
    '''

    '''
    GET /actors
        it should require the 'get:actors' permission
        it should contain the actor.complete data representation
    returns status code 200 and json {"success": True, "actors": actor} where actors is the list of actors or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def actors(jwt):
        try:
            actors=Actors.query.all()
            return jsonify({
                'success': True,
                'actors': [actor.serialize for actor in actors]
            })
        except:
            abort(404)

    '''
    POST /actors
        it should create a new row in the actors table
        it should require the 'post:actors' permission
        it should contain the actor.complete data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor is an array containing only the newly created actor
    or appropriate status code indicating reason for failure
    '''


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def new_actor(jwt):
        body = request.get_json(force=True)

        if not('name' in body and 'age' in body and 'gender' in body):
            abort(422)


        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = Actors(name=name, age=age, gender=gender)
            actor.create()

            return jsonify({
                'success':True,
                'actor': [actor.serialize]
            })

        except:
            abort(422)

    '''
    PATCH /actor/<id>
        where <id> is the existing model id
        it should respond with a 404 error is <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actor' permission
        it should contain the actor.complete data representation
    returns status code 200 and json {"success": True, "actors": actor} where actor is an array containing only the updated actor
    or appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor=Actors.query.get(id)

        if actor:
            try:
                body = request.get_json()

                name = body.get('name')
                age = body.get('age')
                gender = body.get('gender')

                if name:
                    actor.name = name
                if age:
                    actor.age = age
                if gender:
                    actor.gender = gender

                actor.update()

                return jsonify({
                    'success': True,
                    'actors': [actor.serialize]
                })
            except:
                abort(422)
        else:
            abort(404)

    '''
    DELETE /actor/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or the appropriate status code indicating reason for failure
    '''

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor=Actors.query.get(id)

        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except:
                abort(422)
        else:
            abort(404)
    '''
    GET /movies
        it should require the 'get:movies' permission
        it should contain the movie.complete data representation
    returns status code 200 and json {"success": True, "movies": movie} where movies is the list of movies or appropriate status code indicating reason for failure
    '''


    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def movies(jwt):
        try:
            movies=Movies.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.serialize for movie in movies]
            })
        except:
            abort(404)

    '''
    POST /movies
        it should create a new row in the movies table
        it should require the 'post:movies' permission
        it should contain the movie.complete data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie is an array containing only the newly created movie
    or appropriate status code indicating reason for failure
    '''


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def new_movie(jwt):
        body = request.get_json(force=True)

        if not('title' in body and 'release_date' in body):
            abort(422)
        title = body.get('title')
        release_date = body.get('release_date')

        try:
            movie = Movies(title=title, release_date=release_date)
            movie.create()

            return jsonify({
                'success':True,
                'movies':[movie.serialize]
            })

        except:
            abort(422)

    '''
    PATCH /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error is <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:movie' permission
        it should contain the movie.complete data representation
    returns status code 200 and json {"success": True, "movies": movie} where movie is an array containing only the updated movie
    or appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie=Movies.query.get(id)

        if movie:
            try:
                body = request.get_json()

                title = body.get('title')
                release_date = body.get('release_date')

                if title:
                    movie.title = title
                if release_date:
                    movie.release_date = release_date

                movie.update()

                return jsonify({
                    'success': True,
                    'movies': [movie.serialize]
                })
            except:
                abort(422)
        else:
            abort(404)

    '''
    DELETE /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
    or the appropriate status code indicating reason for failure
    '''

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, id):
        movie = Movies.query.get(id)

        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except:
                abort(422)
        else:
            abort(404)


    '''
    Error Handling
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422



    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            'message': ex.error['description']
        }), 401

    return app

app = create_app()

if __name__ == '__main__':
      app.run()

