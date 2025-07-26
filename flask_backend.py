from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

print("Current working directory:", os.getcwd())

app = Flask(__name__)
CORS(app)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it.")

client = Groq(api_key=groq_api_key)

def summarize_text_groq(text):
    """Summarizes the given text using the Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text. Provide concise, well-structured summaries that capture the main points and key information."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{text}"
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None

def translate_text_groq(text, target_language):
    """Translates the given text to the target language using the Groq API."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant that translates text to {target_language}. Provide accurate, natural translations that preserve the meaning and tone of the original text."
                },
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_language}:\n\n{text}"
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error during translation: {e}")
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/summarize", methods=["POST"])
def summarize_api():
    """API endpoint to summarize text"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data."}), 400
        
        text = data.get("text", "")
        if not text.strip():
            return jsonify({"error": "Input text is empty."}), 400
        
        if len(text.strip()) < 50:
            return jsonify({"error": "Text must be at least 50 characters long for meaningful summarization."}), 400
        
        summary = summarize_text_groq(text)
        
        if not summary:
            return jsonify({"error": "Summary could not be generated. Please try again."}), 500
        
        return jsonify({"summary": summary})
    
    except Exception as e:
        print(f"Error in summarize_api: {e}")
        return jsonify({"error": f"An error occurred during summarization: {str(e)}"}), 500

@app.route("/api/translate", methods=["POST"])
def translate_api():
    """API endpoint to translate text"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data."}), 400
        
        text = data.get("text", "")
        target_language = data.get("target_language", "")
        
        if not text.strip():
            return jsonify({"error": "Input text is empty."}), 400
        
        if not target_language:
            return jsonify({"error": "Target language is required."}), 400
        
        translation = translate_text_groq(text, target_language)
        
        if not translation:
            return jsonify({"error": "Translation could not be generated. Please try again."}), 500
        
        return jsonify({"translation": translation})
    
    except Exception as e:
        print(f"Error in translate_api: {e}")
        return jsonify({"error": f"An error occurred during translation: {str(e)}"}), 500

@app.route("/api/process", methods=["POST"])
def process_api():
    """Combined API endpoint to summarize and translate text in one call"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data."}), 400
        
        text = data.get("text", "")
        target_language = data.get("target_language", "")
        
        if not text.strip():
            return jsonify({"error": "Input text is empty."}), 400
        
        if not target_language:
            return jsonify({"error": "Target language is required."}), 400
        
        if len(text.strip()) < 50:
            return jsonify({"error": "Text must be at least 50 characters long for meaningful summarization."}), 400
        
        # First summarize
        summary = summarize_text_groq(text)
        if not summary:
            return jsonify({"error": "Summary could not be generated. Please try again."}), 500
        
        # Then translate the summary
        translation = translate_text_groq(summary, target_language)
        if not translation:
            return jsonify({
                "summary": summary,
                "translation": None,
                "error": "Translation could not be generated, but summary was successful."
            }), 206  # Partial content
        
        return jsonify({
            "summary": summary,
            "translation": translation
        })
    
    except Exception as e:
        print(f"Error in process_api: {e}")
        return jsonify({"error": f"An error occurred during processing: {str(e)}"}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Groq Text Processor API is running"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("Groq client instantiated and Flask app ready.")
    print("Available endpoints:")
    print("  GET  /              - Serve frontend")
    print("  POST /api/summarize - Summarize text")
    print("  POST /api/translate - Translate text")
    print("  POST /api/process   - Summarize and translate (combined)")
    print("  GET  /api/health    - Health check")
    
    app.run(debug=True, host="0.0.0.0", port=5000)