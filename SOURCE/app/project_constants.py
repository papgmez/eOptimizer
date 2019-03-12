#!/usr/bin/python3

import random

# Fichero de Constantes del Proyecto
# ----------------------------------
# Numero de modulos fotovoltaicos del Sistema.
PV_MODULES = 125
# Kw de consumo propio del Sistema. Valor que consume el sistema en una hora t y debe ser satisfecho siempre (aleatorio entre 10 y 12 Kwh)
C = random.uniform(10,12)

# --------- API Aemet OpenData ---------
# Codigo de la API OpenData de AEMET
CITY_CODE = '13034' # Ciudad Real

# Api key para el manejo de OpenData AEMET
AEMET_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYWJsby5wYWxvbWlubzFAb3V0bG9vay5jb20iLCJqdGkiOiJmOGFhZTdiNi0yYWIzLTQzOTktYjU3Mi0zNDBlYWE2OGUwMDUiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTU0ODU4NTE1NywidXNlcklkIjoiZjhhYWU3YjYtMmFiMy00Mzk5LWI1NzItMzQwZWFhNjhlMDA1Iiwicm9sZSI6IiJ9.4VGEUO4v-ncytcyWuaNwHBBvhhIAW5r-5Es0VAFiLr8'

# url api AEMET OpenData
AEMET_URL = 'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/{}/?api_key={}'.format(CITY_CODE, AEMET_KEY)

# --------- API Esios REE ---------
# Token para la API de Esios (Red Electrica de España)
ESIOS_TOKEN = '879c5ab5bc0211a1ba23527736e3402a0e708f0a5e7c370f0274004e676ee5f6'

# url api Esios REE
ESIOS_URL = 'https://api.esios.ree.es/indicators/$INDICATOR?start_date=$START_DATE&end_date=$END_DATE'

# Indicadores de precios Esios REE
PVPC = '1013' # Precio Voluntario para el Pequeño Consumidor (precio de venta al cliente)
SPOT = '613'  # Precio marginal del intradiario (precio de compra/venta a la red eletrica)

# # Maxima Potencia Nominal posible (MNP) en W de un modulo fotovoltaico de Potencia Pico 50 W, de cada conjunto difuso del estado de Cielo
FUZZY_SETS = {
    'Despejado' : 48,
    'Poco nuboso' :43.16,
    'Nubes altas' : 38.16,
    'Intervalos nubosos' : 33.16,
    'Intervalos nubosos con lluvia escasa' : 28.16,
    'Intervalos nubosos con lluvia' : 23.16,
    'Nuboso' : 18.16,
    'Nuboso con lluvia escasa' : 13.16,
    'Cubierto' : 8.16,
    'Cubierto con lluvia escasa' : 2.66,
    'Nuboso noche' : 0,
    'Muy nuboso' : 0,
    'Nubes altas noche' : 0,
    'Intervalos nubosos con lluvia escasa noche' : 0,
    'Nuboso con lluvia escasa noche' : 0,
    'Muy nuboso con lluvia escasa' : 0,
    'Despejado noche' : 0,
    'Intervalos nubosos noche' : 0,
    'Poco nuboso noche' : 0,
    'Intervalos nubosos con lluvia noche' : 0,
    'Nuboso con lluvia' : 0,
    'Nuboso con lluvia noche' : 0,
    'Muy nuboso con lluvia' : 0,
    'Cubierto con lluvia' : 0,
    'Intervalos nubosos con nieve escasa' : 0,
    'Intervalos nubosos con nieve escasa noche' : 0,
    'Nuboso con nieve escasa' : 0,
    'Nuboso con nieve escasa noche' : 0,
    'Muy nuboso con nieve escasa' : 0,
    'Cubierto con nieve escasa' : 0,
    'Intervalos nubosos con nieve' : 0,
    'Intervalos nubosos con nieve noche' : 0,
    'Nuboso con nieve' : 0,
    'Nuboso con nieve noche' : 0,
    'Muy nuboso con nieve' : 0,
    'Cubierto con nieve' : 0,
    'Intervalos nubosos con tormenta' : 0,
    'Intervalos nubosos con tormenta noche' : 0,
    'Nuboso con tormenta' : 0,
    'Nuboso con tormenta noche' : 0,
    'Muy nuboso con tormenta' : 0,
    'Cubierto con tormenta' : 0,
    'Intervalos nubosos con tormenta y lluvia escasa' : 0,
    'Intervalos nubosos con tormenta y lluvia escasa noche' : 0,
    'Nuboso con tormenta y lluvia escasa' : 0,
    'Nuboso con tormenta y lluvia escasa noche' : 0,
    'Muy nuboso con tormenta y lluvia escasa' : 0,
    'Cubierto con tormenta y lluvia escasa' : 0
}
