#!/bin/bash

# Test script for Sidebar Scholar API
# Make sure the server is running: uvicorn main:app --reload --port 3000

BASE_URL="http://localhost:3000"

echo "=== Testing Health Endpoint ==="
curl -X GET "${BASE_URL}/health" \
  -H "Content-Type: application/json" \
  -w "\n\nHTTP Status: %{http_code}\n"

echo -e "\n\n=== Testing /api/ask Endpoint ==="
echo "Note: This requires an API key in .env or passed in the request"

curl -X POST "${BASE_URL}/api/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this page about?",
    "context": {
      "title": "Test Page",
      "url": "https://example.com/test",
      "text": "This is a test page about artificial intelligence and machine learning. It discusses various topics including neural networks, deep learning, and natural language processing.",
      "headings": [
        {"level": "H1", "text": "Introduction to AI"},
        {"level": "H2", "text": "Machine Learning Basics"}
      ]
    },
    "api_provider": "openai"
  }' \
  -w "\n\nHTTP Status: %{http_code}\n"

echo -e "\n\n=== Test with API key in request (if not in .env) ==="
echo "Replace YOUR_API_KEY with your actual API key"
# Uncomment and add your API key to test:
# curl -X POST "${BASE_URL}/api/ask" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "question": "What is this page about?",
#     "context": {
#       "title": "Test Page",
#       "url": "https://example.com/test",
#       "text": "This is a test page about artificial intelligence."
#     },
#     "api_provider": "openai",
#     "api_key": "YOUR_API_KEY"
#   }'
