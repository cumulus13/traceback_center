import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# def create_app(test_config = None):
app = Flask(__name__, instance_relative_config = True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.from_mapping(SECRET_KEY='1x2c3v4b5n6m7,8.', DATABASES=db)

from models import Traceback

try:
	os.makedirs(app.instance_path)
except OSError:
	pass

# if not test_config:
# 	app.config.from_pyfile('config.py', silent = True)
# else:
# 	app.config.from_mapping(test_config)


@app.route('/')
def index():
	return "<h1><center>WELCOME</center></h1>"

@app.route('/getall')
def get_numbers():
	try:
		track = Traceback.query.all()
		return jsonify([e.serialize() for e in track])
	except Exception as e:
		return str(e)


	# return app


