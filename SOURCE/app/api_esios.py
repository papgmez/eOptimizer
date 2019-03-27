#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-
''' e-sios API module
Note: The functionality of this module is to provide a buffer with the next 24 PVPC or SPOT price values, as indicated
'''
import datetime as dt
import random as rd
import requests
import project_constants as const

HEADERS = {
    'Accept' : 'application/json; application/vnd.esios-api-v1+json',
    'Content-Type' : 'application/json',
    'Host' : 'api.esios.ree.es',
    'Authorization' : 'Token token=\"' + const.ESIOS_TOKEN + '\"'
}


def get_incoming_prices(indicator):
    start = const.START
    end = const.END

    url = const.ESIOS_URL.replace('$INDICATOR', indicator)
    url = url.replace('$START_DATE', dt.datetime.strftime(start, '%Y/%m/%d'))
    url = url.replace('$END_DATE', dt.datetime.strftime(end, '%Y/%m/%d'))

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        price_buffer = create_price_buffer(data, start)
        return price_buffer
    return None

def create_price_buffer(data, start):
    price_buffer = []
    pb_size = 0
    price_per_hours = data['indicator']['values']

    for price in price_per_hours:
        price_date = dt.datetime.strptime(price['datetime'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

        if price['geo_name'] == 'España' and (price_date.date() > start.date() or (price_date.date() == start.date() and price_date.hour >= start.hour)):
            price_buffer.append(round(price['value']/1000, 3)) # price in €/kwh
            pb_size += 1

        if pb_size >= 24: break

    while pb_size < 24:
        price_buffer.append(rd.choice(price_buffer))
        pb_size += 1

    return price_buffer
