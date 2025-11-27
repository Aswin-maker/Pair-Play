# 📘 TRAVEL CHATBOT BACKEND - COMPLETE PROJECT MANUAL

## 1. Project Overview
We have built a production-ready backend for a Travel & Tourism Chatbot. This backend serves as the "brain" of your chatbot, handling data storage, user verification, payments, and AI recommendations. It is built using **FastAPI**, a modern and high-performance Python framework.

## 2. System Architecture
The system consists of several integrated components:

*   **FastAPI Server**: The core application that processes all requests.
*   **Google Sheets**: Acts as your database.
    *   `Packages`: Stores travel packages (Bali, Paris, etc.).
    *   `Leads`: Stores customer inquiries.
    *   `Feedback`: Stores user reviews.
*   **Vonage (Nexmo)**: Handles sending OTP SMS for phone verification.
*   **Razorpay**: Generates payment links for booking.
*   **OpenAI / Gemini**: Provides intelligent travel recommendations.

## 3. Installation & Setup

### Prerequisites
*   Python 3.9 or higher installed.
*   A Google Cloud Service Account (for Sheets).
*   Accounts for Vonage, Razorpay, and OpenAI (optional for testing).

### Step-by-Step Installation
1.  **Clone the Project**:
    Download the code to your local machine.

2.  **Install Dependencies**:
    Open your terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```
    This installs FastAPI, Uvicorn, Vonage, and other required libraries.

3.  **Setup Google Sheets**:
    *   Create a sheet named **`TravelPackages`** at [sheets.google.com](https://sheets.google.com).
    *   Share it with your service account email (found in `google_credentials.json`) as **Editor**.
    *   Create 3 tabs: `Packages`, `Leads`, `Feedback`.

## 4. Configuration (.env)
The `.env` file holds your secret keys. **NEVER** share this file.

*   `GOOGLE_SHEETS_CREDENTIALS_JSON`: Path to your Google service account key file.
*   `VONAGE_API_KEY`: Your Vonage API Key (for SMS).
*   `VONAGE_API_SECRET`: Your Vonage Secret.
*   `VONAGE_SMS_NUMBER`: The phone number Vonage assigned to you.
*   `RAZORPAY_KEY_ID`: Your Razorpay Key ID.
*   `RAZORPAY_KEY_SECRET`: Your Razorpay Secret.
*   `OPENAI_API_KEY`: Your OpenAI Key (for AI features).
*   `SECRET_KEY`: A random string to secure your API tokens.

## 5. How It Works (Key Workflows)

### A. Browsing Packages
1.  User asks for packages.
2.  Backend reads the `Packages` sheet from Google Sheets.
3.  Returns the list of packages to the chatbot.

### B. Lead Generation & OTP
1.  User provides their phone number.
2.  Backend generates a 6-digit OTP.
3.  Backend sends SMS via **Vonage**.
4.  User enters OTP.
5.  Backend verifies it.
6.  If correct, the lead is saved to the `Leads` sheet.

### C. Booking & Payment
1.  User selects a package.
2.  Backend calls **Razorpay** to create a payment link.
3.  Link is sent to the user.

### D. AI Recommendations
1.  User asks "Where should I go for a honeymoon with $2000?".
2.  Backend sends this query to **OpenAI**.
3.  AI analyzes the request and suggests suitable packages.

## 6. Running the Server
To start the backend locally:
```bash
uvicorn app.main:app --reload
```
*   **Access the API**: Open `http://127.0.0.1:8000`
*   **Interactive Docs**: Open `http://127.0.0.1:8000/docs` (Swagger UI)

## 7. Testing
We have included several test scripts to verify everything is working:
*   `python check_health.py`: Checks all systems (Server, Sheets, Vonage, etc.).
*   `python test_vonage.py`: Specifically tests SMS sending.

## 8. Deployment (Going Live)
To make your backend accessible to the world (and Zoho SalesIQ), deploy it to **Render**:
1.  Push your code to GitHub.
2.  Create a new Web Service on Render.
3.  Connect your GitHub repo.
4.  Add your Environment Variables (from `.env`) to Render.
5.  Your API will be live at `https://your-app-name.onrender.com`.

---
**Status**: The project is currently fully functional locally. You just need to add your real API keys to the `.env` file to move from "Mock Mode" to "Live Mode".
