#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from werkzeug.utils import secure_filename
from config import prod_config

import datetime as dt
import random as rd
import os

def read_from_file(filename):
    filepath = "{}/{}".format(prod_config.CONSUMPTIONS_FOLDER, filename)
    consumption_file = open(filepath, "r")

    # redundant data
    for i in range(0, 6):
        consumption_file.readline()

    # necessary data
    values = []
    for i in range(0, 24):
        hour = consumption_file.readline().split("\t\t\t\t")
        # the value in file is in Wh
        try:
            values.append(float(hour[2])/1000)
        except ValueError:
            return None
        consumption_file.close()
    return values

def store_upload_file(upload_file, userid):
    created_at = dt.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    filename = secure_filename('{}-consumption-{}'.format(userid, created_at))

    upload_file.save(os.path.join(prod_config.CONSUMPTIONS_FOLDER, filename))

    return filename

def get_random_values():
    values = []
    for i in range(0, 24):
        values.append(rd.random())
    return values
