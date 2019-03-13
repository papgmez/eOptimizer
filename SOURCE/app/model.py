#!/usr/bin/python3

import project_constants as pc
from scipy.optimize import linprog

class Model:
    def __init__(self, pvm=pc.PV_MODULES, module_price=pc.MODULE_PRICE, yearly_pw_ph=pc.YEARLY_POWER_PH_ESTIMATE, years_ph=pc.YEARS_TO_AMORTIZE_PH, total_batt_price=pc.BATTERY_PRICE, disch_depth=pc.DISCHARGE_DEPTH,batt_size=pc.BATTERY_CAPACITY, years_bat=pc.YEARS_TO_AMORTIZE_BATT, c_int=pc.C_INT, c=pc.C):
        self.pv_modules = pvm
        self.pv_price = self.calculate_pv_price(module_price, years_ph, yearly_pw_ph)
        self.discharge_depth = disch_depth
        self.battery_capacity = batt_size
        self.battery_price = self.calculate_battery_price(total_batt_price, years_bat)
        self.c_int = c_int
        self.c = c

    def calculate_pv_price(self, module_price, years_ph, yearly_pw_ph):
        return (self.pv_modules * module_price / years_ph) / (yearly_pw_ph * self.pv_modules)

    def calculate_battery_price(self, total_batt_price, years_bat):
        return (total_batt_price / years_bat) / self.battery_capacity

    # def f()
