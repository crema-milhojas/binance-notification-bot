from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from ..schemas.price_monitoring_response import PriceMonitoringResponse
from ..services.monitoring_service import MonitoringService

router = APIRouter()

@router.get("/ustd", response_model=List[PriceMonitoringResponse])
def price_monitoring(trans_amount: int = Query(100, description="Monto de la transacción")):
    monitoringService = MonitoringService()
    return monitoringService.consult_market_usdt(trans_amount)
