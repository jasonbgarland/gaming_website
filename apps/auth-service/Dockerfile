# Start from an official Python image
FROM python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl \
    && pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy only requirements to cache dependencies
COPY pyproject.toml ./
COPY poetry.lock ./

# Install dependencies
RUN poetry install --no-root --only main

# Copy the rest of the code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
