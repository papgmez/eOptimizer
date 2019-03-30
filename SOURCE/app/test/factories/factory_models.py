#!/usr/bin/python3

import sys
sys.path.append('../..')
from models import Users, Homes
from faker import Faker
import random

faker_generator = Faker()

def generate_user():
    user = Users()
    user.name = faker_generator.first_name()
    user.lastname = faker_generator.last_name()
    user.email = faker_generator.email()
    user.password = faker_generator.password()

    return user

def generate_home(user_id):
    home = Homes()
    home.pv_modules = random.randint(1,100)
    home.city_code = '28079'
    home.amortization_years_pv = random.randint(1,100)
    home.amortization_years_bat = random.randint(1,100)
    home.UserId = user_id

    return home
