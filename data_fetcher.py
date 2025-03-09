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

# 2 SAME FUNCTIONS?
def format_population(population):
    """Format population number with dot separators."""
    return f"{population:,}".replace(",",".") + " residents"

def format_country_population(population):
    """Format country population with dot separators."""
    return f"{population:,}".replace(",",".") + " residents"

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
        "countryIds": eu_data[city]["iso_code"],
        "limit": 1,
        "minPopulation": 400000
    }
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "wtf-geo-db.p.rapidapi.com"
    }

    try:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                # API call failed - return fallback data
                return format_population(eu_data_extended[city].get("city_population", "Unknown"))

            data = await response.json()
            cities = data.get("data",[])
            if not cities:
                # No data returned - return fallback
                return format_population(eu_data_extended[city].get("city_population", "Unknown"))
            
            return format_population(cities[0].get("population", eu_data_extended[city].get("city_population", "Unknown")))
        
    except Exception:
        # Any network/API error - return fallback data from eu_data_extended
        return format_population(eu_data_extended[city].get("city_population","Unknown"))


async def fetch_country_population(session, country):
    """Fetches population data for a country."""
    if country == "Ireland":
        return format_country_population(IRELAND_POPULATION)

    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        async with session.get(url) as response:
            data = await response.json()
            if response.status != 200 or not data or "population" not in data[0]:
                # fall back logic can be here if needed
                return f"No population data found for {country}."
            return format_country_population(data[0]["population"])

    except Exception as e:
        # fall back logic can be here if needed
        return f"Country population API error: {e}"


# add more details as needed
async def fetch_all_data(city, country):
    """Fetches all required API data asynchronously."""
    async with aiohttp.ClientSession() as session:
        country_code = eu_data[city]["iso_code"]
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
    

# add more details as needed
def get_data(city, country):
    """Runs the async function synchronously for integration in main script."""
    return asyncio.run(fetch_all_data(city, country))