#!/usr/bin/python3

import project_constants as const
from scipy.optimize import minimize

def calculate_EF(current_mnp):
    return const.PV_MODULES * current_mnp / 1000

def f()
# C + (EFr*EF+EBr*EB) + (EFb*EF+ERb*ER) + (EFc*EF+EFr*ER+EBc*EB
# f = sumatorio 0,24 (EFr*EF+EBr*EB)*Pr + (EFv*EF+EBv*EB+ERv*ER)*Pv - ER*Pv
