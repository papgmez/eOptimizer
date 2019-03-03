#!/usr/bin/python3

import requests
import time

import project_constants as const

def aemet_weather ():
    weather_buffer = []
    url = const.AEMET_URL.replace('$CITY-CODE',const.CITY_CODE).replace('$API-KEY',const.AEMET_KEY)
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

'''
if "__NAME__==__MAIN__":
    print("Weather buffer of the next 24 h:")
    print(aemet_weather())
'''
