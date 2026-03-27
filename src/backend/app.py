from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import base64
from starlette.templating import Jinja2Templates


# Initialize FastAPI application
app = FastAPI(
    title="B&S Auto",
    description="A web application for B&S Auto to manage customer interactions and services.",
    version="1.0.0",
)


# TODO: See todo.md for notes on updating the CSS paths as they require SCSS compile
# | Mount static files so the browser can download/render them
# ---------------
# | File on disk                        | URL in browser          |
# | ----------------------------------- | ----------------------- |
# | `src/frontend/static/js/app.js`     | `/static/js/app.js`     |
# | `src/frontend/static/css/style.css` | `/static/css/style.css` |
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")


# Templates for rendering HTML templates
# Instead of just serving it as a raw file like .JS or .CSS
# HTML is Returned by FastAPI via endpoints
templates = Jinja2Templates(directory="src/frontend/templates/")


# HTML Calls these Endpoints - Page navigation handled by HTML
# ---------------
# Endpoint for the index page
@app.get("/", response_class=HTMLResponse)
def read_homepage(request: Request) -> HTMLResponse:
    """Renders the homepage template.

    Parameters
    ----------
    request : Request
        The incoming HTTP request object from FastAPI.


    Returns
    -------
    reponse : HTMLResponse
        HTML template reponse containing the homepage.

    """
    # TODO: Add logging to track homepage access
    # logging.info("Homepage accessed")

    # TODO: Implement ninja for this - see docaid
    return templates.TemplateResponse("index.html", {"request": request})


# Pydantic Data Model
# class FormData(BaseModel):
#     name: str
#     email: str
#     message: str

# # Form Data Endpoint
# @app.post("/submit")
# def submit_form(form: FormData): # Todo add return type

#     return {"status": "ok"}
