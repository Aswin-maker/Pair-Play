# Quick Start Guide

## ✅ Your server is running successfully!

### Access the Application

1. **API Documentation (Swagger UI)**
   - Open your browser and go to: `http://localhost:8000/docs`
   - This interactive documentation lets you test all endpoints

2. **Root Endpoint**
   - `http://localhost:8000/` - Welcome message (no auth required)

### Testing the API

All API endpoints require Bearer Token authentication except the root endpoint.

**Authorization Header:**
```
Authorization: Bearer supersecretkey
```

### Available Endpoints

#### 📦 Packages
- `GET /packages/` - List all travel packages
- `POST /packages/search` - Search packages with filters

#### 👤 Leads & OTP
- `POST /leads/send-otp` - Send OTP to phone
- `POST /leads/verify-otp` - Verify OTP code
- `POST /leads/create-lead` - Create a new lead

#### 💳 Payments
- `POST /payments/generate-invoice` - Generate Razorpay payment link

#### 🤖 AI & Feedback
- `POST /ai/recommend` - Get AI travel recommendations
- `POST /ai/feedback` - Submit feedback

### Example: Testing with Swagger UI

1. Go to `http://localhost:8000/docs`
2. Click the **Authorize** button (🔒 icon at top right)
3. Enter: `supersecretkey`
4. Click **Authorize**
5. Now you can test any endpoint!

### Example: Testing with cURL

```bash
# Get all packages
curl -X GET "http://localhost:8000/packages/" \
  -H "Authorization: Bearer supersecretkey"

# Search packages
curl -X POST "http://localhost:8000/packages/search" \
  -H "Authorization: Bearer supersecretkey" \
  -H "Content-Type: application/json" \
  -d '{"location": "Bali", "max_budget": 1000}'

# Send OTP
curl -X POST "http://localhost:8000/leads/send-otp" \
  -H "Authorization: Bearer supersecretkey" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

### Mock Data

Since you haven't configured external services yet, the app uses mock data:
- **Packages**: Returns 3 sample packages (Bali, Paris, Kerala)
- **OTP**: Prints OTP to console (check terminal)
- **Payments**: Returns mock payment link
- **AI**: Returns generic recommendation

### Next Steps

1. **Configure Google Sheets**: Add your credentials to `.env`
2. **Add Real API Keys**: Update `.env` with Twilio, Razorpay, OpenAI keys
3. **Deploy to Render**: Follow `deployment.md`
4. **Integrate with Zoho**: Use `zoho_plugs.json` examples

### Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.
