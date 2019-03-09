#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import datetime
import requests
import project_constants as const
import datetime as dt
import random as rd

headers = {
          'Accept' : 'application/json; application/vnd.esios-api-v1+json',
          'Content-Type' : 'application/json',
          'Host' : 'api.esios.ree.es',
          'Authorization' : 'Token token=\"' + const.ESIOS_TOKEN + '\"'
          }


def get_price (indicator):
    global headers
    today = dt.datetime.today()
    tomorrow = today+dt.timedelta(1)
    url = const.ESIOS_URL.replace('$INDICATOR',indicator).replace('$START_DATE',dt.datetime.strftime(today,'%Y/%m/%d')).replace('$END_DATE',dt.datetime.strftime(tomorrow,'%Y/%m/%d'))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price_buffer = create_price_buffer(data,today)
        return price_buffer
    else:
        print("An error has occurred")
        return None

def create_price_buffer(data,today):
    pb = []
    pb_size = 0
    price_per_hours = data['indicator']['values']

    for price in price_per_hours:
        price_date = dt.datetime.strptime(price['datetime'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

        if price['geo_name'] == 'España' and (price_date.date() > today.date() or (price_date.date() == today.date() and price_date.hour >= today.hour)):
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
    print ("PVPC of the next 24 h:")
    print(get_price(const.PVPC))
    print("SPOT price of the next 24 h:")
    print(get_price(const.SPOT))
'''
