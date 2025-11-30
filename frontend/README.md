# Travel Chatbot Frontend (React + Vite)

This React frontend integrates the existing FastAPI backend with the Zoho SalesIQ widget and provides a simple package browsing UI.

## Features
- Embeds Zoho SalesIQ chat widget (SalesIQ script included in `index.html`).
- Displays packages from `/api/packages`.
- Allows lead creation (`/api/create-lead`) when a user clicks "Enquire".
- Bridges custom functions (`window.TravelBot.recommend`, `window.TravelBot.createLead`) for Deluge / SalesIQ scripts to call.
- Provides AI recommendation hook via `/api/ai-recommend`.

## Project Structure
```
frontend/
  index.html            # Contains Zoho SalesIQ widget script tag
  src/
    main.jsx            # React entry
    App.jsx             # Main application component
    components/
      Packages.jsx      # Package grid UI
      ChatWidget.jsx    # Widget status + bridge
    api.js              # Backend API client wrappers
  .env.example          # Example env file for backend URL
```

## Running Locally
Make sure backend is running (FastAPI on `http://127.0.0.1:8000`).

```powershell
cd frontend
npm install
npm run dev
```
Open the printed local URL (default `http://localhost:5173`).

## Environment Variables
Create a `.env` file in `frontend/` based on `.env.example`:
```
VITE_BACKEND_URL=https://your-production-domain
```

## Zoho SalesIQ Integration
`index.html` loads the SalesIQ widget. Once ready, `ChatWidget` detects SalesIQ and sets up `window.TravelBot` functions. In Deluge / SalesIQ custom scripts, you can call:

```javascript
// Example from a SalesIQ custom function
$sendToVisitor("Fetching recommendations...");
var recommendation = await window.TravelBot.recommend("Family trip to Paris under 1000 USD");
$sendToVisitor(recommendation);
```

(Adjust to SalesIQ's scripting environment — asynchronous patterns may differ; if `await` unsupported, expose callback-based versions.)

## Deluge Script Flow
1. Visitor enters query in chat.
2. SalesIQ triggers Deluge function.
3. Deluge (server-side) can either:
   - Call backend REST endpoint directly (preferred for secure operations), OR
   - Use front-end bridge (less secure, mainly for demo UX).
4. Response returned to visitor in chat.

Recommended: Keep sensitive operations (payments, authentication) strictly via backend REST.

## Extending
- Add search form: Use `searchPackages(filters)` from `api.js`.
- Show AI suggestions: Call `aiRecommend(text)` when user triggers a prompt.
- Replace mock lead data with form-bound user inputs.

## Production Build
```powershell
cd frontend
npm run build
```
Generates `dist/` folder. Serve it via a static host (Railway static service or CDN). Ensure `VITE_BACKEND_URL` points to the deployed FastAPI domain.

## Security Notes
- Do NOT expose secrets in the frontend `.env` (only public URLs).
- Keep service account JSON ONLY in backend env vars, never here.

## Next Steps
- Implement auth flow once backend has token endpoints.
- Add form for user details before lead creation.
- Add loading states and toasts for user feedback.
