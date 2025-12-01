"""
Serverless function for Vercel to proxy TheMealDB API
"""

from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import ssl
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query string
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Remove /api/proxy from the path if present
        path = parsed_path.path.replace('/api/proxy', '')
        if not path:
            path = '/search.php'
        
        # Build the target URL
        target_url = f"https://www.themealdb.com/api/json/v1/1{path}"
        if parsed_path.query:
            target_url += f"?{parsed_path.query}"
        
        try:
            # Create SSL context
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
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                
        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_msg = json.dumps({"error": str(e)})
            self.wfile.write(error_msg.encode())
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
