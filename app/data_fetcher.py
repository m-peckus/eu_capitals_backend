#!/usr/bin/env python3

import asyncio
import aiohttp
import math
import os
from dotenv import load_dotenv
from nested_eu_data import *

# Load API keys from .env file
load_dotenv()
OPEN_WEATHER_MAP_API_KEY = os.getenv('OPEN_WEATHER_MAP_API_KEY')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

# Hardcoded population fixes
FIXED_POPULATIONS = {
    "Valletta": "5.157 residents",
    "Rome": "2.760.000 residents"
}

# Ireland's fixed population
IRELAND_POPULATION = 5262000

def format_number(value):
    """Format population number with dot separators and append 'residents'."""
    return f"{value:,}".replace(",",".") + " residents"


async def fetch_weather(session, city, country_code):
    """Fetches temperature data for a city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPEN_WEATHER_MAP_API_KEY}"

    try:
        async with session.get(url) as response:
            data = await response.json()
            if response.status != 200 or "main" not in data:
                return f"Error featching weather data for {city}."
            
            temp_kelvin = data['main']['temp']
            temp_celsius = math.floor(temp_kelvin - 273.15)
            return temp_celsius
        
    except Exception as e:
        return f"Weather API error {e}"


async def fetch_currency(session, city):
    """Fetches exchange rate if local currency is not Euro."""
    currency = eu_data_extended[city]["currency_code"]
    if currency == "EUR":
        return f"Local currency in {city} is Euro (no exchange rate needed)."
    
    url = f"https://api.frankfurter.app/latest?from=EUR&to={currency}"
    try:
        async with session.get(url) as response:
            data = await response.json()
            if response.status != 200 or "rates" not in data:
                return f"Error fetching exchange rate for {currency}."
            
            exchange_rate = data["rates"].get(currency)
            return round(1 / exchange_rate, 2) if exchange_rate else f"No exchange rate found."
    except Exception as e:
        return f"Currency API error: {e}"
    
async def fetch_capital_population(session, city):
    """Fetches population data for a capital city."""
    """Falls back to nested_eu_dictionary data if API calls fails."""
    if city in FIXED_POPULATIONS:
        return FIXED_POPULATIONS[city]
    
    # Ensure city exists in the extended dictionary
    if city not in eu_data_extended:
        return f"No population data available for {city}."
    
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    params = {
        "namePrefix": city,
        "countryIds": eu_data_extended[city]["iso_code"],
        "limit": 1,
        "minPopulation": 400000
    }
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    try:
        async with session.get(url, headers=headers, params=params) as response:
            data = await response.json()
            if response.status != 200 or not data.get("data", []):
                # API call failed - return fallback data
                return format_number(eu_data_extended[city].get("city_population", "Unknown"))
            return format_number(data["data"][0].get("population", eu_data_extended[city]["city_population"]))
        
    except Exception:
            return format_number(eu_data_extended[city]["city_population"])


async def fetch_country_population(session, country):
    """Fetches population data for a country. Falls back to eu_data_extended if API call fails."""
    if country == "Ireland":
        return format_number(IRELAND_POPULATION)

    # Get a city from eu_data_extended to access the country's stored population
    city = next(city for city, data in eu_data_extended.items() if data["country"] == country)

    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        async with session.get(url) as response:
            data = await response.json()
            if response.status != 200 or not data or "population" not in data[0]:
                raise ValueError("Invalid API response")  # Trigger fallback
                
            return format_number(data[0]["population"])

    except Exception:
        # Fallback: Return stored country population from eu_data_extended
        return format_number(eu_data_extended[city]["country_population"])
        


async def fetch_all_data(city, country):
    """Fetches all required API data asynchronously."""
    async with aiohttp.ClientSession() as session:
        country_code = eu_data_extended[city]["iso_code"]
        tasks = [
            fetch_weather(session, city, country_code),
            fetch_currency(session, city),
            fetch_capital_population(session, city),
            fetch_country_population(session, country)
        ]
        results = await asyncio.gather(*tasks)
        return {
            "temperature": results[0],
            "exchange_rate": results[1],
            "city_population": results[2],
            "country_population": results[3]
        }
    

async def get_data(city, country):
    """Runs fetch_all_data() asynchronously."""
    return await fetch_all_data(city, country)

