from config import project_constants as const
import os

SECRET_KEY = os.urandom(10)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'db2://{}:{}@{}:{}/{}'.format(const.IBM_USER,
                                                      const.IBM_KEY,
                                                      const.IBM_HOSTNAME,
                                                      const.IBM_PORT,
                                                      const.IBM_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False
CONSUMPTIONS_FOLDER = 'consumptions'
SIMULATIONS_FOLDER = 'simulations'
