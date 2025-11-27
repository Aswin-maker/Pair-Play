from pydantic import BaseModel
from typing import Optional, List

class PackageBase(BaseModel):
    package_name: str
    location: str
    days: int
    budget: int
    itinerary: str
    image_url: Optional[str] = None

class Package(PackageBase):
    pass

class PackageFilter(BaseModel):
    location: Optional[str] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    days: Optional[int] = None
