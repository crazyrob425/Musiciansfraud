"""
Desktop GUI Application Launcher
Wraps the Flask web app in a native desktop window using PyWebView
"""

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

# Try to import webview, but provide fallback
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("PyWebView not available. Install with: pip install pywebview")

from app import app as flask_app

# Get the application directory
APP_DIR = Path(__file__).parent


class DesktopApp:
    """Desktop wrapper for the AI Song Generator"""
    
    def __init__(self):
        self.flask_thread = None
        self.port = 5000
        self.host = '127.0.0.1'
        self.url = f'http://{self.host}:{self.port}'
        
    def start_flask(self):
        """Start Flask server in a separate thread"""
        flask_app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
    
    def wait_for_server(self, timeout=10):
        """Wait for Flask server to start"""
        import socket
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.host, self.port))
                sock.close()
                
                if result == 0:
                    return True
            except Exception:
                pass
            
            time.sleep(0.1)
        
        return False
    
    def run_with_webview(self):
        """Run the app with PyWebView (native window)"""
        print("🎵 AI Song Generator - Desktop Mode")
        print("=" * 50)
        print("Starting application...")
        
        # Start Flask in background thread
        self.flask_thread = threading.Thread(target=self.start_flask, daemon=True)
        self.flask_thread.start()
        
        # Wait for server to be ready
        print("Initializing server...")
        if not self.wait_for_server():
            print("❌ Error: Could not start Flask server")
            return
        
        print(f"✅ Server ready at {self.url}")
        print("Opening desktop window...")
        
        # Create native window
        window = webview.create_window(
            title='AI Song Generator - Musicians Fraud',
            url=self.url,
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            min_size=(800, 600)
        )
        
        # Start the GUI event loop
        webview.start()
        
        print("Application closed.")
    
    def run_with_browser(self):
        """Run the app with default web browser (fallback)"""
        print("🎵 AI Song Generator - Browser Mode")
        print("=" * 50)
        print("Starting application...")
        
        # Start Flask in background thread
        self.flask_thread = threading.Thread(target=self.start_flask, daemon=True)
        self.flask_thread.start()
        
        # Wait for server to be ready
        print("Initializing server...")
        if not self.wait_for_server():
            print("❌ Error: Could not start Flask server")
            return
        
        print(f"✅ Server ready at {self.url}")
        print("Opening in web browser...")
        
        # Open in default browser
        webbrowser.open(self.url)
        
        print("\n" + "=" * 50)
        print(f"Application is running at: {self.url}")
        print("Press Ctrl+C to stop the server")
        print("=" * 50 + "\n")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
    
    def run(self):
        """Run the application (with webview if available, browser otherwise)"""
        if WEBVIEW_AVAILABLE:
            try:
                self.run_with_webview()
            except Exception as e:
                print(f"\n⚠️  Could not start in desktop mode: {e}")
                print("Falling back to browser mode...\n")
                self.run_with_browser()
        else:
            print("\n💡 TIP: For a better desktop experience, install PyWebView:")
            print("   pip install pywebview\n")
            self.run_with_browser()


def main():
    """Main entry point for desktop application"""
    # Ensure we're in the right directory
    os.chdir(APP_DIR)
    
    # Create output directory if it doesn't exist
    output_dir = APP_DIR / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Create .env file if it doesn't exist
    env_file = APP_DIR / '.env'
    env_example = APP_DIR / '.env.example'
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
    
    # Run the desktop app
    app = DesktopApp()
    app.run()


if __name__ == '__main__':
    main()
