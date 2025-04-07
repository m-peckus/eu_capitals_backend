#!/usr/bin/env python3

import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
# Old file path works locally
# from data_fetcher import get_data
# New file path for Reneder deployment
from app.data_fetcher import get_data
from nested_eu_data import eu_data_extended

# Load keys from .env file
load_dotenv()
SessionMiddleware_key = os.getenv('Middleware_Key')

# Initialize FAstAPI app
app = FastAPI()
# Add session middleware for storing quiz progress
app.add_middleware(SessionMiddleware, secret_key=SessionMiddleware_key)

# Setup Jinja2 templates for rendering HTML

# Old Line 
# templates = Jinja2Templates(directory="/home/mpeckus/eu_capitals_backend/app/templates")

# New Line from here
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR,"templates"))
# New Line until here

# Load static files
# Old Line
#app.mount("/static", StaticFiles(directory="/home/mpeckus/eu_capitals_backend/app/static"), name="static")

# New Line from here
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
# New Line until here

TOTAL_CAPITALS = len(eu_data_extended) # Total number of EU capitals

@app.get("/")
async def index(request: Request):
    """Renders the main quiz page and ensures session reset on restart."""
    session = request.session

    # Force session reset if restarting the app
    if "initialized" not in session:
        session.clear() # Clear old session data
        session["score"] = TOTAL_CAPITALS # Reset score
        session["previous_answers"] = [] # Reset previous answers list
        session["initialized"] = True # Mark session as initialized

    #if "score" not in session:
        #session["score"] = TOTAL_CAPITALS # Start with 27 EU capitals
        #session["previous_answers"] = [] # Track user answers

    return templates.TemplateResponse("index.html", {
        "request":request, 
        "score": session["score"],
        "previous_answers": session["previous_answers"],
        "result": None # No data initially
    })

@app.post("/")
# Old Line
#async def proccess_city(request: Request, city: str = Form(...)):
# New Line
async def proccess_city(request: Request, city: str = Form()):

    """Processes user input, updates quiz progress, and displays API results."""
    session = request.session
    city = city.strip().title() # Normalize input

    if "score" not in session or "previous_answers" not in session:
        session["score"] = TOTAL_CAPITALS
        session["previous_answers"] = []

    # Validate city using 'eu_data_extended'
    if city in eu_data_extended:
        country = eu_data_extended[city]["country"]
        currency = eu_data_extended[city]["currency_name"]
        result = await get_data(city, country) # Fetch API data (fallback handled inside)

        result["city"] = city
        result["country"] = country
        result["currency"] = currency
        result["city_found"] = True
        #result["message"] = (
            #f"{city} is the capital of the {country}.\n"
            #f"City population: {result['city_population']}.\n"
            #f"Country population: {result['country_population']}.\n"
            #f"Temperature: {result['temperature']}.\n"
            #f"Exchange rate: {result['exchange_rate']}"
       # )
       
        # Update score only if it's a new valid answer
        if city not in session["previous_answers"]:
            session["previous_answers"].append(city) # Store answer
            session["score"] -= 1 # Reduce score only for new correct answer

    else:
        result = {
            "city": city, 
            "city_found": False,
            "message": f"{city} is not recognized EU capital city."
            }     # Invalid city

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": result,
        "score": session["score"],
        "previous_answers": list(session["previous_answers"])
        })

@app.get("/exit")
async def exit_page(request: Request):
    """Renders the exit page"""
    return templates.TemplateResponse("exit.html", {"request": request})

@app.get("/restart")
async def restart_quiz(request: Request):
    """Restart quiz progress."""
    request.session.clear() # Clear all session data
    request.session["score"] = TOTAL_CAPITALS # Reset score to initial value
    request.session["previous_answers"] = [] # Reset answered cities list

    return templates.TemplateResponse("index.html", {
        "request": request,
        "score": request.session["score"],
        "previous_answers": request.session["previous_answers"],
        "restart": True,
        "result": None # Clear previous result

    })