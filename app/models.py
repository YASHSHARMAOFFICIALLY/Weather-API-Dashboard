from app import db
from flask_login import UserMixin
from datetime import datetime
class users(db.Model,UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),nullable = False,unique = True)
    password_hash = db.Column(db.String(200),nullable = False)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    country = db.Column(db.String(50),nullable = True)
class Searchhistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable = False)
    city_name = db.Column(db.String(200),nullable = False)
    searched_at = db.Column(db.DateTime,default=datetime.utcnow)
    summary_temp = db.Column(db.Float,nullable = True)
class Favouritecity(db.Model):
    __tablename__ = "favourite_city"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    city_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'city_name', name='unique_user_city'),)

class Forecastday(db.Model):
    __tablename__ = "forecast_day"
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable = False)
    city_name = db.Column(db.String(200),nullable = False)
    date = db.Column(db.Date,nullable = False)
    temp_min = db.Column(db.Float, nullable=True)
    temp_max = db.Column(db.Float, nullable=True)
    simple_condition = db.Column(db.String(50), nullable=True)  
    icon_code = db.Column(db.String(20), nullable=True)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

