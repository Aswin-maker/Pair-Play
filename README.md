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
See [deployment.md](deployment.md) for instructions on deploying to Render.
