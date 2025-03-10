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
    ).title().strip()


    if user_input == '5':
        print("Exiting the program. Goodbye!")
        break
    
    clear_screen()

    if user_input.isdigit() or len(user_input) > 12 or not user_input.replace("","").isalpha():
        print("Invalid input: Enter a valid city name(letters only, max 12 characters)\n")
        continue

    result = check_eu_capital(user_input)

    if isinstance(result, tuple) and len(result) == 3:
        city, country, currency = result
        data = get_data(city, country)

        print(f"{city} is the capital city of {country}.")
        print(f"- Population of {city}: {data['city_population']}.")
        print(f"- Population of {country}: {data['country_population']}.")
        print(f"- Local currency is {currency}.")
        if currency != "Euro":
                print(f"- 1 {currency} = {data['exchange_rate']} Euro.")

        print(f"- Weather temperature in {city}: {data['temperature']}°C\n")
    else:
        print(f"{user_input} is not a recognized EU capital.\n")


