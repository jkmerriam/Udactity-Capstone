import os
from sqlalchemy import Table, ForeignKey, Column, Integer, Boolean, String, Date, Float, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from config.py import database_info

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
Performance Association Table
This table allows for the relationship of many to many for movies and actors
'''

performance_table = Table('performance', db.Model.metadata,
        Column('Movie_id', Integer, ForeignKey('movies.id')),
        Column('Actor_id', Integer, ForeignKey('actors.id')),
        Column('actor_rating', Integer))


'''
Movies Class creates the table for Movies with a foreign key relationship to actors
'''

class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(db.ARRAY(String))
    release_date = Column(Date)
    actors = db.relationship('Actor', secondary=Performance, backref=db.backref('performances'))

    def __init__(self, title, genres, release_date):
        self.title = title
        self.genres = genres
        self.release_date = release_date

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
            'title': self.title,
            'genres': self.genres,
            'release_date': self.release_date
        }


'''
Actors Class creates the table for Actors to be tracked in the DB
'''

class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    genres = Column(db.ARRAY(String))
    seeking_work = Column(Boolean)

    def __init__(self, name, age, gender, genres, seeking_work):
        self.name = name
        self.age = age
        self.gender = gender
        self.genres = genres
        self.seeking_work = seeking_work

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
            'genres': self.genres,
            'seeking_work': self.seeking_work
        }






