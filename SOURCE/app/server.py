#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

from flask import Flask, make_response, abort, jsonify, request, redirect, flash, url_for, render_template

from api_aemet import aemet_cr_weather
from api_esios import spot_price, pvpc_price

app = Flask(__name__)
app.secret_key = "development"


@app.route('/')
def index():
   return "Welcome"

@app.route('/weather')
def get_weather_buffer():
    w_buffer = aemet_cr_weather()

    if w_buffer is not None:
        return make_response(jsonify({'buffer':w_buffer}),200)
    abort(404)

@app.route('/price/<type>')
def get_current_price(type):    
    price = None

    if type == 'PVPC':
       price = pvpc_price()
    elif type == 'SPOT':
        price = spot_price()
        
    if price is not None:
        return make_response(jsonify({'type':type, 'unit':'Kwh', 'price':price}),200)
    abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)



if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0',port=7000)    
