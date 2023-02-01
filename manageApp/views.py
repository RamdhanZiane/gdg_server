from flask import Blueprint, request, flash, jsonify
from flask_login import login_required, current_user
from . import mysql
import json
from .models import Members, Activities, Events, Departments, USERS_ROLES, EVENTS_ROLES


views = Blueprint('views', __name__)




# ROUTES

@views.route('/favicon.ico')
def favicon():
    # return send_from_directory(STATIC_PATH , 'favicon.ico' , mimetype='image/vnd.microsoft.icon')
    pass
	


@views.route('/', methods=['GET'])
def base():
	# return redirect(FIRST_URL)
    pass

