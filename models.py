import os
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "casting_agency"
# database_path = 'postgresql:///casting_agency'
database_path = 'postgres://postgres:test123@localhost:5432/casting_agency'

# database_name = "cast_agency_test"
# database_path = 'postgresql:///cast_agency_test'

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # uncomment it when testing 
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    db.app = app
    db.init_app(app)
    db.create_all()

def drop_and_create_all():
    '''
    drop table and flush in fresh data
    '''
    db.drop_all()
    db.create_all()
    init_data()

def init_data():
    '''
    insert new data to the clean data base
    '''
    actor = Actor(name='Jeffrey', age=20, gender='Male')
    movie = Movie(title='John Wick', release_date='2014-10-24')
    performance = Performance.insert().values(movie_id = movie.id, actor_id = actor.id)
    actor.insert()
    movie.insert()
    db.session.execute(performance)
    db.session.commit()


####### a relation table for junction Actor and Movie tables
Performance = db.Table('Performance', db.Model.metadata,
    Column('movie_id', Integer, db.ForeignKey('movies.id')),
    Column('actor_id', Integer, db.ForeignKey('actors.id')),
)

class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'Id': self.id,
            'Name': self.name,
            'Age': self.age,
            'Gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    actors = db.relationship('Actor', secondary=Performance, backref=db.backref('performance'), lazy='joined')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'Id': self.id,
            'Title': self.title,
            'Release Date': self.release_date,
        }


