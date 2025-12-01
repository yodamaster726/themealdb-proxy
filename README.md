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
