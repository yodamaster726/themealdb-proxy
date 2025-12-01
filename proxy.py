"""
Simple proxy server for TheMealDB API
Bypasses Cloudflare blocking by proxying requests through your home computer
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import ssl

# Configuration
PORT = 8080
THEMEALDB_BASE = "https://www.themealdb.com/api/json/v1/1"


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Build the target URL
        target_url = THEMEALDB_BASE + self.path
        
        try:
            # Create SSL context that doesn't verify (in case of cert issues)
            ctx = ssl.create_default_context()
            
            # Make request to TheMealDB with browser-like headers
            req = urllib.request.Request(target_url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            req.add_header('Accept', 'application/json, text/plain, */*')
            req.add_header('Accept-Language', 'en-US,en;q=0.9')
            req.add_header('Referer', 'https://www.themealdb.com/')
            req.add_header('Origin', 'https://www.themealdb.com')
            
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                data = response.read()
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Allow CORS
                self.end_headers()
                self.wfile.write(data)
                
        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Proxy error: {str(e)}".encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), ProxyHandler)
    print(f"Proxy server running on port {PORT}")
    print(f"Local URL: http://localhost:{PORT}/search.php?s=Arrabiata")
    print(f"External URL: http://73.179.46.16:{PORT}/search.php?s=Arrabiata")
    print("\nPress Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
