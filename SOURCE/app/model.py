#!/usr/bin/python3

import project_constants as pc
import api_esios as esios
from scipy.optimize import linprog

class Model:
    def __init__(self, pvm=pc.PV_MODULES, module_price=pc.MODULE_PRICE, yearly_pw_ph=pc.YEARLY_POWER_PH_ESTIMATE,
                 years_ph=pc.YEARS_TO_AMORTIZE_PH, total_batt_price=pc.BATTERY_PRICE, disch_depth=pc.DISCHARGE_DEPTH,
                 batt_size=pc.BATTERY_CAPACITY, years_bat=pc.YEARS_TO_AMORTIZE_BATT, c_int=pc.C_INT, c=pc.C):
        self.pv_modules = pvm
        self.pv_price = self.calculate_pv_price(module_price, years_ph, yearly_pw_ph)
        self.discharge_depth = disch_depth
        self.battery_capacity = batt_size
        self.battery_price = self.calculate_battery_price(total_batt_price, years_bat)
        self.c_int = c_int
        self.c = c # list of 24 h with the c value of next 24h

    def calculate_pv_price(self, module_price, years_ph, yearly_pw_ph):
        return (self.pv_modules * module_price / years_ph) / (yearly_pw_ph * self.pv_modules)

    def calculate_battery_price(self, total_batt_price, years_bat):
        return (total_batt_price / years_bat) / self.battery_capacity

    def generate_restriction_1(self, i):
        restr_coef = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        restr_coef[i*3] = 1
        restr_coef[i*3+1] = 1
        restr_coef[i*3+2] = -1
        return restr_coef

    def optimize_model(self):
        '''
        Funcion a minimizar:
        -----------------------------------------------
        | f(x) = Σ(0..23) EFi*PFi + ERi*PRi - CRi*PRi |
        -----------------------------------------------
        (Gasto diario en la produccion de energia para autoconsumo)
        '''
        # Coeficientes de f
        # ------------------
        f = []
        pr_buffer = esios.get_incoming_prices() # buffer con los proximos 24 precios del mercado electrico

        for i in range(0,24):
            f.append(self.pv_price) # gasto de producir 1kw de energia fotovoltaica en una hora t
            f.append(pr_buffer[i]) # gasto de comprar 1kw de energia de red en una hora t
            f.append(-pr_buffer[i]) # ganacia de vender 1kw de energia a la red en una hora t
            c_buffer.append(modelo.c_int+modelo.c[i]) # consumo a satisfacer en una hora t (consumo de funcionamiento del sistema + consumo del hogar)

        # Restricciones de <=
        # -------------------
        # A_ub = [[]]
        # b_ub = []

        # Restricciones de =
        # ------------------
        A_eq = [] # Coeficientes de las variables en las restricciones (lado izquierdo)
        b_eq = [] # Constantes en las restricciones (lado derecho)

        # 1. EFi+ERi-CRi=Cinst+Cprop_i (i=0..23)
        for i in range(0,24):
            A_eq.append(modelo.generate_restriction_1(i))
            b_eq.append(modelo.c_int + modelo.c[i])
        # 2.

# f = ef0*pf + er0*pr0 - cr0*pr0 + ef1*pf + er1*pr1 - cr1*pr1 + ef2*pf + er2*pr2 - cr2*pr2 + ef3*pf + er3*pr3 - cr3*pr3 + ef4*pf + er4*pr4 - cr4*pr4 + ef5*pf + er5*pr5 - cr5*pr5 + ef6*pf + er6*pr6 - cr6*pr6 + ef7*pf + er7*pr7 - cr7*pr7 + ef8*pf + er8*pr8 - cr8*pr8 + ef9*pf + er9*pr9 - cr9*pr9 + ef10*pf + er10*pr10 - cr10*pr10 + ef11*pf + er11*pr11 - cr11*pr11 + ef12*pf + er12*pr12 - cr12*pr12 + ef13*pf + er13*pr13 - cr13*pr13 + ef14*pf + er14*pr14 - cr14*pr14 + ef15*pf + er15*pr15 - cr15*pr15 + ef16*pf + er16*pr16 - cr16*pr16 + ef17*pf + er17*pr17 - cr17*pr17 + ef18*pf + er18*pr18 - cr18*pr18 + ef19*pf + er19*pr19 - cr19*pr19 + ef20*pf + er20*pr20 - cr20*pr20 + ef21*pf + er21*pr21 - cr21*pr21 + ef22*pf + er22*pr22 - cr22*pr22 + ef23*pf + er23*pr23 - cr23*pr23
