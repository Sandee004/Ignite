#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node dependencies and Build Frontend
# Assuming your frontend is in a folder named 'frontend'
echo "Building Frontend..."
cd frontend
npm install
npm run build
cd ..

# 3. (Optional) Run database migrations
# python backend/api.py # or wherever your migration logic is