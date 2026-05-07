# 📄 Smart Document Analyser

A powerful AI-powered document analysis tool built with Streamlit and LangChain that enables intelligent question-answering over your documents using Retrieval-Augmented Generation (RAG).

## 🌟 Features

- **format Support**: Upload and analyze PDF
- **Intelligent Q&A**: Ask questions about your documents and get accurate, context-aware answers
- **Vector Search**: Uses ChromaDB for efficient semantic search across document content
- **Chat Interface**: Intuitive conversational interface for document interaction
- **Session Management**: Maintains conversation history throughout your session
- **Fast & Efficient**: Optimized with caching for quick response times

## 🚀 Demo

<img width="1876" height="912" alt="image" src="https://github.com/user-attachments/assets/458fc67f-97d9-4837-b989-652865868515" />




## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **LLM Framework**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embeddings / HuggingFace Embeddings
- **Language Model**: OpenAI GPT / Anthropic Claude / Open-source LLMs
- **Text Processing**: LangChain Text Splitters
- **Python**: 3.12+

## 📋 Prerequisites

- Python 3.12 or higher
- OpenAI API key (or alternative LLM provider)
- pip or uv package manager

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Ashivu3112/smart-document-analyser.git
cd smart-document-analyser
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Using uv:
```bash
uv pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
# Or for other providers:
# ANTHROPIC_API_KEY=your_anthropic_key
# HUGGINGFACE_API_KEY=your_hf_key
```

## 🎯 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### How to Use

1. **Upload Documents**: Click on the file uploader and select your PDF, DOCX, or TXT files
2. **Wait for Processing**: The system will chunk and index your documents
3. **Ask Questions**: Type your questions in the chat input
4. **Get Answers**: Receive AI-generated answers based on your document content
5. **Follow-up**: Ask follow-up questions to dive deeper into your documents

## 📁 Project Structure

```
smart-document-analyser/
│
├── app.py                      # Main Streamlit application
├── graph.py                    # Graph and State schema setup
├── nodes.py                    # Node workflow setup
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                 # Git ignore file
|
├── utils/
│   ├── pdf_processor.py       # PDF loading and processing
│   ├── vector_store.py        # ChromaDB vector store management
|   ├── prompts.py             # Prompt templates for llms
|   ├── llm_client.py          # Openai or anthropic client
│   └── text_chunker.py        # Text splitter
│
├── data/                       # Temporary document storage (gitignored)
└── README.md                   # This file
```

## 🔧 Configuration

### Customizing Chunk Size

In `utils/pdf_processor.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Adjust chunk size
    chunk_overlap=200,    # Adjust overlap
)
```

### Changing the LLM Model

In `utils/llm_client.py`:

```python
llm = ChatOpenAI(
    model="gpt-4",           # Change model
    temperature=0.7,         # Adjust creativity
)
```

### Vector Store Settings

In `utils/vector_store.py`:

```python
collection = client.create_collection(
    name="document_collection",
    metadata={"hnsw:space": "cosine"}  # or "l2", "ip"
)
```

## 👤 Author

**Ashish Biswal**

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) for the amazing framework
- [Streamlit](https://streamlit.io/) for the intuitive UI framework
- [ChromaDB](https://www.trychroma.com/) for the vector database
- OpenAI/Anthropic for the powerful language models

## 📊 Performance

- Average query response time: ~2-3 seconds
- Supports documents up to 200MB
- Handles multiple concurrent users
- Efficient caching for repeated queries

## 🐛 Known Issues

- Large documents (>100 pages) may take longer to process
- PDF files with complex formatting may have extraction issues
- Maximum file size limited to 200MB

## 🔮 Future Enhancements

- [ ] Support for more document formats (Docs, Excel, PowerPoint)
- [ ] Multi-document comparison
- [ ] Document summarization feature
- [ ] Export conversation history
- [ ] User authentication and document persistence
- [ ] Advanced filtering and search options
- [ ] Integration with cloud storage (Google Drive, Dropbox)

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the [Issues](https://github.com/Ashivu3112/smart-document-analyser/issues) page
2. Create a new issue with detailed information
3. Contact me directly at your.email@example.com

---

⭐ If you find this project useful, please consider giving it a star!

**Built with ❤️ by Ashish Biswal**
