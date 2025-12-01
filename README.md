# TheMealDB Proxy

Simple proxy to bypass Cloudflare blocking for TheMealDB API.

## Prerequisites

### Install Node.js and npm (if not already installed)

**macOS:**
```bash
# Using Homebrew
brew install node

# Or download from https://nodejs.org/
```

**Windows:**
```bash
# Download installer from https://nodejs.org/
# Or using Chocolatey
choco install nodejs
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# Fedora
sudo dnf install nodejs npm
```

Verify installation:
```bash
node --version
npm --version
```

## Deploy to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

4. Your proxy will be live at a URL like:
```
https://your-project.vercel.app/api/proxy?s=Arrabiata
```

## Usage

Replace:
```
https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata
```

With:
```
https://your-project.vercel.app/api/proxy/search.php?s=Arrabiata
```

## Local Testing

```bash
python3 proxy.py
```

Then access: `http://localhost:8080/search.php?s=Arrabiata`

## How It Works

### Architecture

This proxy bypasses Cloudflare blocking by acting as an intermediary between your client and TheMealDB API.

```
School Network → Vercel Proxy → TheMealDB API
(Blocked)         (Allowed)      (Original API)
```

### Key Components

#### 1. `api/proxy.py` - Serverless Function
- **Purpose**: Handles incoming requests on Vercel's serverless platform
- **How it works**:
  - Receives requests at `/api/proxy?s=Arrabiata`
  - Adds browser-like headers (User-Agent, Referer, etc.) to mimic a real browser
  - Forwards the request to TheMealDB API
  - Returns the response with CORS headers enabled
- **Why it works**: Vercel's servers aren't blocked by Cloudflare, and the browser-like headers make the request appear legitimate

#### 2. `vercel.json` - Configuration
```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/proxy" }
  ]
}
```
- **Purpose**: Routes all `/api/*` requests to the `api/proxy.py` serverless function
- **How it works**: Vercel uses this file to understand how to handle incoming requests
- **Result**: Any path like `/api/proxy?s=Arrabiata` gets handled by the Python function

#### 3. `proxy.py` - Local Server (Optional)
- **Purpose**: Run the proxy locally for testing or if you prefer self-hosting
- **How it works**: Simple HTTP server on port 8080 that does the same thing as the Vercel function
- **Use case**: Testing locally before deploying, or running on your own computer

### Why Cloudflare Blocks the Original API

Cloudflare blocks requests that:
1. Come from certain IP ranges (like school networks)
2. Don't have proper browser headers
3. Make too many requests

### Why This Proxy Works

1. **Different IP**: Vercel's servers have different IPs that aren't blocked
2. **Browser Headers**: We add headers that make it look like a real browser request
3. **CORS Enabled**: Allows your web app to call the proxy from any domain
4. **Serverless**: No server to maintain, scales automatically

### Request Flow Example

```
1. Your App: fetch('https://themealdb-proxy.vercel.app/api/proxy?s=Arrabiata')
2. Vercel: Receives request, runs api/proxy.py
3. Proxy: Adds headers, calls https://www.themealdb.com/api/json/v1/1/search.php?s=Arrabiata
4. TheMealDB: Returns recipe data
5. Proxy: Forwards response back to your app
6. Your App: Receives the data
```
