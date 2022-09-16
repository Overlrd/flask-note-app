from flask import Blueprint , render_template , request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user , login_required, logout_user , current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	email = request.form.get('email')
	password = request.form.get('password')
	email = str(email)
	l = len(email)

	user = User.query.filter_by(email=email).first()
	if user :
		if check_password_hash(user.password, password):
			flash('Logged in Successfully', category='success')
			login_user(user , remember=True)
			return redirect(url_for('views.home'))
		else:
			flash('Incorrect Email or Password , Try again', category='error')
	else:
		pass


	return render_template("login.html", user= current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
	
		user = User.query.filter_by(email=email).first()
		if user:
			flash('Email already exists', category='error')

		elif len(email) < 4:
			flash('Email must be greater than 4 characters.', category='error')
		elif len(firstName) < 2:
			flash('First Name must be greater than 1 character.', category='error')
		elif password1 != password2:
			flash('Passwords don\'t match.', category='error')
		elif len(password1) < 4:
			flash('Password must be greater than 4 characters ', category='error')
		else :

			new_user = User(email=email, first_name= firstName, password= generate_password_hash(password1, method='sha256' ))
			db.session.add(new_user)
			db.session.commit()
			flash('Account created !', category='success')
			login_user(new_user , remember=True)
			return redirect(url_for('auth.login'))

	return render_template("signup.html", user=current_user)