from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from local_ai_engine import LocalAIEngine
import threading
import time

app = Flask(__name__)
CORS(app)

# Initialize the local AI engine
ai_engine = LocalAIEngine()

# Cache for responses to avoid repeated processing
response_cache = {}
MAX_CACHE_SIZE = 100
CACHE_EXPIRY = 3600  # 1 hour

@app.route('/')
def home():
    return render_template('index.html')

def process_with_timeout(user_input, timeout=10):  # Reduced timeout for Render
    """Process user input with a timeout"""
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = ai_engine.process(user_input)
        except Exception as e:
            exception[0] = str(e)
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    
    if thread.is_alive():
        return None, "Request timed out. Please try a simpler query."
    elif exception[0]:
        return None, f"Error: {exception[0]}"
    else:
        return result[0], None

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.get_json().get("message", "")
    
    # Check cache first
    cache_key = user_input.lower().strip()
    current_time = time.time()
    
    if cache_key in response_cache and current_time - response_cache[cache_key]["timestamp"] < CACHE_EXPIRY:
        return jsonify({"reply": response_cache[cache_key]["reply"]})
    
    try:
        # Process with timeout
        reply, error = process_with_timeout(user_input)
        
        if error:
            return jsonify({"reply": f"⚠️ {error}\n\n— Created by Aman Gupta"}), 500
        
        full_reply = reply + "\n\n— Created by Aman Gupta"
        
        # Cache the response
        if len(response_cache) >= MAX_CACHE_SIZE:
            # Remove oldest entry
            oldest_key = min(response_cache.keys(), key=lambda k: response_cache[k]["timestamp"])
            response_cache.pop(oldest_key)
        
        response_cache[cache_key] = {
            "reply": full_reply,
            "timestamp": current_time
        }
        
        return jsonify({"reply": full_reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}\n\n— Created by Aman Gupta"}), 500

@app.route('/teach', methods=['POST'])
def teach():
    data = request.get_json()
    pattern = data.get("pattern", "")
    response = data.get("response", "")
    
    if not pattern or not response:
        return jsonify({"status": "error", "message": "Both pattern and response are required"}), 400
    
    result = ai_engine.add_custom_response(pattern, response)
    if result:
        return jsonify({"status": "success", "message": f"I've learned to respond to '{pattern}' with '{response}'."})
    else:
        return jsonify({"status": "error", "message": "Failed to save the custom response"}), 500

@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    """Clear the response cache"""
    global response_cache
    response_cache = {}
    return jsonify({"status": "success", "message": "Cache cleared successfully"})

if __name__ == '__main__':
    app.run(debug=True)
