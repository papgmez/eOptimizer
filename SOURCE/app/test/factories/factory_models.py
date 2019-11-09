#!/usr/bin/python3

import sys
import random

from faker import Faker
from models import Users, Homes

sys.path.append('../..')


FAKER_GENERATOR = Faker()

def generate_user():
    user = Users()
    user.name = FAKER_GENERATOR.first_name()
    user.lastname = FAKER_GENERATOR.last_name()
    user.email = FAKER_GENERATOR.email()
    user.set_password(FAKER_GENERATOR.password())

    return user

def generate_home(user_id):
    home = Homes()
    home.pv_modules = random.randint(1, 100)
    home.city_code = '28079'
    home.amortization_years_pv = random.randint(1, 100)
    home.amortization_years_bat = random.randint(1, 100)
    home.UserId = user_id

    return home
