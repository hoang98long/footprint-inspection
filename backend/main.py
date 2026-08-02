"""FastAPI application entry point; routes are intentionally not registered in the skeleton."""

from fastapi import FastAPI


app = FastAPI(
    title="Footprint Inspection",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
