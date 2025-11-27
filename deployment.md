# Deployment Guide (Render)

## Prerequisites
- A GitHub repository containing this code.
- A Render account (https://render.com).
- API Keys for Google Sheets, Vonage, Razorpay, and OpenAI.

## Steps

1. **Push to GitHub**
   - Initialize a git repo: `git init`
   - Add files: `git add .`
   - Commit: `git commit -m "Initial commit"`
   - Push to your GitHub repository.

2. **Create Web Service on Render**
   - Go to Render Dashboard -> New -> Web Service.
   - Connect your GitHub repository.
   - **Name**: `travel-chatbot-backend`
   - **Region**: Choose closest to you.
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

3. **Environment Variables**
   - Scroll down to "Environment Variables" and add the following:
     - `PYTHON_VERSION`: `3.9.0`
     - `GOOGLE_SHEETS_CREDENTIALS_JSON`: (Paste your JSON content here)
     - `VONAGE_API_KEY`: (Your Vonage API Key)
     - `VONAGE_API_SECRET`: (Your Vonage API Secret)
     - `VONAGE_SMS_NUMBER`: (Your Vonage SMS Number)
     - `RAZORPAY_KEY_ID`: (Your Key ID)
     - `RAZORPAY_KEY_SECRET`: (Your Secret)
     - `OPENAI_API_KEY`: (Your Key)
     - `SECRET_KEY`: (Your chosen secret key for Bearer Auth)

4. **Deploy**
   - Click "Create Web Service".
   - Wait for the build to finish.
   - Once live, your URL will be `https://travel-chatbot-backend.onrender.com`.

## Testing
- Use the URL in Zoho SalesIQ Plugs.
- Ensure you add the `Authorization: Bearer <YOUR_SECRET_KEY>` header in Zoho.
