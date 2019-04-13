#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import random as rd

def read_from_file(path):
    file = open("home_data/{}".format(path), "r")
    # redundant data
    for i in range(0, 6):
        file.readline()
    # necessary data
    values = []
    for i in range(0, 24):
        hour = file.readline().split("\t\t\t\t")
        # the value in file is in Wh
        values.append(float(hour[2])/1000)
    file.close()
    return values

def get_random_values():
    values = []
    for i in range(0, 24):
        values.append(rd.random())
    return values
