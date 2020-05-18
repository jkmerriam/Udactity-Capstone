import os
from sqlalchemy import Table, ForeignKey, Column, Integer, Boolean, String, Date, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from config import database_info

'''
Set up the database to be able to Run CRUD on tables
'''

# database_path = os.environ.get('DATABASE_URL', "postgres://{}:{}@{}:{}/{}".format(database_info["db_user"], database_info["db_password"], database_info["db_location"], database_info["db_port"], database_info["db_name"]))

db = SQLAlchemy()

'''
setup_db(app, database_path=database_path)
binds a flask application to a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://jamesmerriam@localhost:5432/casting_agency'
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
    db_init_values()
'''
Initialize the database with values'
'''
def db_init_values():
    new_movie = (Movies(title='Curious Class of FSND', release_date=date.today()))
    new_actor = (Actors(name='Jamie Merriam', gender="Male", age=26))
    new_performance = (Performance(rating=95, movie_id=new_movie.id, movie=new_movie, actor_id=new_actor.id, actor=new_actor))

    new_movie.create()
    new_actor.create()
    new_performance.create()
    db.session.commit()



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
            'release_date': self.release_date,
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

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
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
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    movie = db.relationship('Movies', backref=db.backref('movies', cascade="all,delete"))
    actor_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
    actor = db.relationship('Actors', backref=db.backref('actors', cascade="all, delete"))

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

