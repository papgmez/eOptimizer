#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import time
import requests
import project_constants

headers = {
          'Accept' : 'application/json; application/vnd.esios-api-v1+json',
          'Content-Type' : 'application/json',
          'Host' : 'api.esios.ree.es',
          'Authorization' : 'Token token=\"' + project_constants.ESIOS_TOKEN + '\"'
          }

def pvpc_price (start_date=time.strftime("20%y/%m/%d"),end_date=time.strftime("20%y/%m/%d")):
    global headers

    url = project_constants.ESIOS_URL.replace('$INDICATOR',project_constants.PVPC).replace('$START_DATE',start_date).replace('$END_DATE',end_date)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data['indicator']['values'][0]['value']/1000 # price in €/kwh
        return price
    else:
        print("An error has occurred")
        return None

def spot_price (start_date=time.strftime("20%y/%m/%d"),end_date=time.strftime("20%y/%m/%d")):
    global headers

    url = project_constants.ESIOS_URL.replace('$INDICATOR',project_constants.SPOT).replace('$START_DATE',start_date).replace('$END_DATE',end_date)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data['indicator']['values'][1]['value']/1000 # price in Spain(1) in €/kwh
        return price
    else:
        print("An error has occurred")
        return None


if "__NAME__==__MAIN__":
    print ("PVPC: {} €/kwh\nSPOT: {} €/kwh".format(pvpc_price(),spot_price()))
