#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import datetime as dt
import json

from scipy.optimize import linprog

from helpers import api_esios as esios
from helpers import api_aemet as aemet
from config import project_constants as const


class Simulation:
    def __init__(self, home, user, c, date):
        # ---- time bounds of the simulation ----
        self.start = date
        self.end = self.start + dt.timedelta(1)
        # ---- attr ----
        self.home = home
        self.user = user
        self.discharge_depth = const.DISCH_DEPTH
        self.battery_capacity = const.BAT_CAPACITY
        self.battery_level = self.battery_capacity * 0.5
        self.max_ef_buffer = self.calculate_max_ef_buffer(date)
        # ---- prices ----
        self.ef_price = self.calculate_ef_price()
        self.er_price = esios.get_incoming_prices(const.PVPC, self.start, self.end)
        self.eb_price = self.calculate_eb_price()
        self.cr_price = esios.get_incoming_prices(const.SPOT, self.start, self.end)
        self.cb_price = self.calculate_cb_prices()
        # ---- home consumptions ----
        self.c_int = const.C_INT
        self.c = c
        self.comparable_result = self.calculate_comparable_result()
        # ---- simulation arguments ----
        self.f = self.generate_function_coeficients() # coeficients of the function to minimize
        self.A_eq, self.b_eq, self.A_ub, self.b_ub = [], [], [], [] # restrictions arrays

    def calculate_max_ef_buffer(self, date):
        today = dt.datetime.now()
        max_values = []

        if date.date() == today.date():
            wb = aemet.get_weather_today(self.home.city_code)
        else:
            wb = aemet.get_weather_archive(date.strftime("%Y-%m-%d"), self.home.city_code)

        for state in wb:
            max_values.append(self.home.pv_modules * const.FUZZY_SETS.get(state)/1000)

        return max_values

    def calculate_ef_price(self):
        yearly_cost = self.home.pv_modules * const.MODULE_PRICE / self.home.amortization_years_pv
        yearly_prod = const.YEAR_PV_ESTIM * self.home.pv_modules

        return yearly_cost / yearly_prod

    def calculate_eb_price(self):
        yearly_cost = const.BAT_PRICE / self.home.amortization_years_bat
        yearly_prod = self.battery_capacity * 182.5

        return yearly_cost / yearly_prod

    def calculate_cb_prices(self):
        prices = []

        for i in range(0, 24):
            # is the minimum price between ef and er (value saved by storing energy)
            if self.ef_price <= self.er_price[i]:
                prices.append(self.ef_price)
            else:
                prices.append(self.er_price[i])

        return prices

    def calculate_comparable_result(self):
        price = 0

        for i in range(0, 24):
            price += self.er_price[i] * self.c[i]

        return price

    def generate_function_coeficients(self):
        f = []

        for i in range(0, 24):
            f.append(self.ef_price)     # cost of producing 1kw of photovoltaic energy in t hour
            f.append(self.er_price[i])  # cost of buying 1kw of network energy in t hour
            f.append(self.eb_price)     # cost of obtaining 1kw from batteries in t hour
            f.append(-self.cr_price[i]) # cost of selling 1kw to the network energy in t hour
            f.append(-self.cb_price[i]) # cost of store 1kw in the battery in t hour

        return f

    def generate_restriction_1(self):
        # 1. EFi+ERi+EBi=CRi+CBi+Cinst+Cprop_i (i=0..23)
        # restr_coef will have 120 values (5 variables * 24 hours)
        # i*5 is the t hour of the model, and adds 1,2,3,4 or 5 to point to the variables of f(x)
        # (i*5+0 is EFi, i*5+1 is ERi, etc)
        # i*5 because there are 5 variables for each iteration
        for i in range(0, 24):
            restr_coef = [0]*5*24
            restr_coef[i*5] = 1
            restr_coef[i*5+1] = 1
            restr_coef[i*5+2] = 1
            restr_coef[i*5+3] = -1
            restr_coef[i*5+4] = -1
            self.A_eq.append(restr_coef)
            self.b_eq.append(self.c_int + self.c[i])

    def generate_restriction_2(self):
        # 2. EF_night(21:30-7:00) = 0
        for i in range(0, 24):
            restr_coef = [0]*5*24
            time = (self.start+dt.timedelta(hours=i)).time()
            if time >= dt.time(21, 30) or time <= dt.time(7, 00):
                restr_coef[i*5] = 1
            self.A_eq.append(restr_coef)
            self.b_eq.append(0)

    def generate_restriction_3(self):
        # 3. EFi <= EFmax_i
        for i in range(0, 24):
            restr_coef = [0]*5*24
            restr_coef[i*5] = 1
            self.A_ub.append(restr_coef)
        self.b_ub.extend(self.max_ef_buffer)

    def generate_restriction_4(self):
        # 4. EB0 <= initial_level - capacity*depth
        restr_coef = [0]*5*24
        restr_coef[2] = 1
        self.A_ub.append(restr_coef)
        self.b_ub.append(self.battery_level-self.battery_capacity*self.discharge_depth)

    def generate_restriction_5(self):
        # 5. CB0 - EB0 <= capacity - initial_level
        restr_coef = [0]*5*24
        restr_coef[0] = -1
        restr_coef[4] = 1
        self.A_ub.append(restr_coef)
        self.b_ub.append(self.battery_capacity-self.battery_level)

    def generate_restriction_6(self):
        # 6. EBi <= initial_level + Σ(0,i-1){-EBt + CBt} - capacity*depth
        for i in range(1, 24):
            restr_coef = [0]*5*24
            restr_coef[i*5+2] = 1
            for j in range(0, i-1):
                restr_coef[j*5+2] = 1
                restr_coef[j*5+4] = -1
            self.A_ub.append(restr_coef)
            self.b_ub.append(self.battery_level-self.battery_capacity*self.discharge_depth)

    def generate_restriction_7(self):
        # 7. CBi <= capacity - (initial_level + Σ(0,i-1){-EBt + CBt}) + EBi
        for i in range(1, 24):
            restr_coef = [0]*5*24
            restr_coef[i*5+4] = 1
            restr_coef[i*5+2] = -1
            for j in range(0, i-1):
                restr_coef[j*5+2] = -1
                restr_coef[j*5+4] = 1
            self.A_ub.append(restr_coef)
            self.b_ub.append(self.battery_capacity - self.battery_level)

    def optimize(self):
        # Function to minimize:
        # f(x) = Σ(0..24) EFi*PF + ERi*PVPCi + EB*PB - CRi*PRi - CB*PBin_i
        # Daily expenditure on the production of energy for self-consumption

        self.generate_restriction_1()
        self.generate_restriction_2()
        self.generate_restriction_3()
        self.generate_restriction_4()
        self.generate_restriction_5()
        self.generate_restriction_6()
        self.generate_restriction_7()

        res = linprog(self.f, self.A_ub, self.b_ub, self.A_eq, self.b_eq, bounds=(0, None))

        self.store_result(res)

        return self.prepare_result(res)

    def prepare_result(self, res):
        values = res.x.tolist()
        data = {
            "date" : self.start.strftime("%d-%m-%Y"),
            "start" : self.start.strftime("%H:%M:%S"),
            "end" : self.end.strftime("%H:%M:%S"),
            "created_at" : dt.datetime.now().strftime("%Y-%m-%d_%H:%M"),
            "result" : round(res.fun, 3),
            "comparable_result" : round(self.comparable_result, 3),
            "hours" : self.prepare_hours(values)
        }

        return json.dumps(data)

    def prepare_hours(self, values):
        hours = []

        for i in range(0, len(values)):
            # Parse results to Watios in case of json result
            values[i] *= 1000

        for i in range(0, 24):
            total_generated = values[i*5] + values[i*5+1] + values[i*5+2]
            total_consumed = self.c[i]*1000 + values[i*5+3] + values[i*5+4] + self.c_int*1000

            hours.append({"EF" : round(values[i*5], 3),
                          "EF_rate" : self.get_energy_rate(values[i*5], total_generated),
                          "EF_price" : round(self.ef_price, 3),
                          "ER" : round(values[i*5+1], 3),
                          "ER_rate" : self.get_energy_rate(values[i*5+1], total_generated),
                          "ER_price" : self.er_price[i],
                          "EB" : round(values[i*5+2], 3),
                          "EB_rate" : self.get_energy_rate(values[i*5+2], total_generated),
                          "EB_price" : round(self.eb_price, 3),
                          "C" : round(self.c[i] * 1000, 3),
                          "C_rate" : self.get_energy_rate(self.c[i]*1000, total_consumed),
                          "CR" : round(values[i*5+3], 3),
                          "CR_rate" : self.get_energy_rate(values[i*5+3], total_consumed),
                          "CR_price" : self.cr_price[i],
                          "CB" : round(values[i*5+4], 3),
                          "CB_rate" : self.get_energy_rate(values[i*5+4], total_consumed),
                          "CB_price" : round(self.cb_price[i], 3),
                          "C_int" : self.c_int * 1000,
                          "Cint_rate" : self.get_energy_rate(self.c_int*1000, total_consumed)
                         })

        return hours

    def get_energy_rate(self, amount, total_amount):
        return amount * 100 / total_amount

    def store_result(self, res):
        values = res.x.tolist()
        created_at = dt.datetime.now().strftime("%Y-%m-%d_%H:%M")
        out = open("simulations/simulation_{}.txt".format(created_at), "w")

        out.write("-----------------------------------------------------\n")
        out.write("--------------- Reporte de Simulacion ---------------\n")
        out.write("-----------------------------------------------------\n")
        out.write("Usuario: {}\n".format(self.user.email))
        out.write("Nombre: {} {}\n".format(self.user.name, self.user.lastname))
        out.write("Numero de modulos fotovoltaicos: {}\n".format(self.home.pv_modules))
        out.write("Capacidad de la bateria: {} KW\n".format(self.battery_capacity))
        out.write("-----------------------------------------------------\n")
        out.write("Inicio:\t{}\nFin:\t{}\n".format(self.start, self.end))
        out.write("Gasto con el sistema e-Optimizer: {} €\n\n".format(res.fun))
        out.write("Gasto con energía de red únicamente: {} €\n\n".format(self.comparable_result))

        for i in range(0, 24):
            current_hour = (self.start+dt.timedelta(hours=i)).strftime("%H:%M")
            next_hour = (self.start+dt.timedelta(hours=i+1)).strftime("%H:%M")
            out.write("Valores optimos entre las {} y las {}\n".format(current_hour, next_hour))
            out.write("\t· Energía Fotovoltaica = {} Kwh\n".format(values[i*5]))
            out.write("\t· Energía de Red = {} Kwh\n".format(values[i*5+1]))
            out.write("\t· Energía de Bateria = {} Kwh\n".format(values[i*5+2]))
            out.write("\t· Venta a la Red = {} Kwh\n".format(values[i*5+3]))
            out.write("\t· Consumo de Bateria = {} Kwh\n".format(values[i*5+4]))
            out.write("\t· Consumo del Hogar = {} Kwh\n".format(self.c[i]))
            out.write("\t· Consumo del Sistema = {} Kwh\n".format(self.c_int))
            out.write("\n----------------------------------------------\n")
