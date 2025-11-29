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
     - `PYTHON_VERSION`: `3.10`
     - `GOOGLE_SHEETS_CREDENTIALS_JSON`: (Paste your JSON content here)
     - `VONAGE_API_KEY`: (Your Vonage API Key)
     - `VONAGE_API_SECRET`: (Your Vonage API Secret)
     - `VONAGE_SMS_NUMBER`: (Your Vonage SMS Number)
     - `RAZORPAY_KEY_ID`: (Your Key ID)
     - `RAZORPAY_KEY_SECRET`: (Your Secret)
     - `OPENAI_API_KEY`: (Your Key)
     - `GEMINI_API_KEY`: (Your Key)
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
- Visit `https://<project-name>.railway.app/docs` to see the Swagger UI.
- Use the URL in Zoho SalesIQ Plugs.
