"""
Main FastAPI application for the authentication service.
"""

import logging

from fastapi import FastAPI
from src.api.auth import router as auth_router

# Set up global logging configuration
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for verbose output
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint for service monitoring."""
    return {"status": "ok"}


# Register authentication routes
app.include_router(auth_router)
