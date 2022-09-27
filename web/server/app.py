import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# def create_app(test_config = None):
app = Flask(__name__, instance_relative_config = True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.from_mapping(SECRET_KEY='1x2c3v4b5n6m7,8.', DATABASES=db)

from models import *

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
def get_all():
	try:
		track = Traceback.query.order_by(Traceback.id.desc()).all()
		return jsonify([e.serialize() for e in track])
	except Exception as e:
		return str(e)

@app.route('/gettracebacktype')
def get_traceback_type():
	try:
		track = TracebackType.query.all()
		return jsonify([e.serialize() for e in track])
	except Exception as e:
		return str(e)

@app.route('/get/<numbers>')
def get_numbers(numbers):
	try:
		track = Traceback.query.limit(numbers).all()
		return jsonify([e.serialize() for e in track])
	except Exception as e:
		return str(e)

@app.route('/search')
def search():
	tb = request.args.get('tb', '')
	tp = request.args.get('tp', '')
	vl = request.args.get('vl', '')
	date = request.args.get('date', '')
	app = request.args.get('app', '')
	host = request.args.get('host', '')
	order = request.args.get('order', 'asc')
	limit = request.args.get('limit', 2)
	
	try:
		if order == 'desc':
			track = Traceback.query.filter(Traceback.vl.ilike("%" + vl + "%")).filter(Traceback.tb.ilike("%" + tb + "%")).filter(Traceback.tp.ilike("%" + tp + "%")).filter(Traceback.date.ilike("%" + date + "%")).filter(Traceback.app.ilike("%" + app + "%")).filter(Traceback.host.ilike("%" + host + "%")).order_by(Traceback.id.desc()).limit(limit).all()
		else:
			track = Traceback.query.filter(Traceback.vl.ilike("%" + vl + "%")).filter(Traceback.tb.ilike("%" + tb + "%")).filter(Traceback.tp.ilike("%" + tp + "%")).filter(Traceback.date.ilike("%" + date + "%")).filter(Traceback.app.ilike("%" + app + "%")).filter(Traceback.host.ilike("%" + host + "%")).order_by(Traceback.id.asc()).limit(limit).all()
		return jsonify([e.serialize() for e in track])
	except SQLAlchemyError as err:
		return jsonify(message='not found.'), 400


	# return app


