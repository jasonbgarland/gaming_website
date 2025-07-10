"""
Main FastAPI application for the authentication service.
"""

from fastapi import FastAPI
from src.api.auth import router as auth_router

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint for service monitoring."""
    return {"status": "ok"}


# Register authentication routes
app.include_router(auth_router)
