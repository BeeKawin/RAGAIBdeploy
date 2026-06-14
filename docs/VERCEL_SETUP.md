# Vercel Frontend Setup

Use this when configuring the Vercel demo website.

## Project Settings

Create a new Vercel project from the same GitHub repository.

Set:

```text
Root Directory: ragaib/demo
Framework Preset: Other
Build Command: leave blank
Output Directory: leave blank
Install Command: leave blank
```

The demo is a static site. Vercel serves:

```text
index.html
styles.css
app.js
config.js
vercel.json
```

## API URL Connection

Recommended for first testing:

1. Leave `demo/config.js` blank:
   ```js
   window.RAGAIB_API_BASE_URL = "";
   ```
2. Open the deployed Vercel site.
3. Paste your Railway backend URL into the page's **API Base URL** field.
4. The browser saves it in `localStorage`.

After the Railway URL is stable, you can optionally edit `demo/config.js`:

```js
window.RAGAIB_API_BASE_URL = "https://your-railway-api-url";
```

Then commit and redeploy the frontend.

## CORS Reminder

After Vercel gives you a production URL, go back to Railway and set:

```env
ALLOWED_ORIGINS=https://your-vercel-site.vercel.app
OPENROUTER_SITE_URL=https://your-vercel-site.vercel.app
```

For a temporary Vercel preview URL, add it as a comma-separated origin:

```env
ALLOWED_ORIGINS=https://your-vercel-site.vercel.app,https://your-preview-site.vercel.app
```

## What You Should Not Put In Vercel

Do not add:

```text
OPENROUTER_API_KEY
vector_db/
Python backend env vars
Railway secrets
```

Vercel hosts only the static frontend. Secrets stay in Railway.

## Final Test

After Railway and Vercel are both live, run from `ragaib/`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_deployment.ps1 `
  -ApiBaseUrl "https://your-railway-api-url" `
  -FrontendOrigin "https://your-vercel-site.vercel.app"
```

Then test the page manually:

```text
Question: What is Newton's second law?
Subject: physics
Grade: M4
Language: EN
Answer type: homework-help
```

The page should show the RAG answer, baseline answer, retrieved chunks, scores, and winner.
