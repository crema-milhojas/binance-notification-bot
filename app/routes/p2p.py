from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.price_monitoring_response import PriceMonitoringResponse
from ..services.monitoring_service import MonitoringService

router = APIRouter()

@router.get("/", response_model=List[PriceMonitoringResponse])
def price_monitoring():
    return MonitoringService.consult_market()
