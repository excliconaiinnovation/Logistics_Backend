from pydantic import BaseModel
from datetime import date
from typing import Optional

class MaintenanceResponse(BaseModel):
    id: int
    vehicle_id: int
    maintenance_type: Optional[str]
    issue: Optional[str]
    cost: Optional[float]
    service_date: Optional[date]

    model_config = {
        "from_attributes": True  # ✅ Pydantic V2 way
    }