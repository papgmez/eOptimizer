#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

# from pdb import set_trace as breakpoint

from flask import Flask, make_response, abort, jsonify, request, redirect, url_for, render_template, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from models import Base, Users, Homes
from config import project_constants as const, prod_config
from simulation import Simulation
import datetime as dt
import json
import os

app = Flask(__name__)
app.config.from_object(prod_config)
db = SQLAlchemy(app)
Base.metadata.create_all(bind=db.engine)
# Bootstrap(app)

currentUser = None
login_attempts = 0

@app.route('/')
def index():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      #return render_template('index.html')
      return "Welcome to my TFG"

@app.route('/signup', methods=['POST'])
def sign_up():
   global currentUser
   # ---- creating user ----
   user = Users()
   user.name = request.form['form-first-name']
   user.lastname = request.form['form-last-name']
   user.email = request.form['form-email']
   user.set_password(request.form['form-newpassword'])

   db.session.add(user)
   try:
      db.session.commit()
   except IntegrityError:
      # User Error
      return render_template('login.html', signup_error='An Error has occurred')
   # ---- creating user home ----
   home = Homes()
   home.pv_modules = request.form['pv_modules']
   home.city_code = request.form['city_code']
   home.amortization_years_pv = request.form['amortization_years_pv']
   home.amortization_years_bat = request.form['amortization_years_bt']
   home.userId = user.id

   db.session.add(home)
   '''
   try:
      db.session.commit()
   except IntegrityError:
      # Error de insercion de home

   currentUser = user
   session['logged_in'] = True
   '''
   return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def do_login():
   global currentUser
   global login_attempts

   if login_attempts >= 3:
      return render_template('login.html', login_error='Your session is blocked for max login attempts')

   input_email = request.form['form-username']
   input_pass = request.form['form-password']
   user = db.session.query(Users).filter_by(email=input_email).first()

   if user is not None:
      if user.check_password(input_pass):
         currentUser = user
         session['logged_in'] = True
         return redirect(url_for('index'))
      else:
         # Password fails
         login_attempts += 1
         return render_template('login.html', login_error='Incorrect password. Please try again')
   else:
      # User fails
      login_attempts += 1
      return render_template('login.html', login_error="User {} does not exists".format(input_email))

@app.route('/simulation', methods=['POST'])
def simulation():
   global currentUser

   if currentUser is not None:
      # Recoger date y consumo
      current_sim = Simulation(current_user.home, const.C, dt.datetime(2019, 3, 11, 0, 0, 0))
      data = current_sim.optimize()
      result = json.loads(data)

      return make_response(jsonify(result), 200)
   else:
      return redirect(url_for('do_login'))

@app.route('/logout')
def do_logout():
   global currentUser

   currentUser = None
   session['logged_in'] = False

   return redirect(url_for('do_login'))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


if __name__=="__main__":
   app.secret_key = os.urandom(10)
   app.run(debug=True, host='0.0.0.0', port=7000)
