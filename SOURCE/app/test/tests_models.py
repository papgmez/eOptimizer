
#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from config import test_config
from models import Base, Users, Homes
from factories import factory_models as factory

class test_Models(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config.from_object(test_config)
        self.db = SQLAlchemy(app)
        Base.metadata.create_all(bind=self.db.engine)

    def tearDown(self):
        self.db.session.remove()
        Base.metadata.drop_all(bind=self.db.engine)

    def test_create_user(self):
        user = factory.generate_user()

        self.db.session.add(user)
        self.db.session.commit()
        self.assertEqual(self.db.session.query(Users).count(), 1)

    def test_create_fail_user(self):
        user = factory.generate_user()
        user.email = None

        self.db.session.add(user)
        self.assertRaises(IntegrityError, self.db.session.commit)

    def test_create_home(self):
        user = factory.generate_user()
        self.db.session.add(user)
        self.db.session.commit()
        home = factory.generate_home(user.id)

        self.db.session.add(home)
        self.assertEqual(self.db.session.query(Homes).count(), 1)
        self.assertEqual(self.db.session.query(Homes).get(home.id).user, user)

    def test_create_fail_home(self):
        user = factory.generate_user()
        self.db.session.add(user)
        self.db.session.commit()
        home = factory.generate_home(user.id)
        home.pv_modules = None

        self.db.session.add(home)
        self.assertRaises(IntegrityError, self.db.session.commit)

if __name__ == '__main__':
    unittest.main()
