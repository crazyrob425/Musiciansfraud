"""
Desktop GUI wrapper for Musicians Fraud AI Song Generator
Uses Eel to wrap the Flask web interface in a desktop window
"""

import eel
import sys
import os
from threading import Thread
from app import app as flask_app

# Initialize Eel with the templates folder
eel.init('templates')

def start_flask():
    """Start Flask server in background thread"""
    flask_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

@eel.expose
def close_application():
    """Properly close the application"""
    sys.exit(0)

if __name__ == '__main__':
    # Start Flask in background thread
    flask_thread = Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Start Eel GUI
    eel.start('index.html', 
              mode='chrome',
              host='localhost',
              port=8080,
              size=(1200, 800),
              position=(100, 100))
