from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime

from services.openai_service import call_openai
from services.anthropic_service import call_anthropic
from utils.prompt_builder import build_context_prompt

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Sidebar Scholar API",
    description="Backend API server for Sidebar Scholar Chrome extension",
    version="1.0.0"
)

# CORS middleware - allow Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your extension's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class Heading(BaseModel):
    level: str
    text: str

class PageContext(BaseModel):
    title: str
    url: str
    text: str
    headings: Optional[List[Heading]] = None
    timestamp: Optional[str] = None

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask")
    context: PageContext
    api_provider: Optional[str] = Field(None, description="API provider: 'openai' or 'anthropic'")
    api_key: Optional[str] = Field(None, description="API key (optional if server has default)")

class QuestionResponse(BaseModel):
    answer: str
    provider: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint for asking questions about web page content.
    
    - **question**: The question to ask about the page
    - **context**: Page context including title, URL, text content, and headings
    - **api_provider**: Optional API provider ('openai' or 'anthropic')
    - **api_key**: Optional API key (uses server default if not provided)
    """
    from datetime import datetime
    
    # Determine API provider
    provider = request.api_provider or os.getenv("DEFAULT_API_PROVIDER", "openai")
    api_key = request.api_key or get_default_api_key(provider)
    
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail=f"API key not provided. Please provide api_key in request or set {get_env_key_name(provider)} in environment variables."
        )
    
    # Build prompt with context
    prompt = build_context_prompt(request.context, request.question)
    
    # Call appropriate API
    try:
        if provider.lower() == "openai":
            answer = await call_openai(api_key, prompt)
        elif provider.lower() in ["anthropic", "claude"]:
            answer = await call_anthropic(api_key, prompt)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported API provider: {provider}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"API request failed: {str(e)}"
        )
    
    return {
        "answer": answer,
        "provider": provider,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def get_default_api_key(provider: str) -> Optional[str]:
    """Get default API key from environment variables"""
    env_key = get_env_key_name(provider)
    return os.getenv(env_key) if env_key else None

def get_env_key_name(provider: str) -> Optional[str]:
    """Get environment variable name for API key"""
    provider_lower = provider.lower()
    if provider_lower == "openai":
        return "OPENAI_API_KEY"
    elif provider_lower in ["anthropic", "claude"]:
        return "ANTHROPIC_API_KEY"
    return None

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)
