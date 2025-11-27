from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models.package import Package, PackageFilter
from app.services.sheets import sheets_service

router = APIRouter()

SHEET_NAME = "TravelPackages"
WORKSHEET_NAME = "Packages"

# Mock data for testing when Sheets is not connected
MOCK_PACKAGES = [
    {"package_name": "Bali Bliss", "location": "Bali", "days": 5, "budget": 800, "itinerary": "Day 1: Arrival...", "image_url": "http://example.com/bali.jpg"},
    {"package_name": "Paris Romance", "location": "Paris", "days": 4, "budget": 1200, "itinerary": "Day 1: Eiffel Tower...", "image_url": "http://example.com/paris.jpg"},
    {"package_name": "Kerala Nature", "location": "Kerala", "days": 6, "budget": 500, "itinerary": "Day 1: Houseboat...", "image_url": "http://example.com/kerala.jpg"},
]

def get_all_packages_from_source():
    try:
        data = sheets_service.get_all_records(SHEET_NAME, WORKSHEET_NAME)
        if not data:
            return MOCK_PACKAGES
        return data
    except:
        return MOCK_PACKAGES

@router.get("/", response_model=List[Package])
async def get_packages():
    """
    Fetch all travel packages.
    """
    return get_all_packages_from_source()

@router.post("/search", response_model=List[Package])
async def search_packages(filter_params: PackageFilter):
    """
    Search packages based on criteria.
    """
    all_packages = get_all_packages_from_source()
    filtered = []
    
    for pkg in all_packages:
        # Normalize data types from sheets (everything might be string)
        p_loc = str(pkg.get("location", "")).lower()
        p_budget = int(pkg.get("budget", 0))
        p_days = int(pkg.get("days", 0))
        
        match = True
        if filter_params.location and filter_params.location.lower() not in p_loc:
            match = False
        if filter_params.min_budget and p_budget < filter_params.min_budget:
            match = False
        if filter_params.max_budget and p_budget > filter_params.max_budget:
            match = False
        if filter_params.days and p_days != filter_params.days:
            match = False
            
        if match:
            filtered.append(pkg)
            
    return filtered
