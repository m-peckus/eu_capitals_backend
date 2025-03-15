#!/usr/bin/env python3

from nested_eu_data import *

def check_eu_capital(city):
    
    if city in eu_data_extended:
        country = eu_data_extended[city]["country"]
        currency = eu_data_extended[city]["currency_name"]
        return city, country, currency
    else:
        return city

#print(check_eu_capital("Vilnius"))