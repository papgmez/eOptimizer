#!/usr/bin/python3

import project_constants as pc
import api_esios as esios
import api_aemet as aemet
import datetime as dt
from scipy.optimize import linprog
import numpy as np

class Model:
    def __init__(self,pvm=pc.PV_MODULES,module_price=pc.MODULE_PRICE,yearly_pw_ph=pc.YEARLY_POWER_PH_ESTIMATE,years_ph=pc.YEARS_TO_AMORTIZE_PH,
                total_batt_price=pc.BATTERY_PRICE,disch_depth=pc.DISCHARGE_DEPTH,batt_size=pc.BATTERY_CAPACITY,years_bat=pc.YEARS_TO_AMORTIZE_BATT,c_int=pc.C_INT,c=pc.C):
        self.ef_price = self.calculate_ef_price(pvm, module_price, years_ph, yearly_pw_ph)
        self.discharge_depth = disch_depth
        self.battery_capacity = batt_size
        self.eb_price = self.calculate_eb_price(total_batt_price, years_bat)
        self.c_int = c_int
        # ---- buffers of data ----
        self.max_ef_buffer = self.calculate_max_ef_buffer(pvm) # buffer con los proximos 24 valores maximos posibles de energia fotovoltaica que se puede obtener
        self.cr_price = esios.get_incoming_prices(pc.SPOT) # buffer con los proximos 24 precios del mercado electrico
        self.er_price = esios.get_incoming_prices(pc.PVPC) # buffer con los proximos 24 precios de PVPC de electricidad
        self.c = c # buffer con el consumo del hogar de las prox. 24h
        # ---- rango temporal del modelo ----
        self.start = dt.datetime.now()
        self.end = self.start + dt.timedelta(1)

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

    def generate_restriction_1(self, i):
        # EFi+ERi-CRi=Cinst+Cprop_i (i=0..23)
        restr_coef = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        restr_coef[i*3] = 1
        restr_coef[i*3+1] = 1
        restr_coef[i*3+2] = -1
        return restr_coef

    def generate_restriction_2(self,i):
        # EFi <= EFmax_i
        restr_coef = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        restr_coef[i*3] = 1
        return restr_coef

    def generate_restriction_3(self,i):
        # EF_nigth(21:30-7:00) = 0
        restr_coef = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        time = (self.start+dt.timedelta(hours=i)).time()
        if time >= dt.time(21,30) or time <= dt.time(7,00):
            restr_coef[i*3] = 1
        return restr_coef

    def optimize_model(self):
        '''
        Funcion a minimizar:
        -----------------------------------------------
        | f(x) = Σ(0..23) EFi*PFi + ERi*PRi - CRi*PRi |
        -----------------------------------------------
        (Gasto diario en la produccion de energia para autoconsumo)
        '''
        f = []

        for i in range(0,24):
            f.append(self.ef_price) # gasto de producir 1kw de energia fotovoltaica en una hora t
            f.append(self.er_price[i]) # gasto de comprar 1kw de energia de red en una hora t
            f.append(-self.cr_price[i]) # ganacia de vender 1kw de energia a la red en una hora t

        # Restricciones de =
        # ------------------
        A_eq = [] # Coeficientes de las variables en las restricciones (lado izquierdo)
        b_eq = [] # Constantes en las restricciones (lado derecho)

        # EFi+ERi-CRi=Cinst+Cprop_i (i=0..23) (la suma de la energia generada debe ser igual a la suma de la energia consumida)
        for i in range(0,24):
            A_eq.append(self.generate_restriction_1(i))
            b_eq.append(self.c_int + self.c[i])

        # EF_night = 0 (no se produce energia fotovoltaica por la noche)
        for i in range(0,24):
            A_eq.append(self.generate_restriction_3(i))
            b_eq.append(0)

        # Restricciones de <=
        # -------------------
        A_ub = [] # Coeficientes de las variables en las restricciones (lado izquierdo)
        b_ub = [] # Constantes en las restricciones (lado derecho)

        # EFi <= EFmax_i (la energia fotovoltaica que se obtiene debe ser menor o igual que la maximaa posible en esa hora t)
        for i in range(0,24):
            A_ub.append(self.generate_restriction_2(i))
            b_ub.extend(self.max_ef_buffer)

        res = linprog(f, A_ub, b_ub, A_eq, b_eq, bounds=(0,None))

        print(res)

        return res.x.tolist()
