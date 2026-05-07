# ============================================================================
# FILE: utils/llm_client.py
# ============================================================================

import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_response(prompt):
    """
    Initializes the Gemini model and processes the response to ensure 
    it returns a clean string, handling new multi-block content formats.
    """
    # 1. Initialize the model (using the free-tier compatible name)
    # Use 'gemini-flash-latest' as it's the most stable free alias.
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.7
    )

    # 2. Invoke the model
    response = llm.invoke(prompt)
    
    # 3. Handle different response formats
    # Gemini 3+ models often return a list of content blocks
    if isinstance(response.content, list):
        # Extract and join all text segments while ignoring 'extras' and 'signatures'
        text_parts = [
            block.get("text", "") 
            for block in response.content 
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "".join(text_parts).strip()
    
    # Fallback: If it's already a string, return it directly
    return response.content.strip()

# Aliasing to ensure compatibility with nodes.py and app.py
get_chatgpt_response = get_gemini_response

