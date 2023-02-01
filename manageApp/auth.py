from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Members
from werkzeug.security import generate_password_hash, check_password_hash
from . import mysql
from flask_login import login_user, login_required, logout_user, current_user

import dns.resolver
import socket
import smtplib , imaplib
import re


auth = Blueprint('auth', __name__)




def is_admin(user_id) :
	is_admin = Members.query.filter(Members.member_id==user_id,
									mysql.or_(Members.role=='leader',Members.role=='hr')).first()
	if is_admin:
		return True
		
	return False
	



@auth.route('/signin', methods=['POST'])
def signin():
	data = {}
	
	email = request.form.get('email')
	password = request.form.get('password')

	user = Members.query.filter(Members.email==email,
								mysql.or_(Members.role=='leader',Members.role=='hr')).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Email does not exist.'
		return jsonify(data)
	
	if not check_password_hash(user.password, password):
		data['code'] = 400
		data['message'] = 'Incorrect password, try again.'
		return jsonify(data)
	
	login_user(user, remember=True)
	
	data['code'] = 200
	data['message'] = 'Logged in successfully!'
	return jsonify(data)



@auth.route('/signout')
@login_required
def signout():
	logout_user()
	
	data = {}
	data['code'] = 200
	data['message'] = 'Logged out successfully!'
	return jsonify(data)
   
   

@auth.route('/signup', methods=['POST'])
@login_required
def signup():
	data = {}
	
	if not is_admin(current_user.member_id) :
		data['code'] = 400
		data['message'] = 'you are not allowed to perform this action'
		return jsonify(data)
		
	
	email = request.form.get('email')
	# first_name = request.form.get('firstName')
	password1 = request.form.get('password1')
	password2 = request.form.get('password2')

	user = Members.query.filter_by(email=email).first()
	if not user:
		data['code'] = 400
		data['message'] = 'Member does not exist.'
		return jsonify(data)
		
	# if not IsValidEmail(email) :
		# data['code'] = 400
		# data['message'] = 'Email not valid.'
		# return jsonify(data)
		
	# if len(first_name) < 4:
		# data['code'] = 400
		# data['message'] = 'First name must be greater than 3 character.'
		# return jsonify(data)
	   
	if len(password1) < 8:
		data['code'] = 400
		data['message'] = 'Password must be at least 8 characters.'
		return jsonify(data)
	
	if password1 != password2:
		data['code'] = 400
		data['message'] = "Passwords don't match, reconfirm the password."
		return jsonify(data)
	   
	# new_user = Members(email=email, 
					# first_name=first_name, 
					# password=generate_password_hash(password1, method='sha256'))
	# mysql.session.add(new_user)
	
	user.role = 'hr'
	user.password = generate_password_hash(password1, method='sha256')
	
	mysql.session.commit()
	
	data['code'] = 200
	data['message'] = 'Account created successfully.'
	return jsonify(data)
