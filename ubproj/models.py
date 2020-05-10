from datetime import datetime
from flask import current_app
from ubproj import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	user_image_file = db.Column(db.String(20), nullable=False, default='userdefault.jpg')
	password = db.Column(db.String(60), nullable=False)
	age = db.Column(db.Integer, nullable=True)
	gender = db.Column(db.String(), nullable=True)
	height = db.Column(db.Integer, nullable=True)
	weight = db.Column(db.Integer, nullable=True)
	education = db.Column(db.String(60), nullable=True)
	address = db.Column(db.String(60), nullable=True)
	environment = db.Column(db.String(60), nullable=True)
	nationality = db.Column(db.String(), nullable=True)
	pets = db.Column(db.String(), nullable=True)
	place_of_birth = db.Column(db.String(), nullable=True)
	normal_or_csection = db.Column(db.String(), nullable=True)
	infant_food = db.Column(db.String(), nullable=True)
	parents_smoking = db.Column(db.String(), nullable=True)
	parents_overweight = db.Column(db.String(), nullable=True)
	parents_nationality = db.Column(db.String(), nullable=True)
	meals = db.relationship('Meal', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.user_image_file}')"



class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    meal_image_file = db.Column(db.String(20), nullable=False, default='mealdefault.jpg')
    content = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Meal('{self.title}', '{self.date_added}', '{self.meal_image_file}')"	






