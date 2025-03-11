#!/usr/bin/env python3

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data_fetcher import get_data
from nested_eu_data import *

app = FastAPI()

# Load HTML templates
templates = Jinja2Templates(directory="/home/mpeckus/eu_capitals_backend/app/templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, restart: bool = False):
    return templates.TemplateResponse("index.html", {"request":request, "result": None, "restart": restart})

@app.post("/", response_class=HTMLResponse)
async def fetch_info(request: Request, city: str = Form(...)):
    city = city.strip().title() # Normalize input

    if city in eu_data_extended:
        country = eu_data_extended[city]["country"]
        currency = eu_data_extended[city]["currency_name"]

        # Fetch full data (population, exchange rate, weather, etc.)
        data = await get_data(city, country)

        result = {
            "city_found": True,
            "city": city,
            "country": country,
            "currency": currency,
            "city_population": data["city_population"],
            "country_population": data["country_population"],
            "exchange_rate": data["exchange_rate"] if currency != "Euro" else None,
            "temperature": data["temperature"],
        }
    else:
        result = {"city_found": False, "city": city}

    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.get("/exit", response_class=HTMLResponse)
async def exit_page(request: Request):
    return templates.TemplateResponse("exit.html", {"request": request})