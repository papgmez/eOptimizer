#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import time
import requests
import random as rd

from config import project_constants as const

def get_weather_today(city):
    weather_buffer = []
    url = const.AEMET_URL_NOW.replace('$CITY', city)
    response = requests.get(url)
    data = response.json()

    if data['estado'] == 200:
        url = data['datos']
        response = requests.get(url)
        data = response.json()[0]
        weather_buffer = create_weather_buffer(data)
        return weather_buffer
    else:
        return None

def get_weather_archive(date, city):
    weather_buffer = []
    province = city[:2]
    url = const.AEMET_URL_DATE.replace('$PROVINCE', province).replace('$DATE', date)

    response = requests.get(url)
    data = response.json()

    if data['estado'] == 200:
        url = data['datos']
        response = requests.get(url)
        raw_info = response.text
        weather_buffer = proccess_weather_archive(raw_info)
        return weather_buffer
    else:
        return None

def create_weather_buffer(data):
    wb = []
    buffer_size = 0
    current_hour = time.strftime("%H")
    prediction_today = data['prediccion']['dia'][0]['estadoCielo']
    prediction_tomorrow = data['prediccion']['dia'][1]['estadoCielo']

    # adds the remaining predictions per hour of the day to the buffer
    for hour in prediction_today:
        if int(hour['periodo']) >= int(current_hour):
            wb.append(hour['descripcion'])
            buffer_size += 1
    # adds tomorrow's predictions per hour until complete the 24 h of the buffer
    for hour in prediction_tomorrow:
        if buffer_size < 24:
            wb.append(hour['descripcion'])
            buffer_size += 1
    return wb

def proccess_weather_archive(raw_info):
    possible_states = const.FUZZY_SETS.keys()
    occurred_states = []
    wb_size = 0

    for state in possible_states:
        if raw_info.find(state) != -1:
            occurred_states.append(state)
            wb_size += 1

        if wb_size >= 24: break

    # To fill the remaining slots in the buffer, randomly concatenates states of those occurred
    while wb_size < 24:
        occurred_states.append(rd.choice(occurred_states))
        wb_size += 1

    return occurred_states
