import os

SECRET_KEY = os.urandom(10)
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'db2://dwm91559:zswksj730cmk90%5Eq@dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net:50000/BLUDB'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CONSUMPTIONS_FOLDER = 'consumptions'
SIMULATIONS_FOLDER = 'simulations'
