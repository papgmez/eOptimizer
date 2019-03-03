#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from flask import Flask, make_response, abort, jsonify, request, redirect, flash, url_for, render_template

import api_aemet as aemet
import api_esios as esios
import project_constants as const

app = Flask(__name__)
app.secret_key = "development"


@app.route('/')
def index():
   return "Welcome"

@app.route('/weather')
def get_weather_buffer():
    weather = aemet.get_weather()

    if weather is None:
       abort(404)

    values = []
    for state in weather:
       # centroids of each weather state fuzzy set
       values.append(const.FUZZY_SETS.get(state))

    return make_response(jsonify({'weather_states':weather, 'weather_values':values}),200)

@app.route('/price/<type>')
def get_current_price(type):
    price = None

    if type == 'PVPC':
       price = esios.get_price(const.PVPC)
    elif type == 'SPOT':
        price = esios.get_price(const.SPOT)

    if price is not None:
        return make_response(jsonify({'type':type, 'unit':'€/Kwh', 'price_buffer':price}),200)
    abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=7000)
