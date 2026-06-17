import http.server
import socketserver
import os
import mimetypes

PORT = 8000

class TkbpyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Advanced Router for tkbpy:
    1. Automatically detects file types (CSS, JS, PNG, etc.)
    2. Maps root (/) to templates/index.html
    3. Handles the /static/ directory properly
    4. Disables caching for instant developer feedback
    """
    
    def do_GET(self):
        # 1. Route the Homepage (/)
        if self.path == '/':
            self.path = 'templates/index.html'
            return self.serve_file(self.path)

        # 2. Route Static Assets (/static/...)
        if self.path.startswith('/static/'):
            # Strip the leading slash to look in the local project folder
            requested_path = self.path.lstrip('/')
            return self.serve_file(requested_path)

        # 3. Fallback to standard behavior for other files
        return super().do_GET()

    def serve_file(self, file_path):
        """Helper to serve files with correct headers or show fallback"""
        if os.path.exists(file_path):
            # Identify the file (e.g., is it a .css or a .js file?)
            content_type, _ = mimetypes.guess_type(file_path)
            
            self.send_response(200)
            self.send_header('Content-type', content_type or 'text/plain')
            self.end_headers()
            
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.serve_fallback_error(file_path)

    def serve_fallback_error(self, path):
        """Standard tkbpy 404/Missing file screen"""
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        error_html = f"""
        <html>
        <body style="background:#f0f9ff; font-family:sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
            <div style="background:white; padding:3rem; border-radius:20px; text-align:center; border-top:10px solid #ef4444;">
                <h1 style="color:#b91c1c;">File Not Found</h1>
                <p style="color:#64748b;">tkbpy couldn't find: <strong>{path}</strong></p>
                <a href="/" style="color:#0ea5e9; text-decoration:none; font-weight:bold;">Back to Home</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode())

    def end_headers(self):
        """CRITICAL: Forces browser to NOT cache files during development"""
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def start():
    """Launch the tkbpy engine with address-reuse enabled"""
    # This prevents 'Address already in use' errors if you restart quickly
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("", PORT), TkbpyHandler) as httpd:
            print(f"\n📡 tkbpy Engine: http://localhost:{PORT}")
            print("🚀 Serving /templates and /static folders")
            print("💡 Press CTRL+C to stop safely\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
    except Exception as e:
        print(f"❌ Server Error: {e}")

if __name__ == "__main__":
    start()