import os

PWD = os.path.abspath(os.curdir)
SECRET_KEY = os.urandom(10)
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db/test_dbase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
