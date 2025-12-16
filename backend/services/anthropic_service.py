from anthropic import Anthropic
import os
import asyncio

async def call_anthropic(api_key: str, prompt: str) -> str:
    """
    Call Anthropic API with the given prompt.
    
    Args:
        api_key: Anthropic API key
        prompt: The prompt to send to the API
        
    Returns:
        The response text from Anthropic
        
    Raises:
        Exception: If API call fails
    """
    client = Anthropic(api_key=api_key)
    
    def _call_api():
        return client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            max_tokens=int(os.getenv("ANTHROPIC_MAX_TOKENS", "1000")),
            system="You are a helpful assistant that explains web content clearly and concisely. Provide accurate, well-structured answers based on the context provided.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    
    try:
        # Run the synchronous API call in a thread to avoid blocking the event loop
        # asyncio.to_thread() is available in Python 3.9+
        response = await asyncio.to_thread(_call_api)
        
        answer = response.content[0].text
        
        if not answer:
            raise Exception("No response content received from Anthropic")
        
        return answer
        
    except Exception as e:
        if hasattr(e, 'message'):
            raise Exception(f"Anthropic API error: {e.message}")
        raise Exception(f"Anthropic API error: {str(e)}")
