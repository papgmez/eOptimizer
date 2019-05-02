#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import unittest
import datetime as dt

from app import app, db
from faker import Faker
from models import Base
from config import test_config
from flask_sqlalchemy import SQLAlchemy
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

    def test_login_unknown_user(self):
        fake_email = 'fail@email.com'
        result = self.tester.post('/login', data = {'form-username' : fake_email,
                                                    'form-password' : 'test'})

        self.assertIn('User {} does not exists'.format(fake_email), str(result.data))

    def test_login_incorrect_password(self):
        testing_user = factory.generate_user()
        self._add_user(testing_user)
        result = self.tester.post('/login', data = {'form-username' : testing_user.email,
                                                    'form-password' : 'fail'})

        self.assertIn('Password fails. Try again', str(result.data))

    def test_index_without_logged_in(self):
        result = self.tester.get('/')

        self.assertIn('Enter username and password', str(result.data))
        self.assertEqual(result.status_code, 200)

    def test_index_with_logged_in_and_not_home_added(self):
        testing_user = factory.generate_user()
        self._add_user(testing_user)
        self.tester.post('/login', data = {'form-username' : testing_user.email,
                                                          'form-password' : 'test'})
        result = self.tester.get('/')

        self.assertIn('Enter your home data', str(result.data))
        self.assertEqual(result.status_code, 200)

    def test_index_with_logged_in_and_home_added(self):
        testing_user = factory.generate_user()
        testing_home = factory.generate_home(None)
        self._add_user(testing_user)
        self._add_home(testing_home)
        self.tester.post('/login', data = {'form-username' : testing_user.email,
                                                          'form-password' : 'test'})
        result = self.tester.get('/')

        self.assertIn('Dashboard', str(result.data))
        self.assertEqual(result.status_code, 200)

    def test_simulation_success(self):
        simulation_date = dt.datetime.now().strftime("%Y-%m-%d")
        testing_user = factory.generate_user()
        testing_home = factory.generate_home(None)
        self._add_user(testing_user)
        self._add_home(testing_home)
        self.tester.post('/login', data = {'form-username' : testing_user.email,
                                           'form-password' : 'test'})
        result = self.tester.post('/simulation', data = {'form-start-date' : simulation_date})

        self.assertEqual(result.status_code, 200)

    def test_simulation_without_file(self):
        simulation_date = Faker().date_this_year(before_today=True, after_today=False)
        simulation_date = simulation_date.strftime("%Y-%m-%d")
        testing_user = factory.generate_user()
        testing_home = factory.generate_home(None)
        self._add_user(testing_user)
        self._add_home(testing_home)
        self.tester.post('/login', data = {'form-username' : testing_user.email,
                                           'form-password' : 'test'})
        result = self.tester.post('/simulation', data = {'form-start-date' : simulation_date})

        self.assertIn('You must upload your Endesa consumption', str(result.data))

    def test_simulation_without_date(self):
        testing_user = factory.generate_user()
        testing_home = factory.generate_home(None)
        self._add_user(testing_user)
        self._add_home(testing_home)
        self.tester.post('/login', data = {'form-username' : testing_user.email,
                                           'form-password' : 'test'})
        result = self.tester.post('/simulation', data = {'form-start-date' : ''})

        self.assertIn('You must select a simulation date', str(result.data))


if __name__ == '__main__':
    unittest.main()
