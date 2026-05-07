# ============================================================================
# FILE: utils/llm_client.py
# ============================================================================

import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_gemini_response(prompt):
    # Initialize the Gemini model (using the free 'flash' model for speed)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        google_api_key=os.environ.get("GOOGLE_API_KEY")
    )
    response = llm.invoke(prompt)
    return response.content
get_chatgpt_response = get_gemini_response
#Adding this line for Aliasing
