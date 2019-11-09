#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import unittest
import datetime as dt

from faker import Faker
from helpers import api_aemet, api_esios
from config import project_constants as const

class test_API(unittest.TestCase):

    def test_get_weather_today(self):
        city_code = '13034'
        response_buffer = api_aemet.get_weather_today(city_code)

        self.assertEqual(len(response_buffer), 24)

    def test_get_weather_today_fail(self):
        city_code = 'XXXXX'
        response_buffer = api_aemet.get_weather_today(city_code)

        self.assertEqual(len(response_buffer), 0)

    def test_get_weather_archive(self):
        date = Faker().date_this_year(before_today=True, after_today=False)
        date = date.strftime("%Y-%m-%d")
        city_code = '13034'
        response_buffer = api_aemet.get_weather_archive(date, city_code)

        self.assertEqual(len(response_buffer), 24)

    def test_get_weather_archive_fail(self):
        date = 'fake-date'
        city_code = '13034'
        response_buffer = api_aemet.get_weather_archive(date, city_code)

        self.assertEqual(len(response_buffer), 0)

    def test_get_esios_prices(self):
        start = dt.datetime.now()
        end = start + dt.timedelta(1)
        indicator = const.PVPC
        response_buffer = api_esios.get_incoming_prices(indicator, start, end)

        self.assertEqual(len(response_buffer), 24)

    def test_get_esios_prices_fail(self):
        start = dt.datetime.now()
        end = start + dt.timedelta(1)
        indicator = 'XXXXX'
        response_buffer = api_esios.get_incoming_prices(indicator, start, end)

        self.assertEqual(len(response_buffer), 0)

if __name__ == '__main__':
    unittest.main()
