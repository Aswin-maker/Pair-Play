from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.routers import packages, leads, payments, ai

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Include Routers with authentication
app.include_router(packages.router, prefix="/packages", tags=["Packages"])
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(ai.router, prefix="/ai", tags=["AI & Feedback"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Chatbot Backend"}
