#!/usr/bin/env python3

from fastapi import FastAPI
from data_fetcher import get_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "EU Capitals Info API is running!"}

@app.get("/fetch")
def fetch_data(city: str, country: str):
    """Fetches data for a given EU capital."""
    try:
        data = get_data(city, country)
        return {"city": city, "country": country, "data": data}
    except Exception as e:
        return {"error": str(e)}