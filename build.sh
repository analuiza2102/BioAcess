#!/bin/bash
# Railway build script

echo "📦 Installing Python dependencies..."
python -m pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed!"
