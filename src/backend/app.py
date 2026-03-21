from fastapi import FastAPI
from pydantic import BaseModel
import base64

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



