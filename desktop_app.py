import os
import sys
import threading
import time
import webview

# Add backend to path so imports work
if getattr(sys, 'frozen', False):
    # In frozen state, backend is in the root of the bundle or in a subdir
    # But we import backend.api.advanced_server
    # If we add sys._MEIPASS to path, we can import backend
    sys.path.append(sys._MEIPASS)
else:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the Flask app
# We use the absolute import which works because we added the root (or sys._MEIPASS) to sys.path
try:
    from backend.api.advanced_server import app
except ImportError:
    # Fallback if run from root without backend in path
    sys.path.append(os.path.dirname(__file__))
    from backend.api.advanced_server import app

def start_server():
    # Run Flask server
    # use_reloader=False is important for threading
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)

import webbrowser

class Api:
    def open_browser(self, url):
        webbrowser.open(url)

if __name__ == '__main__':
    # Start server in a separate thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Wait a bit for server to start
    time.sleep(2)
    
    # Create a native window
    api = Api()
    webview.create_window('Plastic Detection System', 'http://127.0.0.1:5001', js_api=api)
    
    # Start the GUI loop
    webview.start(debug=True)
