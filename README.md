# agentic-rag-system
Agentic AI-Powered Query Service


**Technologies Used**
- FastAPI: For building the web API.
- LangChain: For integrating language models and managing embeddings.
- Boto3: AWS SDK for Python, used for AWS services.
- Sarvam API: For speech-to-text and text-to-speech functionalities.
- PyMuPDF (fitz): For PDF document handling and text extraction.
- FAISS: For efficient similarity search and clustering of text embeddings.


**Installation**
- Clone the repository

- Change the directory:
```bash
cd rag_system
```

- Install the required packages:
```bash  
pip install -r requirements.txt
```

- Set up environment variables for API keys:
```bash
export SARVAM_API_KEY='your_sarvam_api_key'
```

- Run the setup.py file:
```bash  
python setup.py
```

- Run the gradio_interface.py file to get the URL for the first interface and try the first endpoint:
```bash  
python frontend/gradio_interface.py
```

- Then run the gradio_agent_interface.py to get the URL of the second interface and try the second endpoint:
```bash  
python frontend/gradio_agent_interface.py
```

**API Endpoints**
- POST /query
- POST /query_agent

**Features**
- Text and Voice Input: Supports user queries via text and audio uploads (WAV/MP3).
- Speech Recognition: Converts spoken language to text using Sarvam's STT API.
- Text-to-Speech: Generates audio responses from text using Sarvam's TTS API.
- Document Parsing: Extracts text from PDF documents using AWS Textract and PyMuPDF.
- Contextual Responses: Utilizes language models to provide informative and concise answers.
- Custom Tools: Includes tools for calculations and Wikipedia search integrated with LangChain.

Future Improvements : Microphone feature is in development.
