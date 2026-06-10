import threading
import time
import webbrowser
from app import app

def start_browser():
    """Waits for the server to start, then opens the browser."""
    time.sleep(1.5)
    print("Launching Voice Assistant UI in browser...")
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    print("Starting Voice Assistant Server...")
    # Start a background thread to launch the browser
    browser_thread = threading.Thread(target=start_browser, daemon=True)
    browser_thread.start()
    
    # Run the Flask app (use_reloader=False prevents double-execution in debug mode)
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
