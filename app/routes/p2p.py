from fastapi import APIRouter, Query
from typing import List
from ..schemas.arbitration_ustd_response import ArbitrationUstdResponse
from ..services.monitoring_service import MonitoringService
from ..services.swing_trading import SwingTrading

router = APIRouter()

@router.get("/arbitration-ustd", response_model=List[ArbitrationUstdResponse])
def arbitration_ustd(trans_amount: int = Query(20, description="Monto de la transacción")):
    monitoringService = MonitoringService()
    return monitoringService.arbitration_ustd(trans_amount)

@router.get("/swing-trading", response_model=List[ArbitrationUstdResponse])
def swing_trading():
    swing_trading = SwingTrading()
    return swing_trading.execute()
