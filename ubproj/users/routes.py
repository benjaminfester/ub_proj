from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from ubproj import db, bcrypt
from ubproj.models import User, Meal
from ubproj.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from ubproj.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register_page():
	if current_user.is_authenticated:
		return redirect(url_for('main.home_page'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created. You can now log in!', 'success')
		return redirect(url_for('users.login_page'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login_page():
	if current_user.is_authenticated:
		return redirect(url_for('main.home_page'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home_page'))
		else:
			flash('Login was unsuccessful. Check email and password', 'danger')
	return render_template('login.html', title='Log In', form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home_page'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.user_image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.age = form.age.data
		current_user.gender = form.gender.data
		current_user.height = form.height.data
		current_user.weight = form.weight.data
		current_user.education = form.education.data
		current_user.address = form.address.data
		current_user.environment = form.environment.data
		current_user.nationality = form.nationality.data
		current_user.pets = form.pets.data
		current_user.place_of_birth = form.place_of_birth.data
		current_user.normal_or_csection = form.normal_or_csection.data
		current_user.infant_food = form.infant_food.data
		current_user.parents_smoking = form.parents_smoking.data
		current_user.parents_overweight = form.parents_overweight.data
		current_user.parents_nationality = form.parents_nationality.data

		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account_page'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.age.data = current_user.age
		form.gender.data = current_user.gender
		form.height.data = current_user.height
		form.weight.data = current_user.weight
		form.education.data = current_user.education
		form.address.data = current_user.address
		form.environment.data = current_user.environment
		form.nationality.data = current_user.nationality
		form.pets.data = current_user.pets
		form.place_of_birth.data = current_user.place_of_birth
		form.normal_or_csection.data = current_user.normal_or_csection
		form.infant_food.data = current_user.infant_food
		form.parents_smoking.data = current_user.parents_smoking
		form.parents_overweight.data = current_user.parents_overweight
		form.parents_nationality.data = current_user.parents_nationality


	user_image_file = url_for('static', filename='pics/' + current_user.user_image_file)
	return render_template('account.html', title='Account', user_image_file=user_image_file, form=form)



@users.route('/user_meals/<string:username>', methods=['GET', 'POST'])
@login_required
def user_meals(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    meals = Meal.query.filter_by(author=user)\
        .order_by(Meal.date_added.desc())\
        .paginate(page=page, per_page=6)
    return render_template('user_meals.html', title='Meals', meals=meals, user=user)



















