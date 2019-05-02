#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import unittest
import datetime as dt

from app import app, db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import test_config
from models import Base, Users
from factories import factory_models as factory

class test_App(unittest.TestCase):

    def setUp(self):
        app.config.from_object(test_config)
        db = SQLAlchemy(app)
        Base.metadata.create_all(bind=db.engine)
        self.tester = app.test_client(self)

    def tearDown(self):
        app.config.from_object(test_config)
        db = SQLAlchemy(app)
        db.session.remove()
        Base.metadata.drop_all(bind=db.engine)
        del self.tester

    def _add_user(self, testing_user):
        return self.tester.post('/signup', data = {'form-first-name' : testing_user.name,
                                                   'form-last-name' : testing_user.lastname,
                                                   'form-email' : testing_user.email,
                                                   'form-newpassword' : 'test'})
    def _add_home(self, home):
        return self.tester.post('/add-home', data = {'form-pvmodules' : home.pv_modules,
                                                     'form-city_code' : home.city_code,
                                                     'form-amortization_years_pv' : home.amortization_years_pv,
                                                     'form-amortization_years_bt' : home.amortization_years_bat})
    def test_index(self):
        result = self.tester.get('/')

        self.assertEqual(result.status_code, 200)

    def test_sign_up_and_add_home(self):
        testing_user = factory.generate_user()
        signup_result = self._add_user(testing_user)

        home = factory.generate_home(None)
        addhome_result = self._add_home(home)

        self.assertEqual(signup_result.status_code, 200)
        self.assertEqual(addhome_result.status_code, 302)

    def test_login_and_logout(self):
        testing_user = factory.generate_user()
        self._add_user(testing_user)
        login_result = self.tester.post('/login', data = {'form-username' : testing_user.email,
                                                          'form-password' : 'test'})
        logout_result = self.tester.get('/logout')

        self.assertEqual(login_result.status_code, 302)
        self.assertEqual(logout_result.status_code, 200)

    def test_login_fail(self):
        result = self.tester.post('/login', data = {'form-username' : 'fail@email.com',
                                                    'form-password' : 'fail'})

        self.assertNotEqual(result.status_code, 302)

    def test_simulation(self):
        simulation_date = dt.datetime.now().strftime("%Y-%m-%d")
        testing_user = factory.generate_user()
        testing_home = factory.generate_home(None)
        self._add_user(testing_user)
        self._add_home(testing_home)
        self.tester.post('/login', data = {'form-username' : testing_user.email,
                                           'form-password' : 'test'})
        result = self.tester.post('/simulation', data = {'form-start-date' : simulation_date})

        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
