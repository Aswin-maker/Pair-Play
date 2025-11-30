from fastapi import APIRouter, Request
import time

router = APIRouter()

@router.get("/salesiq/verify")
async def salesiq_verify(request: Request):
    # Basic headers snapshot for debugging SalesIQ connectivity
    headers = {k: v for k, v in request.headers.items() if k.lower() in ["user-agent", "referer", "x-forwarded-for"]}
    return {
        "status": "ok",
        "timestamp": int(time.time()),
        "headers": headers,
        "hint": "If you see this from SalesIQ/Zobot request, backend is reachable."
    }

@router.post("/salesiq/echo")
async def salesiq_echo(payload: dict, request: Request):
    headers = {k: v for k, v in request.headers.items() if k.lower() in ["user-agent", "referer", "x-forwarded-for"]}
    return {
        "received": payload,
        "headers": headers,
        "timestamp": int(time.time())
    }
