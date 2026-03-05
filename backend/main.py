from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy():
    """Privacy policy endpoint for Chrome Web Store"""
    privacy_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - Sidebar Scholar</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 { color: #6366f1; }
        h2 { color: #4f46e5; margin-top: 30px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #6366f1; color: white; }
    </style>
</head>
<body>
    <h1>Privacy Policy for Sidebar Scholar</h1>
    
    <p><strong>Last Updated:</strong> December 18, 2024</p>
    
    <h2>Overview</h2>
    <p>Sidebar Scholar is a browser extension that helps you understand web content using AI. This privacy policy explains what data we collect, how we use it, and your rights.</p>
    
    <h2>Data We Collect</h2>
    
    <h3>1. Page Content (Collected Temporarily)</h3>
    <p>When you ask a question, we collect:</p>
    <ul>
        <li><strong>Page title</strong> - The title of the current webpage</li>
        <li><strong>Page URL</strong> - The web address you're viewing</li>
        <li><strong>Page text content</strong> - Up to 8,000 characters of text from the page</li>
        <li><strong>Page headings</strong> - Up to 10 headings (H1-H6) for context</li>
    </ul>
    <p><strong>Why:</strong> This information provides context so the AI can answer your questions accurately.</p>
    <p><strong>Retention:</strong> This data is sent to the AI service in real-time and is NOT stored on our servers.</p>
    
    <h3>2. Your Questions</h3>
    <ul>
        <li>The questions you type and submit</li>
    </ul>
    <p><strong>Why:</strong> To get AI-generated answers for you.</p>
    <p><strong>Retention:</strong> Questions are processed in real-time and NOT stored on our servers.</p>
    
    <h3>3. Selected Text</h3>
    <ul>
        <li>Text you highlight on a webpage when using keyboard shortcuts</li>
    </ul>
    <p><strong>Why:</strong> To let you ask questions about specific content.</p>
    <p><strong>Retention:</strong> Stored temporarily in your browser's local storage until processed, then deleted.</p>
    
    <h3>4. User Settings (Stored Locally)</h3>
    <ul>
        <li>Your preferred AI provider (OpenAI or Anthropic)</li>
        <li>Backend server URL</li>
        <li>API key (if you provide your own)</li>
    </ul>
    <p><strong>Why:</strong> To remember your preferences.</p>
    <p><strong>Retention:</strong> Stored in your browser's local storage. Never sent to our servers.</p>
    
    <h2>Data We Do NOT Collect</h2>
    <ul>
        <li>❌ Personal identification information (name, email, etc.)</li>
        <li>❌ Browsing history beyond the current page</li>
        <li>❌ Cookies or tracking identifiers</li>
        <li>❌ Location data</li>
        <li>❌ Form data or passwords</li>
        <li>❌ Data from pages where you don't use the extension</li>
    </ul>
    
    <h2>How Your Data Is Used</h2>
    <ol>
        <li><strong>To Answer Your Questions</strong>: Page content and your question are sent to an AI service (OpenAI or Anthropic) to generate helpful responses.</li>
        <li><strong>To Improve Your Experience</strong>: Your settings are saved locally to remember your preferences.</li>
    </ol>
    
    <h2>Third-Party Services</h2>
    <p>When you use Sidebar Scholar, your data is processed by:</p>
    
    <h3>OpenAI (if selected as provider)</h3>
    <ul>
        <li>Privacy Policy: <a href="https://openai.com/privacy">https://openai.com/privacy</a></li>
        <li>Data is sent to OpenAI's API for processing</li>
        <li>Subject to OpenAI's data usage policies</li>
    </ul>
    
    <h3>Anthropic (if selected as provider)</h3>
    <ul>
        <li>Privacy Policy: <a href="https://www.anthropic.com/privacy">https://www.anthropic.com/privacy</a></li>
        <li>Data is sent to Anthropic's API for processing</li>
        <li>Subject to Anthropic's data usage policies</li>
    </ul>
    
    <p><strong>Note:</strong> We recommend reviewing these third-party privacy policies as they govern how your data is handled after it leaves the extension.</p>
    
    <h2>Data Security</h2>
    <ul>
        <li>✅ All network communications use HTTPS encryption</li>
        <li>✅ API keys are stored only in your browser's local storage</li>
        <li>✅ No user data is logged or stored on our backend servers</li>
        <li>✅ No analytics or tracking scripts</li>
    </ul>
    
    <h2>Your Rights and Choices</h2>
    
    <h3>Access Your Data</h3>
    <p>Your settings are stored in Chrome's local storage. You can view them at any time through the extension's settings panel.</p>
    
    <h3>Delete Your Data</h3>
    <ul>
        <li><strong>Clear local data</strong>: Uninstall the extension or clear browser data</li>
        <li><strong>Settings</strong>: Use the extension's settings to clear saved preferences</li>
        <li><strong>Third-party data</strong>: Contact OpenAI or Anthropic directly regarding data sent to their services</li>
    </ul>
    
    <h3>Opt-Out</h3>
    <p>You can stop using the extension at any time. Simply uninstall it to remove all locally stored data.</p>
    
    <h2>Children's Privacy</h2>
    <p>Sidebar Scholar is not intended for children under 13 years of age. We do not knowingly collect personal information from children.</p>
    
    <h2>Data Transfers</h2>
    <p>Your data may be transferred to and processed in the United States or other countries where OpenAI and Anthropic operate their services.</p>
    
    <h2>Changes to This Policy</h2>
    <p>We may update this privacy policy from time to time. We will notify users of any material changes by updating the "Last Updated" date at the top of this policy.</p>
    
    <h2>Open Source</h2>
    <p>Sidebar Scholar is open source. You can review exactly what data is collected by examining our source code.</p>
    
    <h2>Contact Us</h2>
    <p>If you have questions about this privacy policy or our data practices, please:</p>
    <ul>
        <li>Open an issue on our GitHub repository</li>
        <li>Email: [YOUR_EMAIL@example.com]</li>
    </ul>
    
    <h2>Summary</h2>
    <table>
        <tr>
            <th>Data Type</th>
            <th>Collected</th>
            <th>Stored</th>
            <th>Shared With</th>
        </tr>
        <tr>
            <td>Page content</td>
            <td>Yes (when you ask)</td>
            <td>No (real-time only)</td>
            <td>AI provider</td>
        </tr>
        <tr>
            <td>Questions</td>
            <td>Yes</td>
            <td>No</td>
            <td>AI provider</td>
        </tr>
        <tr>
            <td>Selected text</td>
            <td>Yes</td>
            <td>Temporarily (local)</td>
            <td>AI provider</td>
        </tr>
        <tr>
            <td>Settings</td>
            <td>Yes</td>
            <td>Yes (local only)</td>
            <td>No one</td>
        </tr>
        <tr>
            <td>Personal info</td>
            <td>No</td>
            <td>No</td>
            <td>No one</td>
        </tr>
    </table>
    
    <hr>
    <p><em>This privacy policy is effective as of December 18, 2024.</em></p>
</body>
</html>
    """
    return privacy_html

@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint for asking questions about web page content.
    
    - **question**: The question to ask about the page
    - **context**: Page context including title, URL, text content, and headings
    - **api_provider**: Optional API provider ('openai' or 'anthropic')
    - **api_key**: Optional API key (uses server default if not provided)
    """
    
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
