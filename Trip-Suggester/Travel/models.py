from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'UserInfo'
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(128))
    LastLogin = db.Column(db.DateTime)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.Name}>'
    
class TripInputs(db.Model):
    __tablename__ = 'TripInput'
    UserID = db.Column(db.Integer, db.ForeignKey('UserInfo.UserID'))
    TripID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String(80), nullable=False)
    Budget = db.Column(db.Integer, nullable=False)
    Days = db.Column(db.Integer, nullable=False)
    Reason = db.Column(db.String(80), nullable=False)
    Weather = db.Column(db.String(80), nullable=False)
    Food = db.Column(db.String(80), nullable=False)
    Continent = db.Column(db.String(80), nullable=False)
    beaches_and_relaxation = db.Column(db.Boolean, default=False)
    food_and_culinary_experiences = db.Column(db.Boolean, default=False)
    sports_and_events = db.Column(db.Boolean, default=False)
    museums_and_historical_sites = db.Column(db.Boolean, default=False)
    hiking_and_outdoor_adventures = db.Column(db.Boolean, default=False)
    nature_and_wildlife = db.Column(db.Boolean, default=False)
    shopping = db.Column(db.Boolean, default=False)
    nightlife_and_entertainment = db.Column(db.Boolean, default=False)
    Country = db.Column(db.String(80))

class LikedTrips(db.Model):
    __tablename__ = 'LikedTrips'
    UserID = db.Column(db.Integer, db.ForeignKey('UserInfo.UserID'))
    TripID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String(80), nullable=False)
    Budget = db.Column(db.Integer, nullable=False)
    Days = db.Column(db.Integer, nullable=False)
    Reason = db.Column(db.String(80), nullable=False)
    Weather = db.Column(db.String(80), nullable=False)
    Food = db.Column(db.String(80), nullable=False)
    Continent = db.Column(db.String(80), nullable=False)
    beaches_and_relaxation = db.Column(db.Boolean, default=False)
    food_and_culinary_experiences = db.Column(db.Boolean, default=False)
    sports_and_events = db.Column(db.Boolean, default=False)
    museums_and_historical_sites = db.Column(db.Boolean, default=False)
    hiking_and_outdoor_adventures = db.Column(db.Boolean, default=False)
    nature_and_wildlife = db.Column(db.Boolean, default=False)
    shopping = db.Column(db.Boolean, default=False)
    nightlife_and_entertainment = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<TripInputs {self.TripID}>'