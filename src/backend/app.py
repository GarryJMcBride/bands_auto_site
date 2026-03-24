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
# Mount static files (CSS, JS, images) to be served to the DOM
app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
# TODO: This neeeds to be reviewed whenever we start to use typescript for backend logic
app.mount("/js", StaticFiles(directory="src/frontend/js"), name="js")
# Compiled folder for when TypeScript compiles to JS at runtime
# app.mount("/dist", StaticFiles(directory="dist"), name="dist")
# Initialize Jinja2 templates for rendering HTML templates
templates = Jinja2Templates(directory="src/frontend/static/HTML")


# Endpoint for the first page the user will see
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
    return templates.TemplateResponse("new_index.html", {"request": request})


# Pydantic Data Model
# class FormData(BaseModel):
#     name: str
#     email: str
#     message: str

# # Form Data Endpoint
# @app.post("/submit")
# def submit_form(form: FormData): # Todo add return type

#     return {"status": "ok"}
