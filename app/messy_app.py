#!/usr/bin/env python3

import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from data_fetcher import get_data
from nested_eu_data import eu_data_extended

# Load keys from .env file
load_dotenv()
SessionMiddleware_key = os.getenv('Middleware_Key')

# Initialize FAstAPI app
app = FastAPI()
# Add session middleware for storing quiz progress
app.add_middleware(SessionMiddleware, secret_key="SessionMiddelware_key")

# Setup Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="/home/mpeckus/eu_capitals_backend/app/templates")

# Load static files
app.mount("/static", StaticFiles(directory="/home/mpeckus/eu_capitals_backend/app/static"), name="static")

TOTAL_CAPITALS = len(eu_data_extended) # Total number of EU capitals

@app.get("/")
async def index(request: Request):
    """Renders the main quiz page."""
    session = request.session

    if "score" not in session:
        session["score"] = TOTAL_CAPITALS # Start with 27 EU capitals
        session["previous_answers"] = [] # Track user answers

    return templates.TemplateResponse("index.html", {
        "request":request, 
        "score": session["score"],
        "previous_answers": session["previous_answers"],
        "result": None # No data initially
    })

@app.post("/")
async def proccess_city(request: Request, city: str = Form(...)):
    """Processes user input, updates quiz progress, and displays API results."""
    session = request.session
    city = city.strip().title() # Normalize input

    if "score" not in session or "previous_answers" not in session:
        session["score"] = TOTAL_CAPITALS
        session["previous_answers"] = []

    # Validate city using 'eu_data_extended'
    if city in eu_data_extended:
        country = eu_data_extended[city]["country"]
        result = await get_data(city, country) # Fetch API data (fallback handled inside)

        # Update score only if it's a new valid answer
        if city not in session["previous_answers"]:
            session["previous_answers"].append(city) # Store answer
            session["score"] -= 1 # Reduce score only for new correct answer

    else:
        result = {"city": city, "city_found": False}     # Invalid city

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
    request.session.clear()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "score": TOTAL_CAPITALS,
        "previous_answers": set(),
        "restart": True,
        "result": None # Clear previous result

    })