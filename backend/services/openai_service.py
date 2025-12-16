from openai import AsyncOpenAI
import os

async def call_openai(api_key: str, prompt: str) -> str:
    """
    Call OpenAI API with the given prompt.
    
    Args:
        api_key: OpenAI API key
        prompt: The prompt to send to the API
        
    Returns:
        The response text from OpenAI
        
    Raises:
        Exception: If API call fails
    """
    try:
        # Simple client initialization - let OpenAI SDK handle defaults
        client = AsyncOpenAI(api_key=api_key)
        
        response = await client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that explains web content clearly and concisely. Provide accurate, well-structured answers based on the context provided."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        )
        
        answer = response.choices[0].message.content
        
        if not answer:
            raise Exception("No response content received from OpenAI")
        
        return answer
        
    except Exception as e:
        error_msg = str(e)
        # Provide more helpful error messages
        if hasattr(e, 'message'):
            raise Exception(f"OpenAI API error: {e.message}")
        raise Exception(f"OpenAI API error: {error_msg}")
