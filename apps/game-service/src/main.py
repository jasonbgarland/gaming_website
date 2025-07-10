"""
Entry point for the Game Data Service (IGDB) FastAPI application.
Initializes the FastAPI app and includes IGDB API routes.
"""

from fastapi import FastAPI

from src.api import igdb

app = FastAPI(title="Game Data Service (IGDB)")

# Include IGDB API routes
app.include_router(igdb.router, prefix="/igdb", tags=["IGDB"])
