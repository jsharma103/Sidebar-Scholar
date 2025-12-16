#!/bin/bash

# Fix dependencies for Sidebar Scholar backend
echo "Updating Python dependencies..."

# Upgrade pip first
pip install --upgrade pip

# Uninstall conflicting packages
pip uninstall -y openai httpx anthropic

# Install compatible versions
pip install --upgrade "openai>=1.12.0" "httpx>=0.25.0" "anthropic>=0.18.0"

echo "Dependencies updated! Please restart your FastAPI server."
