#!/usr/bin/env python3

from user_input import *
from data_fetcher import get_data
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Access API key for Open Weather Map from .env file
WEATHER_API_KEY = os.getenv('OPEN_WEATHER_MAP_API_KEY')
# Access API key for GeoDB from .env file
city_api_key = os.getenv('RAPID_API_KEY')


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    user_input = input(
        "Enter the name of an EU capital city to get:\n"
        "- Confirmation of EU capital status\n"
        "- Country population data\n"
        "- Local currency & exchange rate (if not Euro)\n"
        "- Local temperature\n"
        "- Enter any other city name to check if it's an EU capital.\n- Or press 5 to exit\n"
        "Enter city name : "
    )


    if user_input == '5':
        print("Exiting the program. Goodbye!")
        break
    
    clear_screen()

    # Ensure city exists in the extended dictionary
    #if user_input not in eu_data_extended:
        #print(f"No data available for {user_input}.")
    #if user_input.isdigit():
        #print("Invalid input: Please enter a valid city name, not a number\n")
    #elif not user_input.isalpha():
        #print("Invalid input: City names should only contain letters\n")
    #elif len(user_input) > 12:
        #print("Invalid input: City names can't exceed 12 characters.\n")
    #else:
    user_input = user_input.title()
    if user_input in eu_data_extended:
        result = check_eu_capital(user_input)
        city, country, currency = result
        data = get_data(city, country)
    if user_input not in eu_data_extended:
        pass
        

    #if data['temperature'] is None:
        #print("Unable to retrieve temperature data. Please try again later.")

    if isinstance(result, tuple) and len(result) == 3:
        city, country, currency = result
        if currency != "Euro":
            print(
                f"{city} is a capital city of {country}.\n"
                f"- Population of {city}: {data['city_population']}.\n"
                f"- Population of {country}: {data['country_population']}.\n"
                f"- Local currency is {currency}.\n"
                f"- 1 {currency} equals to {data['exchange_rate']} Euro.\n"
                f"- Weather temperature in {city} is {data['temperature']}°C\n"
                )
        if currency == "Euro":
            print(
                f"{city} is a capital city of {country}.\n"
                f"- Population of {city}: {data['city_population']}.\n"
                f"- Population of {country}: {data['country_population']}.\n"
                f"- Local currency is {currency}.\n"
                f"- Weather temperature in {city} is {data['temperature']}°C\n"
                )
        
    else:
        print(
            f"{result} is not a rezognized EU capital.\n"
            )

