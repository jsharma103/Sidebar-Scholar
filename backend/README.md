# Sidebar Scholar Backend API

FastAPI backend server for the Sidebar Scholar Chrome extension. Handles AI API calls and provides a secure endpoint for the extension to communicate with.

## Features

- 🔒 **Secure API Key Management**: API keys stored server-side, never exposed to client
- 🤖 **Multiple AI Providers**: Supports OpenAI and Anthropic (Claude)
- 🚀 **Fast & Efficient**: Built with FastAPI for high performance
- 📚 **Auto Documentation**: Interactive API docs at `/docs` and `/redoc`
- 🛡️ **Error Handling**: Comprehensive error handling and validation
- 📝 **Configurable**: Environment-based configuration

## Setup

### 1. Install Python Dependencies

Make sure you have Python 3.8+ installed, then:

```bash
cd backend
pip install -r requirements.txt
```

Or using a virtual environment (recommended):

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Choose your default provider
DEFAULT_API_PROVIDER=openai

# Add at least one API key
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 3. Start the Server

**Development mode:**
```bash
uvicorn main:app --reload --port 3000
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 3000
```

Or using Python directly:
```bash
python main.py
```

The server will start on `http://localhost:3000`

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

## API Endpoints

### POST `/api/ask`

Main endpoint for asking questions about web page content.

**Request Body:**
```json
{
  "question": "What is this page about?",
  "context": {
    "title": "Page Title",
    "url": "https://example.com",
    "text": "Page content text...",
    "headings": [
      {"level": "H1", "text": "Main Heading"}
    ]
  },
  "api_provider": "openai",  // optional, uses default if not provided
  "api_key": "sk-..."        // optional, uses server default if not provided
}
```

**Response:**
```json
{
  "answer": "This page is about...",
  "provider": "openai",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `NODE_ENV` | Environment (development/production) | `development` |
| `DEFAULT_API_PROVIDER` | Default AI provider | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `OPENAI_TEMPERATURE` | OpenAI temperature | `0.7` |
| `OPENAI_MAX_TOKENS` | Max tokens for OpenAI | `1000` |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `ANTHROPIC_MODEL` | Anthropic model to use | `claude-3-haiku-20240307` |
| `ANTHROPIC_MAX_TOKENS` | Max tokens for Anthropic | `1000` |

## API Providers

### OpenAI

- **Models Available**: `gpt-4o-mini`, `gpt-4o`, `gpt-3.5-turbo`, etc.
- **Get API Key**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Cost**: Pay per token usage

### Anthropic (Claude)

- **Models Available**: `claude-3-haiku-20240307`, `claude-3-sonnet-20240229`, `claude-3-opus-20240229`
- **Get API Key**: [Anthropic Console](https://console.anthropic.com/)
- **Cost**: Pay per token usage

## Usage with Chrome Extension

The Chrome extension will send requests to this backend server. Make sure:

1. The server is running
2. CORS is properly configured (already set up for `*` origin)
3. The extension knows the server URL (will be configured in extension settings)

## Development

### Project Structure

```
backend/
├── main.py                    # FastAPI application
├── services/
│   ├── __init__.py
│   ├── openai_service.py     # OpenAI API integration
│   └── anthropic_service.py  # Anthropic API integration
├── utils/
│   ├── __init__.py
│   └── prompt_builder.py     # Builds prompts from context
├── requirements.txt
├── .env.example
└── README.md
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Adding New API Providers

1. Create a new service file in `services/` (e.g., `custom_service.py`)
2. Create an async function that takes `(api_key: str, prompt: str)` and returns the answer
3. Add the provider case in `main.py` in the `/api/ask` endpoint
4. Update environment variables if needed

## Security Considerations

- ⚠️ **CORS**: Currently set to `*` for development. In production, restrict to your extension's origin:
  ```python
  allow_origins=["chrome-extension://your-extension-id"]
  ```
- 🔑 **API Keys**: Never commit `.env` file to version control
- 🛡️ **Rate Limiting**: Consider adding rate limiting middleware for production:
  ```bash
  pip install slowapi
  ```
- 🔐 **Authentication**: For multi-user scenarios, add authentication tokens

## Troubleshooting

### Server won't start
- Check that port 3000 (or your configured port) is available
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.8+)

### Import errors
- Make sure you're running from the `backend` directory
- Verify virtual environment is activated
- Check that all packages are installed

### API errors
- Verify your API keys are correct in `.env`
- Check API provider status/quotas
- Review server logs for detailed error messages
- Check `/docs` endpoint for API schema validation

### CORS errors
- Ensure CORS middleware is properly configured
- Check that the extension is sending requests to the correct origin

## License

MIT License
