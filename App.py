# ============================================================================
# FILE: app.py (Main Streamlit Application)
# ============================================================================
import streamlit as st
from graph import create_document_graph, create_qa_graph
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Smart Document Analyzer",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'document_processed' not in st.session_state:
    st.session_state.document_processed = False
if 'graph_state' not in st.session_state:
    st.session_state.graph_state = None

st.title("📄 Smart Document Analyzer with RAG")
st.markdown("Upload PDF documents and ask questions using AI-powered retrieval")
st.markdown("Built with ❤️ by C3 Group")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF document to analyze"
    )
    
    if uploaded_file:
        if not st.session_state.document_processed:
            with st.spinner("🔄 Processing document..."):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Create and run the document processing graph
                graph = create_document_graph()
                
                # Process document
                result = graph.invoke({
                    "file_path": temp_path,
                    "filename": uploaded_file.name,
                    "extracted_text": "",
                    "chunks": [],
                    "analysis": {},
                    "vector_store": None,
                    "summary": "",
                    "question": "",
                    "answer": "",
                    "context": []
                })
                
                # Clean up temp file
                os.remove(temp_path)
                
                # Store in session state
                st.session_state.graph_state = result
                st.session_state.document_processed = True
                
            st.success("✅ Document processed successfully!")
        
        # Show document info
        if st.session_state.graph_state:
            st.markdown("---")
            st.markdown("### 📊 Document Info")
            st.write(f"**Filename:** {uploaded_file.name}")
            analysis = st.session_state.graph_state.get('analysis', {})
            st.write(f"**Chunks:** {analysis.get('num_chunks', 'N/A')}")
            st.write(f"**Total Words:** {analysis.get('total_words', 'N/A')}")

# Main content area
col1, col2 = st.columns([1, 1])

# Left column - Summary
with col1:
    st.header("📋 Document Summary")
    if st.session_state.graph_state:
        summary = st.session_state.graph_state.get('summary', '')
        st.markdown(summary)
        
        # Show analysis details
        with st.expander("🔍 Detailed Analysis"):
            analysis = st.session_state.graph_state.get('analysis', {})
            st.json(analysis)
    else:
        st.info("👈 Upload a document to see its summary")

# Right column - Chat Interface
with col2:
    st.header("💬 Ask Questions")
    
    if st.session_state.document_processed:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources for assistant messages
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}:**")
                            st.text(source[:200] + "...")
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your document..."):
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get answer using RAG
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Use QA-only graph to avoid re-running document processing
                    qa_graph = create_qa_graph()
                    
                    # Run QA with existing vector store
                    qa_result = qa_graph.invoke({
                        "question": prompt,
                        "vector_store": st.session_state.graph_state['vector_store'],
                        "answer": "",
                        "context": []
                    })
                    
                    answer = qa_result['answer']
                    sources = qa_result['context']
                    
                    st.markdown(answer)
                    
                    # Show sources
                    if sources:
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**Source {i}:**")
                                st.text(source[:200] + "...")
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            
            st.rerun()
    else:
        st.info("👈 Upload a document to start asking questions")
        
        # Show example questions
        st.markdown("### 💡 Example Questions:")
        st.markdown("""
        - What are the main topics discussed in this document?
        - Can you summarize the key findings?
        - What methodology was used?
        - Who are the authors or key people mentioned?
        """)

