#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import time
import requests

TOKEN = '879c5ab5bc0211a1ba23527736e3402a0e708f0a5e7c370f0274004e676ee5f6'
BASE_URL = 'https://api.esios.ree.es'
URL = '{}/indicators/$INDICATOR?start_date=$START_DATE&end_date=$END_DATE'.format(BASE_URL)

INDICATOR_SPOT = '613'  # Precio marginal del mercado intradiario (precio de compra/venta a la red eletrica)
INDICATOR_PVPC = '1013' # Precio Voluntario para el Pequeño Consumidor (precio de venta al cliente)

headers = {
          'Accept' : 'application/json; application/vnd.esios-api-v1+json',
          'Content-Type' : 'application/json',
          'Host' : 'api.esios.ree.es',
          'Authorization' : 'Token token=\"' + TOKEN + '\"'
          }

def pvpc_price (start_date=time.strftime("20%y/%m/%d"),end_date=time.strftime("20%y/%m/%d")):
    global headers

    url = URL.replace('$INDICATOR',INDICATOR_PVPC).replace('$START_DATE',start_date).replace('$END_DATE',end_date)
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

    url = URL.replace('$INDICATOR',INDICATOR_SPOT).replace('$START_DATE',start_date).replace('$END_DATE',end_date)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        price = data['indicator']['values'][1]['value']/1000 # price in Spain(1) in €/kwh
        return price
    else:
        print("An error has occurred")
        return None
    
'''
if "__NAME__==__MAIN__":
    print ("PVPC: {} €/kwh\nSPOT: {} €/kwh".format(pvpc_price(),spot_price()))
'''
