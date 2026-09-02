# ============================================
# IMPORTS - The tools we need
# ============================================
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ============================================
# CONFIGURATION - Setup the app
# ============================================

# Load environment variables from .env file
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Enable CORS (allows frontend to talk to backend)
CORS(app)

# Configure Gemini with your API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model
# Available models: 'gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-pro')

# ============================================
# ROUTES - The URLs your frontend will call
# ============================================

# Test route - check if backend is running
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Scolastic AI Backend with Gemini is running! 🎉',
        'status': 'online'
    })

# Health check - verify API key works
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # Test if API key works by listing models
        genai.list_models()
        return jsonify({
            'status': 'healthy',
            'api_key_valid': True,
            'model': 'gemini-pro'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'api_key_valid': False,
            'error': str(e)
        }), 503

# Main chat endpoint - where the AI magic happens
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Get the user's message from the frontend
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        
        # Get conversation history if provided (Gemini format)
        history = data.get('history', [])
        
        # Start a new chat session
        chat = model.start_chat(history=history)
        
        # Send the user's message and get response
        response = chat.send_message(user_message)
        
        # Extract the AI's reply
        ai_reply = response.text
        
        # Send reply back to frontend
        return jsonify({
            'reply': ai_reply,
            'status': 'success'
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'failed'
        }), 500

# Reset conversation - returns a welcome message
@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    return jsonify({
        'reply': 'Hello! I\'m your Scolastic AI assistant powered by Gemini. How can I help you with your studies today?',
        'status': 'success'
    })

# ============================================
# RUN THE SERVER
# ============================================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
