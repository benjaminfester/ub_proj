from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from ubproj import db
from ubproj.models import Meal
from ubproj.meals.forms import AddMealForm

meals = Blueprint('meals', __name__)


@meals.route('/meal/add', methods=['GET', 'POST'])
@login_required
def add_meal():
    form = AddMealForm()
    if form.validate_on_submit():
    	meal = Meal(title=form.title.data, content=form.content.data, calories=form.calories.data, author=current_user)
    	db.session.add(meal)
    	db.session.commit()
    	flash('Your meal has been added!', 'success')
    	return redirect(url_for('users.user_meals', username=current_user.username))
    return render_template('add_meal.html', title='Add Meal', form=form, legend='Add Meal')

@meals.route('/meal/<int:meal_id>')
def meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    return render_template('meal.html', title=meal.title, meal=meal)


@meals.route('/meal/<int:meal_id>/update', methods=['GET', 'POST'])
@login_required
def update_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    if meal.author != current_user:
        abort(403)
    form = AddMealForm()
    if form.validate_on_submit():
        meal.title = form.title.data
        meal.content = form.content.data
        meal.calories = form.calories.data
        db.session.commit()
        flash('Your meal has been updated!', 'success')
        return redirect(url_for('meals.meal', meal_id=meal.id))
    elif request.method =='GET':
        form.title.data = meal.title
        form.content.data = meal.content
        form.calories.data = meal.calories
    return render_template('add_meal.html', title='Update Meal', form=form, legend='Update Meal')


@meals.route('/meal/<int:meal_id>/delete', methods=['POST'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    if meal.author != current_user:
        abort(403)
    db.session.delete(meal)
    db.session.commit()
    flash('Your meal has been deleted!', 'info')
    return redirect(url_for('users.user_meals', username=current_user.username))


