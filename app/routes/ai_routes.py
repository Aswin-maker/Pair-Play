from fastapi import APIRouter
from app.services.ai_service import recommend_packages
from app.services.google_sheets import read_values

router = APIRouter()

@router.post("/ai-recommend")
async def ai_recommend(query: dict):
    # get package list
    rows = await read_values("Packages!A2:F")
    packages = []
    for r in rows:
        packages.append({
            "package_name": r[0] if len(r) > 0 else "",
            "location": r[1] if len(r) > 1 else "",
            "days": int(r[2]) if len(r) > 2 and r[2].isdigit() else 0,
            "budget": int(r[3]) if len(r) > 3 and r[3].isdigit() else 0,
        })
    answer = await recommend_packages(query.get("text",""), packages)
    return {"recommendation": answer}
