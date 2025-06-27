from fastapi import APIRouter, Query
from typing import List
from ..schemas.arbitration_ustd_response import ArbitrationUstdResponse
from ..services.monitoring_service import MonitoringService

router = APIRouter()

@router.get("/arbitration-ustd", response_model=List[ArbitrationUstdResponse])
def arbitration_ustd(trans_amount: int = Query(20, description="Monto de la transacción")):
    monitoringService = MonitoringService()
    return monitoringService.arbitration_ustd(trans_amount)
