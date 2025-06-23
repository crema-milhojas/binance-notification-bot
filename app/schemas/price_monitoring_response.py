from pydantic import BaseModel

class PriceMonitoringResponse(BaseModel):
    response_code: str
    message: str