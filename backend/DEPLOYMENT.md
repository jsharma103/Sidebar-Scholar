# Backend Deployment Guide

For Chrome Web Store publication, your backend must use **HTTPS**. Here are your deployment options:

---

## Option 1: Railway (Recommended - Easy & Free Tier)

### Setup
1. Create account at https://railway.app
2. Connect your GitHub repository
3. Railway auto-detects Python/FastAPI

### Configuration
Add these environment variables in Railway dashboard:
```
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
DEFAULT_API_PROVIDER=openai
PORT=3000
```

### Procfile (create this file)
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Result
Your API will be available at: `https://your-app.up.railway.app`

---

## Option 2: Render (Free Tier Available)

### Setup
1. Create account at https://render.com
2. Create new "Web Service"
3. Connect GitHub repository
4. Select the `backend` directory as root

### Configuration
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables
Add in Render dashboard:
```
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
DEFAULT_API_PROVIDER=openai
```

### Result
Your API will be available at: `https://your-app.onrender.com`

---

## Option 3: Fly.io (Free Tier)

### Setup
```bash
# Install flyctl
brew install flyctl

# Login
fly auth login

# Launch from backend directory
cd backend
fly launch
```

### fly.toml
```toml
app = "sidebar-scholar-api"
primary_region = "sjc"

[build]

[http_service]
  internal_port = 3000
  force_https = true

[env]
  DEFAULT_API_PROVIDER = "openai"
```

### Secrets
```bash
fly secrets set OPENAI_API_KEY=sk-your-key-here
fly secrets set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## Option 4: Vercel (Serverless)

Create `vercel.json` in backend folder:
```json
{
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

---

## Update Extension Default URL

Once deployed, update the default backend URL in `frontend/background.js`:

```javascript
// Change from:
const backendUrl = settings.backendUrl || 'http://localhost:3000';

// To:
const backendUrl = settings.backendUrl || 'https://your-deployed-url.com';
```

---

## Security Considerations for Production

### 1. Restrict CORS Origins

Update `main.py` to restrict CORS:

```python
# Instead of allow_origins=["*"], use:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://YOUR_EXTENSION_ID",  # Your published extension
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

### 2. Rate Limiting (Recommended)

Add rate limiting to prevent abuse:

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/ask")
@limiter.limit("10/minute")
async def ask_question(request: Request, question: QuestionRequest):
    # ... existing code
```

### 3. Request Validation

The current Pydantic models provide good validation. Consider adding:
- Maximum context length validation
- Question length limits
- Input sanitization

---

## Testing Production Deployment

```bash
# Health check
curl https://your-deployed-url.com/health

# Test question endpoint
curl -X POST https://your-deployed-url.com/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this about?",
    "context": {
      "title": "Test",
      "url": "https://example.com",
      "text": "This is test content."
    }
  }'
```

---

## Architecture Options

### Option A: Shared Backend (You Host)
- You deploy and maintain the backend
- Users use your API endpoint
- You pay for API calls
- Pro: Simple for users
- Con: You bear the costs

### Option B: User-Provided Keys (Current Setup)
- Users provide their own API keys
- Keys sent with each request
- Pro: No cost to you
- Con: Slight setup friction for users

### Option C: Hybrid
- Offer both options
- Free tier with limits using your keys
- Power users can add their own keys

---

## Recommended Architecture for Chrome Store

For a public extension, I recommend:

1. **Deploy backend to Railway/Render** (free tier)
2. **Require users to provide their own API keys**
3. **Set sensible rate limits**
4. **Update default URL in extension**

This way:
- ✅ Works over HTTPS (required)
- ✅ No ongoing costs for you
- ✅ Users control their API usage
- ✅ Scalable



