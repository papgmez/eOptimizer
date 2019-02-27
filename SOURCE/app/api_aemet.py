#!/usr/bin/python3

import requests
import time

URL = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/$CITY-CODE/?api_key=$API-KEY'
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYWJsby5wYWxvbWlubzFAb3V0bG9vay5jb20iLCJqdGkiOiJmOGFhZTdiNi0yYWIzLTQzOTktYjU3Mi0zNDBlYWE2OGUwMDUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU0ODU4NTE1NywidXNlcklkIjoiZjhhYWU3YjYtMmFiMy00Mzk5LWI1NzItMzQwZWFhNjhlMDA1Iiwicm9sZSI6IiJ9.4VGEUO4v-ncytcyWuaNwHBBvhhIAW5r-5Es0VAFiLr8'
CR_CODE = '13034'

def aemet_cr_weather ():
    weather_buffer = []
    url = URL.replace('$CITY-CODE',CR_CODE).replace('$API-KEY',API_KEY)
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
    print(aemet_cr_weather())
'''
