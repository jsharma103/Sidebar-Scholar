def build_context_prompt(context, question: str) -> str:
    """
    Build a prompt with page context and user question.
    
    Args:
        context: PageContext object with page information
        question: User's question
        
    Returns:
        Formatted prompt string
    """
    if not context or not hasattr(context, 'text') or not context.text:
        return f"You are a helpful assistant. Answer the following question clearly and concisely: {question}"
    
    title = context.title if hasattr(context, 'title') else 'Untitled Page'
    url = context.url if hasattr(context, 'url') else 'Unknown URL'
    text = context.text if hasattr(context, 'text') else ''
    
    prompt = f"""You are a helpful assistant that helps users understand web pages. The user is currently viewing a webpage with the following context:

Title: {title}
URL: {url}

Page Content:
{text}"""
    
    # Add headings if available
    if hasattr(context, 'headings') and context.headings:
        prompt += "\n\nPage Structure:\n"
        for heading in context.headings:
            level = heading.get('level', '') if isinstance(heading, dict) else getattr(heading, 'level', '')
            text_content = heading.get('text', '') if isinstance(heading, dict) else getattr(heading, 'text', '')
            prompt += f"{level}: {text_content}\n"
    
    prompt += f"""

User's Question: {question}

Please provide a helpful, clear answer based on the page content. If the question is about understanding something on the page, explain it in simple terms. If asked about jargon or technical terms, provide clear definitions. Be concise but thorough. Format your response in a way that's easy to read."""
    
    return prompt



