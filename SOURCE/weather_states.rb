# -*- coding: utf-8 -*-

# Code to scrap and write all weather states available in AEMET OpenData from the official website

require 'rubygems'
require 'nokogiri'
require 'open-uri'

url = "http://www.aemet.es/es/eltiempo/prediccion/municipios/ayuda"

result = Nokogiri::HTML(open(url))

table = result.at_css("#contenedor > div > div.contenedor_contenido > div.contenedor_central > div:nth-child(2)").text.split("\n")
table.map!{|element| element.gsub("  ","")}
table = table - ["Estado del cielo",""]

f = File.open("weather_states.txt","w")
table.map{|state| f.write(state + "\n")}
f.close
