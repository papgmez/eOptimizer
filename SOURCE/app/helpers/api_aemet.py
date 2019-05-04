#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import time
import requests

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

    return []

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

    return []

def create_weather_buffer(data):
    states_buffer = []
    current_hour = time.strftime("%H")
    prediction_today = data['prediccion']['dia'][0]['estadoCielo']
    prediction_tomorrow = data['prediccion']['dia'][1]['estadoCielo']

    # adds the remaining predictions per hour of the day to the buffer
    for hour in prediction_today:
        if int(hour['periodo']) >= int(current_hour):
            states_buffer.append(hour['descripcion'])
    # adds tomorrow's predictions per hour until complete the 24 h of the buffer
    for hour in prediction_tomorrow:
        if len(states_buffer) < 24:
            states_buffer.append(hour['descripcion'])

    return states_buffer

def proccess_weather_archive(raw_text):
    states_buffer = []
    occurrences = []
    raw_text = raw_text.lower()
    possible_states = const.FUZZY_SETS.keys()

    for state in possible_states:
        if raw_text.find(state.lower()) != -1:
            occurrences.append(state.capitalize())

        if len(occurrences) >= 24: break

    interval = 24 // len(occurrences)

    for state in occurrences:
        for _ in range(0, interval):
            states_buffer.append(state)

    # To fill the remaining slots in the buffer, concatenates last state of those occurred
    while len(states_buffer) < 24:
        states_buffer.append(occurrences[-1])

    return states_buffer
