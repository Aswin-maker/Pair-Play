# Travel & Tourism Chatbot Backend

A production-ready FastAPI backend for a Travel & Tourism Chatbot, designed to integrate with Zoho SalesIQ.

## Features
- **Package Management**: Fetch and filter travel packages from Google Sheets.
- **Lead Generation**: Capture leads and save them to Google Sheets.
- **OTP Verification**: Verify phone numbers using Vonage (Nexmo) or Mock mode.
- **Payments**: Generate payment links using Razorpay.
- **AI Recommendations**: Get travel suggestions using OpenAI or Gemini.
- **Feedback**: Collect user feedback.

## Architecture

```ascii
Zoho SalesIQ Bot  -->  FastAPI Backend (Render)
                            |
                            |--> Google Sheets (Database)
                            |    (Packages, Leads, Feedback)
                            |
                            |--> Vonage (OTP Service)
                            |
                            |--> Razorpay (Payment Gateway)
                            |
                            |--> OpenAI/Gemini (AI Engine)
```

## Setup

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Fill in your API keys (Google Sheets, Vonage, Razorpay, OpenAI).
4. **Run Locally**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Access docs at `http://localhost:8000/docs`.

## API Endpoints

- `GET /packages`: List all packages.
- `POST /packages/search`: Filter packages.
- `POST /leads/send-otp`: Send OTP.
- `POST /leads/verify-otp`: Verify OTP.
- `POST /leads/create-lead`: Create a new lead.
- `POST /payments/generate-invoice`: Create a payment link.
- `POST /ai/recommend`: Get AI recommendations.
- `POST /ai/feedback`: Submit feedback.

## Deployment

### Railway Deployment Configuration

**Start command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Build command:**
```bash
pip install -r requirements.txt
```

**Python Version:**
Set `PYTHON_VERSION` to `3.10` in Environment Variables.

**Environment Variables:**
Ensure you add all variables from `.env.example` to your Railway project settings.

### Deployment Steps

1. **Initialize Git and Push:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to [Railway](https://railway.app/)
   - Click **New Project** -> **Deploy from GitHub repo**
   - Select your repository
   - **Set Environment Variables:**
     - Click on "Variables"
     - Add all keys from `.env.example`
     - Add `PYTHON_VERSION=3.10`
   - **Set Commands:**
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Settings:**
     - Turn OFF "Auto Deploy" initially (recommended).
   - Deploy!

3. **Test Deployment:**
   - Visit `https://<your-project>.railway.app/health` to check status.
   - Visit `https://<your-project>.railway.app/docs` for API documentation.
