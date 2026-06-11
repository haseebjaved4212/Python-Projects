import os
import requests
from flask import Flask, request, jsonify, render_template
import system_commands

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), 'templates')
)

# Ensure the screenshots directory exists inside static
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(os.path.join(STATIC_DIR, "screenshots"), exist_ok=True)

@app.route('/')
def home():
    """Renders the main dashboard index.html."""
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def handle_command():
    """Processes spoken or typed commands from the frontend."""
    data = request.json or {}
    command = data.get('command', '').strip()
    gemini_key = data.get('gemini_key', '').strip()
    
    if not command:
        return jsonify({"type": "error", "message": "No command received."}), 400
        
    print(f"Received command: {command}")
    
    # 1. Try to process as a local system/automation command
    response = system_commands.process_command(command, STATIC_DIR)
    
    if response:
        return jsonify(response)
        
    # 2. If it's not a local command, route to Gemini if key is provided
    if gemini_key:
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{
                    "parts": [{
                        "text": (
                            "You are a helpful, conversational desktop voice assistant. "
                            "Keep your response concise and conversational (1 to 3 sentences max) so it can be spoken easily. "
                            "Avoid markdown tags like bolding (**) or bullet points, as they sound awkward when read aloud. "
                            f"The user says: {command}"
                        )
                    }]
                }]
            }
            res = requests.post(gemini_url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
            print(f"Gemini API response status code: {res.status_code}")
            print(f"Gemini API response body: {res.text}")
            
            if res.status_code == 200:
                res_data = res.json()
                # Extract response text
                text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                return jsonify({"type": "chat", "message": text})
            else:
                return jsonify({
                    "type": "error", 
                    "message": f"Gemini API returned status code {res.status_code}. Details: {res.text}"
                })
        except Exception as e:
            return jsonify({
                "type": "error", 
                "message": f"Error connecting to Gemini: {str(e)}"
            })
            
    # 3. If no key is provided, return a friendly prompt
    return jsonify({
        "type": "fallback",
        "message": (
            f"I recognized '{command}', but I couldn't run it as a local command. "
            "To chat with me or ask complex questions, please enter your Gemini API key in the settings panel. "
            "Alternatively, you can say 'Search Google for [topic]' or 'Search YouTube for [topic]'."
        )
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
