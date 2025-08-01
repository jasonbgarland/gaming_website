"""
Entry point for the Game Data Service (IGDB) FastAPI application.
Initializes the FastAPI app and includes IGDB API routes.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import igdb
from src.api.collection_entry import router as collection_entry_router
from src.api.collections import router as collections_router

# Set up global logging configuration
logging.basicConfig(
    level=logging.INFO,  # Change to logging.DEBUG for verbose output
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(title="Game Data Service (IGDB)")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint for service monitoring."""
    return {"status": "ok"}


# Include IGDB API routes
app.include_router(igdb.router, prefix="/igdb", tags=["IGDB"])

# Include Collections API routes
app.include_router(collections_router)
app.include_router(collection_entry_router)
