from fastapi import FastAPI
from app.routes import package_routes, auth_routes, payment_routes, ai_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Travel Chatbot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(package_routes.router, prefix="/api", tags=["Packages"])
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(payment_routes.router, prefix="/api", tags=["Payments"])
app.include_router(ai_routes.router, prefix="/api", tags=["AI"])
