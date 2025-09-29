#!/bin/bash

# Gaming Website Development Environment Startup Script
# This script starts all services in development mode with hot reloading

echo "🚀 Starting Gaming Website Development Environment..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🏗️  Building and starting services..."
echo "   - PostgreSQL Database"
echo "   - Database Migrations"
echo "   - Auth Service (with hot reload)"
echo "   - Game Service (with hot reload)"  
echo "   - Frontend (with hot reload)"
echo ""

# Use development override configuration
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

echo ""
echo "🛑 Development environment stopped."