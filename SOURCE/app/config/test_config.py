import os

PWD = os.path.abspath(os.curdir)

TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db/test_dbase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
