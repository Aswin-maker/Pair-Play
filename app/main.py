from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from app.routes.package_routes import router as package_router
from app.routes.auth_routes import router as auth_router
from app.routes.payment_routes import router as payment_router
from app.routes.ai_routes import router as ai_router
from app.routes.salesiq_routes import router as salesiq_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Travel Chatbot Backend", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
    )

app.include_router(package_router, prefix="/api", tags=["Packages"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(payment_router, prefix="/api", tags=["Payments"])
app.include_router(ai_router, prefix="/api", tags=["AI"])
app.include_router(salesiq_router, prefix="/api", tags=["SalesIQ"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Chatbot Backend! Visit /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
