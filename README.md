# TheMealDB Proxy

Simple proxy to bypass Cloudflare blocking for TheMealDB API.

## Deploy to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Follow the prompts and your proxy will be live at a URL like:
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
