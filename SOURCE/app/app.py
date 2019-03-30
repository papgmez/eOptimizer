#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from flask import Flask, make_response, abort, jsonify, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import Base, Users, Homes
from config import project_constants as const, prod_config
import api_aemet as aemet
import api_esios as esios
import Simulation

app = Flask(__name__)
app.config.from_object(prod_config)
db = SQLAlchemy(app)
Base.metadata.create_all(bind=db.engine)
# Bootstrap(app)

@app.route('/')
def index():
   return "Welcome to my TFG"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=7000)
