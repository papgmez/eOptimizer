#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import datetime
import requests
import datetime as dt
import random as rd
from config import project_constants as const

headers = {
          'Accept' : 'application/json; application/vnd.esios-api-v1+json',
          'Content-Type' : 'application/json',
          'Host' : 'api.esios.ree.es',
          'Authorization' : 'Token token=\"' + const.ESIOS_TOKEN + '\"'
          }


def get_incoming_prices(indicator, start, end):
    global headers
    url = const.ESIOS_URL.replace('$INDICATOR',indicator).replace('$START_DATE',dt.datetime.strftime(start,'%Y/%m/%d')).replace('$END_DATE',dt.datetime.strftime(end,'%Y/%m/%d'))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price_buffer = create_price_buffer(data,start)
        return price_buffer
    else:
        print("An error has occurred")
        return None

def create_price_buffer(data,start):
    pb = []
    pb_size = 0
    price_per_hours = data['indicator']['values']

    for price in price_per_hours:
        price_date = dt.datetime.strptime(price['datetime'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

        if price['geo_name'] == 'España' and (price_date.date() > start.date() or (price_date.date() == start.date() and price_date.hour >= start.hour)):
            pb.append(round(price['value']/1000,3)) # price in €/kwh
            pb_size += 1

        if pb_size >= 24: break

    # at 20:20 in PVPC case and 17:00 in SPOT case the information of the day D+1 is published. If it is not available yet, then complete the remaining hours of the buffer with a previous random value
    while pb_size < 24:
        pb.append(rd.choice(pb))
        pb_size += 1

    return pb

'''
if "__NAME__==__MAIN__":
    print("Prices between {} and {}".format(const.START,const.END))
    print(get_incoming_prices(const.PVPC))
    print(get_incoming_prices(const.SPOT))
'''
