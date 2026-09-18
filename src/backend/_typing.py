# typing.py
"""Defines type hints and data models for the B&S Autos web application.
This module includes Pydantic models for form data validation and type hints for database interactions."""

from enum import StrEnum


class Service(StrEnum):
    diagnostics = "Diagnostics"
    tyres = "Tyres"
    servicing = "Servicing"
    batteries = "Batteries"
    exhausts = "Exhausts"
    repairs = "Repairs"
