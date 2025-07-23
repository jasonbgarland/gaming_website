# Dockerfile for Game Data Service (IGDB)

FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl libpq-dev \
    && pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements to cache dependencies
COPY apps/game_service/pyproject.toml ./
COPY apps/game_service/poetry.lock ./

# Install dependencies
RUN poetry install --no-root --only main

# Create directory structure to match local development
RUN mkdir -p /app/apps/game_service

# Copy the rest of the code maintaining monorepo structure
COPY apps/game_service/src/ /app/apps/game_service/src/
# Copy db models from monorepo root
COPY db ./db
# Copy shared code from monorepo root
COPY shared ./shared

# Set PYTHONPATH to include all necessary directories
ENV PYTHONPATH=/app:/app/apps/game_service

# Expose port
EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "apps.game_service.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
