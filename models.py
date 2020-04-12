import os
from sqlalchemy import Table, ForeignKey, Column, Integer, Boolean, String, Date, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import crud
from config import database_info

'''
Set up the database to be able to Run CRUD on tables
'''

database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}:{}/{}".format(database_info["db_user"], database_info["db_password"], database_info["db_location"], database_info["db_port"], database_info["db_name"]))

db = SQLAlchemy()

'''
setup_db(app, database_path=database_path)
binds a flask application to a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
db_drop_and_create_all()
drops the database tables and starts fresh
can be used to initialize a clean database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()




'''
Movies Class creates the table for Movies with a foreign key relationship to actors
'''

class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    @property
    def complete(self):
        cast = crud.get_actors_in_movie(self.id)
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'cast': [{
                'actor_id': performance.actor_id,
                'actor_name': performance.actor_name,
            } for performance in cast]
        }

    def __repr__(self):
        return '<Movie %r>' % self.title 




'''
Actors Class creates the table for Actors to be tracked in the DB
'''

class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def details(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    @property
    def complete(self):
        past_performances = crud.get_past_actor_performance(self.id)
        upcoming_performances = crud.get_upcoming_actor_performances(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'past_performances':[{
                'movie_id': performance.movie.id,
                'movie_name': performance.movie.title,
                'release_date': performance.movie.release_date
            } for performance in past_performances],
            'upcoming_performances': [{
                'movie_id': performance.movie.id,
                'movie_name': performance.movie.title,
                'release_date': performance.movie.release_date
            } for performance in upcoming_performances],
            'past_performance_total': len(past_performances),
            'upcoming_performance_total': len(upcoming_performances)
        }


    def __repr__(self):
        return '<Artist %r>' % self.name


'''
Performance Table
This table allows for the relationship of many to many for movies and actors
'''

class Performance(db.Model):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    movie_id = Column(Integer, ForeignKey('Movie.id'), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('movies', cascade="all,delete"))
    actor_id = Column(Integer, ForeignKey('Artist.id'), nullable=False)
    actor = db.relationship('Actor', backref=db.backref('actors', cascade="all, delete"))

    def create(self):
        db.session.add(self)
        db.session.commit()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }

    @property
    def performance(self):
        return {
            'actor_id': self.Actor.id,
            'actor_name': self.Actor.name,
            'movie_title': self.Movie.title,
            'rating': self.rating
            }

