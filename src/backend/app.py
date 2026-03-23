from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse
)
from pydantic import BaseModel
import base64
from starlette.templating import _TemplateResponse

# Initialize FastAPI application
app = FastAPI(title = "B&S Auto")

# Pydantic Data Model
class FormData(BaseModel):
    name: str
    email: str
    message: str

# Form Data Endpoint
@app.post("/submit")
def submit_form(form: FormData): # Todo add return type
    
    return {"status": "ok"}


# Endpoint for the first page the user will see
@app.get("/", response_class=HTMLResponse)
def read_homepage(request: Request) -> _TemplateResponse:
    """Renders the homepage template.

    Parameters
    ----------
    request : Request
        The incoming HTTP request object.


    Returns
    -------
    reponse : _TemplateResponse
        HTML template reponse containing the homepage.
    
    """
    # TODO: Add logging to track homepage access
    # logging.info("Homepage accessed")

    # TODO: Implement ninja for this - see docaid
    return templates.TemplateResponse("new_index.html", {"request": request})



