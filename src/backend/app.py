"""FASTAPI Framework and Main App Endpoints for B&S Auto Web Application.

This module defines the main FastAPI application, including the setup of static file serving,
template rendering, and the primary endpoints for the B&S Auto web application.

The application serves the homepage."""

import os

from typing import AsyncGenerator
import logging
from pydantic import BaseModel
import base64
from contextlib import asynccontextmanager

from starlette.templating import Jinja2Templates
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import asyncpg

from src.backend.routers import handle_form_inputs

# Globals and Configurations
DATABASE_URL = os.getenv("DATABASE_URL")
db_pool = None

# TODO: Move this to config.py and bring in
# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI LifeSpan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan function to manage startup and shutdown events for the FastAPI application."""
    global db_pool

    # Use A client for PostgreSQL - asyncpg - TODO: Move file and bring in connection to Database from else where
    do_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10))

    logger.info("Database connection pool created")

    yield
    await do_pool.close()
    
    logger.info("Database connection pool closed")

# Rate Limiter for API endpoints - Security and traffic management
# ---------------
# Controls the number of requests to an API or server within a specific timeframe
limiter = Limiter(key_func=get_remote_address, default_limits=["1/hour"])

# Initialize FastAPI application
app = FastAPI(
    title="B&S Auto",
    description="A web application for B&S Auto to manage customer interactions and services.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    # debug=False;
)

# Attach the rate limiter to the FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Checkpoint (slowAPI Middleware vs HTTPRedirectMiddleware) 
app.add_middleware()
# Checkpoint (CORS Middleware) Setup Middlware
app.add_middleware()

# Routers
app.include_router(handle_form_inputs.router)

# TODO: See todo.md for notes on updating the CSS paths as they require SCSS compile
# Mount static files so FASTAPI can serve them to the browser
# ---------------
# Static assets (HTML, CSS, jQuery) and compiled TypeScript output are mounted separately
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
app.mount("/dist", StaticFiles(directory="src/frontend/dist"), name="dist")

# Templates for rendering HTML templates, no serving as raw file like `.JS` or `.CSS`
templates = Jinja2Templates(directory="src/frontend/templates/")

# HTML Calls these Endpoints - Page navigation handled by HTML
# ---------------
# Endpoint for the index page
@app.get("/", response_class=HTMLResponse)
def read_homepage(request: Request) -> HTMLResponse:
    """Renders the homepage template."""

    logging.info("Homepage accessed")

    # TODO: Implement ninja for this
    return templates.TemplateResponse("index.html", {"request": request})


###################################
###################################
###################################
###################################
###################################

# Test endpoint for quote submission - to be replaced with actual quote handling logic


# class QuoteSubmission(BaseModel):
#     username: str
#     email: str
#     phone: str
#     registration: str
#     service: str


# @app.post("/api/quote")
# async def submit_quote(payload: QuoteSubmission):
#     logger.info(f"Quote submitted: {payload}")
#     return {"message": "Received", "data": payload}


# fake_db = []


# @app.post("/api/quote")
# def submit(data: dict):
#     fake_db.append(data)
#     return {"status": "ok"}


# @app.get("/debug/db")
# def get_db():
#     return fake_db


# http://127.0.0.1:8000/debug/db
