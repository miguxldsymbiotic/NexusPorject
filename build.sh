#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Building Frontend (Vite) ---"
cd frontend
npm install
npm run build
cd ..

echo "--- Preparing Backend Static Directory ---"
mkdir -p backend/static
# Optional: keep some files if needed, but usually we want a clean build
# rm -rf backend/static/* 
cp -r frontend/dist/* backend/static/

echo "--- Installing Backend Dependencies ---"
cd backend
pip install -r requirements.txt
cd ..

echo "--- Build Complete ---"
