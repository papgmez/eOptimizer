#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from flask import Flask, make_response, abort, jsonify, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import Base, Users, Homes
from config import project_constants as const, prod_config
from simulation import Simulation
import datetime as dt
import json

app = Flask(__name__)
app.config.from_object(prod_config)
db = SQLAlchemy(app)
Base.metadata.create_all(bind=db.engine)
# Bootstrap(app)

@app.route('/')
def index():
   return "Welcome to my TFG"

@app.route('/simulation')
def simulation():
   # global current_user
   # Recoger date y consumo
   current_user = db.session.query(Users).get(1)
   current_sim = Simulation(current_user.home, const.C, dt.datetime(2019, 3, 11, 0, 0, 0))
   data = current_sim.optimize()
   result = json.loads(data)

   return make_response(jsonify(result), 200)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=7000)
