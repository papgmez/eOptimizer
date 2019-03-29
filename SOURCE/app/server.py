#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from flask import Flask, make_response, abort, jsonify, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import project_constants as const, config
import api_aemet as aemet
import api_esios as esios
import Simulation

app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)
db = SQLAlchemy(app)

@app.route('/')
def index():
   return "Welcome to my TFG"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=7000)
