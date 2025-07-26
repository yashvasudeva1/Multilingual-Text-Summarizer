# Multilingual Text Summarizer

A modern web application that uses the **Groq API** to summarize text and translate it into multiple languages.  
Built with a **Flask backend** and **JavaScript frontend**.

## Features
- **Smart Text Summarization**: Generate concise summaries of long texts using AI  
- **Multi-language Translation**: Translate summaries into 16 different languages  
- **Modern UI**: Clean, responsive interface with real-time feedback  
- **Real-time Processing**: Live character counter and input validation  
- **Easy Copy**: One-click copying of results to clipboard  

## Supported Languages
Arabic, Chinese, Danish, Dutch, English, French, German, Hindi, Italian, Japanese, Korean, Norwegian, Portuguese, Russian, Spanish, Swedish

## Prerequisites
- Python 3.7+
- Groq API key

## Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-text-processor

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file in the project root:
# .env
GROQ_API_KEY=your_groq_api_key_here

# Run backend using following command :
python flask_backend.py

