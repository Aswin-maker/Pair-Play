# Deployment Guide (Railway)

## Prerequisites
- A GitHub repository containing this code.
- A Railway account (https://railway.app).
- API Keys for Google Sheets, Vonage, Razorpay, and OpenAI.

## Steps

1. **Push to GitHub**
   - Initialize a git repo: `git init`
   - Add files: `git add .`
   - Commit: `git commit -m "Initial commit"`
   - Push to your GitHub repository.

2. **Create Project on Railway**
   - Go to Railway Dashboard -> New Project -> Deploy from GitHub repo.
   - Connect your GitHub repository.

3. **Configure Settings**
    - **Environment Variables**:
       - `PYTHON_VERSION`: `3.10` (or use the included `runtime.txt`)
       - `SPREADSHEET_ID`: Your Google Sheet ID
       - `GOOGLE_CREDENTIALS_JSON_STRING`: Paste your Service Account JSON (as a single line)
       - `VONAGE_API_KEY`: (Your Vonage API Key)
       - `VONAGE_API_SECRET`: (Your Vonage API Secret)
       - `VONAGE_SMS_NUMBER`: (Your Vonage SMS Number)
       - `RAZORPAY_KEY_ID`: (Your Key ID)
       - `RAZORPAY_KEY_SECRET`: (Your Secret)
       - `GEMINI_API_KEY`: (Optional; for AI recommendations)
       - `SECRET_KEY`: (Your chosen secret key)
       - `ALGORITHM`: `HS256`
       - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`

   - **Build Command**:
     ```bash
     pip install -r requirements.txt
     ```

   - **Start Command**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

4. **Deploy**
   - Turn OFF "Auto Deploy" if you want to verify settings first.
   - Click "Deploy".
   - Once live, your URL will be `https://<project-name>.railway.app`.

## Testing
- Health: `https://<project-name>.railway.app/health`
- Swagger: `https://<project-name>.railway.app/docs`
- Packages: `https://<project-name>.railway.app/api/packages`

## Connect Zoho / Frontend
- Update `backend_base_url` in `zoho_scripts/*.ds` to your Railway URL.
- For the frontend, set `VITE_BACKEND_URL` to the Railway URL during build or in `.env.production`.

---

## Backend-Only Deployment (Ignore Frontend)

If you want to deploy ONLY the FastAPI backend and keep the React frontend local or for a separate host:

1. Use the existing root repository; Railway will ignore the `frontend/` folder because we never build or start it.
2. Do NOT run any Node build step in Railway. Leave build command as Python only:
   ```bash
   pip install -r requirements.txt
   ```
3. Start command stays:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Required Environment Variables (minimum):
   - `SPREADSHEET_ID`
   - `GOOGLE_CREDENTIALS_JSON_STRING` (service account JSON single line)
   - `SECRET_KEY`
   - `ALGORITHM` (HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` (30)
   - Optional integrations: `GEMINI_API_KEY`, `VONAGE_API_KEY`, `VONAGE_API_SECRET`, `VONAGE_SMS_NUMBER`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`
5. After deploy, verify:
   - Health: `/health`
   - Packages: `/api/packages`
   - AI: `/api/ai-recommend` (POST `{"text":"beach"}`)
6. Frontend local dev: keep running `npm run dev` locally and set `VITE_BACKEND_URL` to the Railway URL so local React points to remote backend.
7. SalesIQ scripts: replace `backend_base_url` with the Railway URL; no frontend hosting needed.

### Excluding Frontend (Optional Advanced)
If you prefer to reduce build context size, you can create a separate repo with only:
```
app/
requirements.txt
Procfile
runtime.txt
deployment.md
```
But this is not required—Railway will not execute the React code unless you add Node commands.

### Optional: Add a Preview Environment
Create a second Railway environment (e.g., staging) and duplicate env vars. Use that URL in a staging SalesIQ bot before promoting to production.

---
