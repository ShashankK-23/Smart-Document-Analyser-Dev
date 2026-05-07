
# ============================================================================
# FILE: nodes.py (Individual Processing Nodes)
# ============================================================================
from typing import Dict, Any
from utils.pdf_processor import extract_text_from_pdf
from utils.text_chunker import chunk_text
from utils.vector_store import create_vector_store, retrieve_relevant_chunks
from utils.llm_client import get_gemini_response
from utils.prompts import (
    ANALYSIS_PROMPT,
    SUMMARY_PROMPT,
    QA_PROMPT
)

def extract_text_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Extract text from PDF document"""
    file_path = state["file_path"]
    extracted_text = extract_text_from_pdf(file_path)
    
    return {
        **state,
        "extracted_text": extracted_text
    }

def chunk_text_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Split text into chunks for embedding"""
    extracted_text = state["extracted_text"]
    chunks = chunk_text(extracted_text)
    
    return {
        **state,
        "chunks": chunks
    }

def create_embeddings_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Create vector embeddings and store in vector database"""
    chunks = state["chunks"]
    vector_store = create_vector_store(chunks)
    
    return {
        **state,
        "vector_store": vector_store
    }

def analyze_document_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze document structure and content"""
    extracted_text = state["extracted_text"]
    chunks = state["chunks"]
    
    # Basic analysis
    analysis = {
        "num_chunks": len(chunks),
        "total_words": len(extracted_text.split()),
        "total_chars": len(extracted_text)
    }
    
    # Use LLM for deeper analysis
    analysis_prompt = ANALYSIS_PROMPT.format(text=extracted_text[:3000])
    analysis_result = get_gemini_response(analysis_prompt)
    analysis["llm_analysis"] = analysis_result
    
    return {
        **state,
        "analysis": analysis
    }

def summarize_document_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate document summary"""
    extracted_text = state["extracted_text"]
    
    # Use first portion of text for summary
    summary_prompt = SUMMARY_PROMPT.format(text=extracted_text[:4000])
    summary = get_gemini_response(summary_prompt)
    
    return {
        **state,
        "summary": summary
    }

def qa_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Answer questions using RAG"""
    question = state["question"]
    vector_store = state["vector_store"]
    
    # Retrieve relevant chunks (RAG retrieval)
    relevant_chunks = retrieve_relevant_chunks(vector_store, question, top_k=3)
    
    # Create context from retrieved chunks
    context = "\n\n".join(relevant_chunks)
    
    # Generate answer using LLM (RAG generation)
    qa_prompt = QA_PROMPT.format(context=context, question=question)
    answer = get_gemini_response(qa_prompt)
    
    return {
        **state,
        "answer": answer,
        "context": relevant_chunks
    }

