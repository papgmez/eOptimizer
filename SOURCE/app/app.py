#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import datetime as dt
import json
import os

from flask import Flask, request, render_template, session, send_from_directory
from flask import make_response, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from models import Base, Users, Homes
from config import prod_config
from simulation import Simulation
from helpers import client_consumption as c_utils

app = Flask(__name__)
db = SQLAlchemy()

currentUser = None
currentHome = None
login_attempts = 0
today = dt.datetime.now()

@app.route('/')
def index():
    global currentUser
    global currentHome
    global today

    if currentUser is None or not session.get('logged_in'):
        return render_template('login.html', flag='login')
    elif currentHome is None:
        return render_template('new_home.html')
    else:
        return render_template('dashboard.html', user=currentUser, home=currentHome,
                               max_date=today.strftime("%Y-%m-%d"))

@app.route('/signup', methods=['POST'])
def sign_up():
    global currentUser
    # ---- creating user ----
    errors = []

    user = Users()
    user.name = request.form['form-first-name']
    user.lastname = request.form['form-last-name']
    user.email = request.form['form-email']
    user.set_password(request.form['form-newpassword'])

    if not user.name:
        errors.append('You must introduce your name')

    if not user.lastname:
        errors.append('You must introduce your lastname')

    if not user.email:
        errors.append('You must introduce an email')

    if not errors:
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            # User Error
            return render_template('login.html', flag='signup', error='An error has occurred')
    else:
        return render_template('login.html', flag='signup', errors=errors)

    currentUser = user
    session['logged_in'] = True

    return render_template('new_home.html', user=user.email)

@app.route('/add-home', methods=['POST'])
def add_home():
    global currentUser
    global currentHome

    if currentUser is not None:
        # ---- creating user home ----
        home = Homes()
        home.pv_modules = request.form['form-pvmodules']
        home.city_code = str(request.form['form-city_code'])
        home.amortization_years_pv = request.form['form-amortization_years_pv']
        home.amortization_years_bat = request.form['form-amortization_years_bt']
        home.user = currentUser

        db.session.add(home)
        try:
            db.session.commit()
        except IntegrityError:
            # Error de insercion de home
            return render_template('new_home.html', error='Ha ocurrido un error')
        currentUser = home.user
        currentHome = home

        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def do_login():
    global currentUser
    global currentHome
    global login_attempts

    if login_attempts >= 3:
        return render_template('login.html', flag='login', error='Max login attempts reached!')

    input_email = request.form['form-username']
    input_pass = request.form['form-password']
    user = db.session.query(Users).filter_by(email=input_email).first()

    if user is not None:
        if user.check_password(input_pass):
            currentUser = user
            currentHome = user.home
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            # Password fails
            login_attempts += 1
            return render_template('login.html', flag='login', error='Password fails. Try again')
    else:
        # User fails
        return render_template('login.html', flag='login',
                               error="User {} does not exists".format(input_email))

@app.route('/simulation', methods=['POST'])
def simulation():
    global currentUser
    global currentHome
    global today

    if currentUser is not None and currentHome is not None:
        errors = []
        simulation_date = request.form['form-start-date']

        if not simulation_date:
            errors.append('You must select a simulation date')
        else:
            start_date = dt.datetime.strptime(simulation_date, '%Y-%m-%d')
            if start_date.date() == today.date():
                consumption = c_utils.get_random_values()
            else:
                upload_file = request.files['consumption-file']
                consumption_file = c_utils.store_upload_file(upload_file, currentUser.id)
                consumption = c_utils.read_from_file(consumption_file)

        if 'consumption-file' not in request.files and start_date.date() != today.date():
            errors.append('You must upload your Endesa consumption')
        elif consumption == None:
            errors.append('Your consumption file is invalid')

        if not errors:
            current_sim = Simulation(currentHome, currentUser, consumption, start_date)
            data = current_sim.optimize()

            result = json.loads(data)

            return render_template('simulation.html', simulation=result, user=currentUser)
        else:
            return render_template('dashboard.html', user=currentUser, home=currentHome,
                                   errors=errors, max_date=today.strftime("%Y-%m-%d"))
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def do_logout():
    global currentUser
    global currentHome
    global login_attempts

    currentUser = None
    currentHome = None
    login_attempts = 0
    session['logged_in'] = False

    return render_template('login.html', flag='login')

@app.route('/new_user')
def change_form():
    return render_template('login.html', flag='signup')

@app.route('/simulations/<path:filename>')
def download_file(filename):
    return send_from_directory(prod_config.SIMULATIONS_FOLDER, filename, as_attachment=True)

@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html', error=error)
