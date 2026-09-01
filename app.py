from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Test route
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Scolastic AI Backend is running! 🎉',
        'status': 'online'
    })

# Main chat endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        
        # Get conversation history if provided
        messages = data.get('history', [])
        messages.append({
            'role': 'user',
            'content': user_message
        })
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        ai_reply = response.choices[0].message.content
        
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

# Reset endpoint
@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    return jsonify({
        'reply': 'Hello! I\'m your Scolastic AI assistant. How can I help you with your studies today?',
        'status': 'success'
    })

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        openai.Model.list()
        return jsonify({
            'status': 'healthy',
            'api_key_valid': True
        })
    except:
        return jsonify({
            'status': 'unhealthy',
            'api_key_valid': False
        }), 503

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )