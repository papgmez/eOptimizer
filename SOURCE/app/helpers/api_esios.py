#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import datetime as dt
import requests

from config import project_constants as const

headers = {
    'Accept' : 'application/json; application/vnd.esios-api-v1+json',
    'Content-Type' : 'application/json',
    'Host' : 'api.esios.ree.es',
    'Authorization' : 'Token token=\"' + const.ESIOS_TOKEN + '\"'
}


def get_incoming_prices(indicator, start, end):
    global headers
    url = const.ESIOS_URL.replace('$INDICATOR', indicator).replace('$START_DATE', dt.datetime.strftime(start, '%Y/%m/%d')).replace('$END_DATE', dt.datetime.strftime(end, '%Y/%m/%d'))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price_buffer = create_price_buffer(data, start)
        return price_buffer

    return []

def create_price_buffer(data, start):
    prices_buffer = []
    price_per_hours = data['indicator']['values']

    for price in price_per_hours:
        price_date = dt.datetime.strptime(price['datetime'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

        if price['geo_name'] == 'España' and (price_date.date() > start.date() or (price_date.date() == start.date() and price_date.hour >= start.hour)):
            prices_buffer.append(round(price['value']/1000, 3)) # price in €/kwh

        if len(prices_buffer) >= 24: break

    while len(prices_buffer) < 24:
        prices_buffer.append(prices_buffer[-1])

    return prices_buffer
