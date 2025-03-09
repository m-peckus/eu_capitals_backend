#!/usr/bin/env python3

from nested_eu_data import *

def check_eu_capital(city):
    
    if city in eu_data:
        country = eu_data[city]["country"]
        currency = eu_data[city]["currency_name"]
        return city, country, currency
    else:
        return city

#print(check_eu_capital("Vilnius"))