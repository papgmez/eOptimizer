#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

# from pdb import set_trace as breakpoint

from scipy.optimize import linprog
import numpy as np
import datetime as dt
import api_esios as esios
import api_aemet as aemet
import project_constants as pc

class Model:
    def __init__(self,pvm=pc.PV_MODULES,module_price=pc.MODULE_PRICE,yearly_pw_ph=pc.YEARLY_POWER_PH_ESTIMATE,years_ph=pc.YEARS_TO_AMORTIZE_PH,
                 total_batt_price=pc.BATTERY_PRICE,disch_depth=pc.DISCHARGE_DEPTH,batt_size=pc.BATTERY_CAPACITY,batt_level=pc.BATTERY_LEVEL,
                 years_bat=pc.YEARS_TO_AMORTIZE_BATT,c_int=pc.C_INT,c=pc.C,start=pc.START,end=pc.END):
        self.ef_price = self.calculate_ef_price(pvm, module_price, years_ph, yearly_pw_ph)
        self.discharge_depth = disch_depth
        self.battery_capacity = batt_size
        self.battery_level = self.battery_capacity * batt_level
        self.eb_price = self.calculate_eb_price(total_batt_price, years_bat)
        self.c_int = c_int
        # ---- buffers of data ----
        self.max_ef_buffer = self.calculate_max_ef_buffer(pvm) # buffer with incoming 24 max possible values of PV energy
        self.cr_price = esios.get_incoming_prices(pc.SPOT) # buffer with incoming 24 prices for sell energy
        self.er_price = esios.get_incoming_prices(pc.PVPC) # buffer with incoming 24 prices for buy energy
        self.cb_price = self.calculate_cb_prices() # buffer with incoming 24 prices for store energy in battery
        self.c = c # buffer with incoming 24 values of energy consumption in home
        # ---- time bounds of the simulation ----
        self.start = start
        self.end = end
        # ---- simulation arguments ----
        self.f = self.generate_function_coeficients() # coeficients of the function to minimize
        self.A_eq, self.b_eq, self.A_ub, self.b_ub = [], [], [], [] # restrictions arrays

    def calculate_max_ef_buffer(self, num_modules):
        wb = aemet.get_weather()
        max_values = []
        for state in wb:
            max_values.append(num_modules * pc.FUZZY_SETS.get(state)/1000)
        return max_values

    def calculate_ef_price(self, pvm, module_price, years_ph, yearly_pw_ph):
        return (pvm * module_price / years_ph) / (yearly_pw_ph * pvm)

    def calculate_eb_price(self, total_batt_price, years_bat):
        return (total_batt_price / years_bat) / (self.battery_capacity * 182.5)

    def calculate_cb_prices(self):
        prices = []
        for i in range(0,24):
            # is the minimum price between ef and er (value saved by storing energy)
            prices.append(self.ef_price if (self.ef_price <= self.er_price[i]) else self.er_price[i])
        return prices

    def generate_function_coeficients(self):
        f = []
        for i in range(0,24):
            f.append(self.ef_price)     # cost of producing 1kw of photovoltaic energy in t hour (amortization)
            f.append(self.er_price[i])  # cost of buying 1kw of network energy in t hour
            f.append(self.eb_price)     # cost of obtaining 1kw of energy from batteries in t hour (amortization)
            f.append(-self.cr_price[i]) # cost of selling 1kw of energy to the network energy in t hour
            f.append(-self.cb_price[i]) # cost of store 1kw of energy in the battery in t hour
        return f

    def generate_restriction_1(self):
        # 1. EFi+ERi+EBi=CRi+CBi+Cinst+Cprop_i (i=0..23) (the sum of the energy generated must be equal to the sum of the energy consumed)
        # restr_coef will have 120 values (5 variables * 24 hours)
        # i*5 is the t hour of the model, and adds 1,2,3,4 or 5 to point to the variables of f(x) (i*5+0 is EFi, i*5+1 is ERi, etc)
        # i*5 because there are 5 variables for each iteration
        for i in range(0,24):
            restr_coef = [0]*5*24
            restr_coef[i*5] = 1
            restr_coef[i*5+1] = 1
            restr_coef[i*5+2] = 1
            restr_coef[i*5+3] = -1
            restr_coef[i*5+4] = -1
            self.A_eq.append(restr_coef)
            self.b_eq.append(self.c_int + self.c[i])

    def generate_restriction_2(self):
        # 2. EF_night(21:30-7:00) = 0 (no photovoltaic energy is produced at night)
        for i in range(0,24):
            restr_coef = [0]*5*24
            time = (self.start+dt.timedelta(hours=i)).time()
            if time >= dt.time(21,30) or time <= dt.time(7,00):
                restr_coef[i*5] = 1
            self.A_eq.append(restr_coef)
            self.b_eq.append(0)

    def generate_restriction_3(self):
        # 3. EFi <= EFmax_i (the photovoltaic energy obtained must be less than or equal to the maximum possible at t hour)
        for i in range(0,24):
            restr_coef = [0]*5*24
            restr_coef[i*5] = 1
            self.A_ub.append(restr_coef)
        self.b_ub.extend(self.max_ef_buffer)

    def generate_restriction_4(self):
        # 4. EB0 <= initial_level - capacity*depth (the battery energy obtained in hour 0 must be less than or equal to the current level of the battery minus the battery capacity * discharge depth)
        restr_coef = [0]*5*24
        restr_coef[2] = 1
        self.A_ub.append(restr_coef)
        self.b_ub.append(self.battery_level-self.battery_capacity*self.discharge_depth)

    def generate_restriction_5(self):
        # 5. CB0 - EB0 <= capacity - initial_level (the battery charge in hour 0 must be less than or equal to the difference between capacity and (initial_level minus EB0))
        restr_coef = [0]*5*24
        restr_coef[0] = -1
        restr_coef[4] = 1
        self.A_ub.append(restr_coef)
        self.b_ub.append(self.battery_capacity-self.battery_level)

    def generate_restriction_6(self):
        # 6. EBi <= initial_level + Σ(0,i-1){-EBt + CBt} - capacity*depth (the battery energy obtained in hour i must be less than or equal to the current level minus the battery capacity * discarge depth)
        for i in range(1,24):
            restr_coef = [0]*5*24
            restr_coef[i*5+2] = 1
            for j in range(0,i-1):
                restr_coef[j*5+2] = 1
                restr_coef[j*5+4] = -1
            self.A_ub.append(restr_coef)
            self.b_ub.append(self.battery_level-self.battery_capacity*self.discharge_depth)

    def generate_restriction_7(self):
        # 7. CBi <= capacity - (initial_level + Σ(0,i-1){-EBt + CBt}) + EBi (the battery charge in hour i must be less than or equal to the capacity minus the current baterry level in i plus EB in i)
        for i in range(1,24):
            restr_coef = [0]*5*24
            restr_coef[i*5+4] = 1
            restr_coef[i*5+2] = -1
            for j in range(0,i-1):
                restr_coef[j*5+2] = -1
                restr_coef[j*5+4] = 1
            self.A_ub.append(restr_coef)
            self.b_ub.append(self.battery_capacity - self.battery_level)

    def optimize_model(self):
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

        res = linprog(self.f, self.A_ub, self.b_ub, self.A_eq, self.b_eq, bounds=(0,None))

        self.store_result(res)

        return res

    def store_result(self, res):
        values = res.x.tolist()
        out = open("simulations/simulation_{}".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),"w")
        out.write("-----------------------------------------------------\n")
        out.write("--------------- Simulacion Completada ---------------\n")
        out.write("-----------------------------------------------------\n")
        out.write("Inicio:\t{}\nFin:\t{}\n".format(self.start, self.end))
        out.write("Gasto: {} €\n\n".format(res.fun))

        for i in range(0,24):
            out.write("Valores a las {}\n".format((self.start+dt.timedelta(hours=i)).strftime("%H:%M %d/%m/%y")))
            out.write("\t· EF = {} Kwh\n".format(values[i*5]))
            out.write("\t· ER = {} Kwh\n".format(values[i*5+1]))
            out.write("\t· EB = {} Kwh\n".format(values[i*5+2]))
            out.write("\t· CR = {} Kwh\n".format(values[i*5+3]))
            out.write("\t· CB = {} Kwh\n".format(values[i*5+4]))
            out.write("\t· Consumo del Hogar = {} Kwh\n".format(self.c[i]))
            out.write("\t· Consumo del Sistema = {} Kwh\n".format(self.c_int))
            out.write("\n----------------------------------------------\n")
