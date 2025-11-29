from fastapi import APIRouter, HTTPException
from app.services.google_sheets import read_values, append_row
from app.models import PackageRequest, LeadCreate, FeedbackRequest

router = APIRouter()

@router.get("/packages")
async def get_packages():
    rows = await read_values("Packages!A2:F")
    # Expect header in A1:F1; map rows to dicts
    packages = []
    for r in rows:
        packages.append({
            "package_name": r[0] if len(r) > 0 else "",
            "location": r[1] if len(r) > 1 else "",
            "days": int(r[2]) if len(r) > 2 and r[2].isdigit() else None,
            "budget": int(r[3]) if len(r) > 3 and r[3].isdigit() else None,
            "itinerary": r[4] if len(r) > 4 else "",
            "image_url": r[5] if len(r) > 5 else ""
        })
    return {"packages": packages}

@router.post("/search-packages")
async def search_packages(req: PackageRequest):
    rows = await read_values("Packages!A2:F")
    results = []
    for r in rows:
        try:
            pkg = {
                "package_name": r[0] if len(r) > 0 else "",
                "location": r[1] if len(r) > 1 else "",
                "days": int(r[2]) if len(r) > 2 and r[2].isdigit() else 0,
                "budget": int(r[3]) if len(r) > 3 and r[3].isdigit() else 0,
                "itinerary": r[4] if len(r) > 4 else "",
                "image_url": r[5] if len(r) > 5 else ""
            }
        except Exception:
            continue
        # apply filters
        if req.location and req.location.lower() not in pkg["location"].lower():
            continue
        if req.days and pkg["days"] != 0 and req.days != pkg["days"]:
            continue
        if req.min_budget and pkg["budget"] < req.min_budget:
            continue
        if req.max_budget and pkg["budget"] > req.max_budget:
            continue
        results.append(pkg)
    return {"count": len(results), "results": results}

@router.post("/create-lead")
async def create_lead(lead: LeadCreate):
    # append to Leads sheet
    await append_row("Leads!A2:E", [lead.name, lead.email, lead.phone, lead.package_name, "new"])
    return {"status": "lead_created"}
