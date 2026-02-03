# 📄 DocLens - Intelligent Document Analysis

DocLens is a powerful document analysis tool that uses Retrieval-Augmented Generation (RAG) to provide intelligent answers to questions about PDF documents. It combines FastAPI backend with a beautiful Streamlit frontend for an excellent user experience.

## 🚀 Features

- **PDF Processing**: Extract and analyze text from PDF documents via URL
- **RAG Technology**: Uses advanced AI models for context-aware responses
- **Multiple Questions**: Process multiple questions in a single request
- **Beautiful UI**: Modern Streamlit frontend with responsive design
- **Fast Processing**: Optimized for quick response times
- **Vector Search**: Semantic search using FAISS and sentence transformers
- **Groq Integration**: Powered by Groq's fast LLM inference

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │   Groq LLM      │
│   Frontend      │◄──►│   Backend       │◄──►│   API           │
│   (Port 8501)   │    │   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- GROQ API key (get it from [groq.com](https://groq.com))
- Internet connection for PDF downloads

## 🛠️ Installation

### Option 1: Quick Start (Windows)
1. Double-click `run_doclens.bat`
2. The script will automatically:
   - Create a virtual environment
   - Install dependencies
   - Start both backend and frontend

### Option 2: Manual Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd DocLens
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   API_KEY=your_api_key_here  # Optional
   ```

## 🚀 Running the Application



### Option 1: Run Services Separately

**Terminal 1 - Start Backend:**
```bash
python main.py
```

**Terminal 2 - Start Frontend:**
```bash
streamlit run streamlit_app.py
```

## 🌐 Access Points

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📱 Using the Frontend

1. **Open the Streamlit app** in your browser
2. **Enter PDF URL**: Paste the URL of a PDF document you want to analyze
3. **Add Questions**: Type your questions about the document
4. **Process**: Click "Process Document & Get Answers"
5. **View Results**: Get intelligent, context-aware answers

### Frontend Features

- **Modern UI**: Beautiful gradient design with responsive layout
- **Dynamic Questions**: Add/remove questions as needed
- **Real-time Validation**: URL and input validation with helpful feedback
- **Progress Indicators**: Loading states and status updates
- **Error Handling**: Clear error messages and troubleshooting tips
- **Responsive Design**: Works on desktop and mobile devices

## 🔧 Configuration

### Backend Settings
- **Port**: Default 8000 (configurable in `main.py`)
- **Host**: Default 0.0.0.0 (accessible from any IP)
- **Model**: Uses Groq's `llama-3.1-8b-instant` for fast responses

### Frontend Settings
- **Port**: Default 8501 (configurable in launcher)
- **Backend URL**: Configurable in sidebar
- **API Key**: Optional authentication support

## 📊 API Endpoints

### POST `/DocLens`
Process PDF documents and answer questions.

**Request Body:**
```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the coverage limit?",
    "What are the exclusions?"
  ]
}
```

**Response:**
```json
{
  "answers": [
    "The coverage limit is $100,000 per occurrence.",
    "Exclusions include pre-existing conditions and cosmetic procedures."
  ]
}
```

### GET `/health`
Health check endpoint for monitoring.


```

## 🔍 How It Works

1. **PDF Extraction**: Downloads PDF from URL and extracts text
2. **Text Chunking**: Breaks document into manageable chunks
3. **Vector Embeddings**: Creates semantic embeddings using sentence transformers
4. **FAISS Index**: Builds searchable vector index
5. **Query Processing**: Analyzes questions and finds relevant chunks
6. **RAG Generation**: Uses Groq LLM to generate context-aware answers

## 🚨 Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure FastAPI backend is running on port 8000
   - Check firewall settings
   - Verify GROQ_API_KEY in .env file

2. **PDF Processing Errors**
   - Ensure PDF URL is publicly accessible
   - Check if URL points to a valid PDF file
   - Verify internet connection

3. **Streamlit Issues**
   - Check if port 8501 is available
   - Restart Streamlit if UI becomes unresponsive
   - Clear browser cache if needed

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export LOG_LEVEL=DEBUG
```

## 📈 Performance Tips

- Use specific, focused questions for better results
- Limit questions to 20 per request for optimal performance
- Ensure PDF URLs are from fast, reliable sources
- Consider document size (larger PDFs take longer to process)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the beautiful frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance backend
- [Groq](https://groq.com/) for fast LLM inference
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [Sentence Transformers](https://www.sbert.net/) for text embeddings

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Open an issue on GitHub
4. Check the logs for detailed error information

---

**Happy Document Analysis! 📚✨**