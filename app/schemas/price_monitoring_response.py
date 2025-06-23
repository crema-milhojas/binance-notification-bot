from pydantic import BaseModel
from typing import Any 

class PriceMonitoringResponse(BaseModel):
    response_code: str
    message: str
    data: Any