import os

PWD = os.path.abspath(os.curdir)
SECRET_KEY = os.urandom(10)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db/dbase.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
CONSUMPTIONS_FOLDER = 'consumptions'
SIMULATIONS_FOLDER = 'simulations'
