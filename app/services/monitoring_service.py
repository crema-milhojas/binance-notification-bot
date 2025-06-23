from typing import List
from ..schemas.price_monitoring_response import PriceMonitoringResponse

class MonitoringService:
     @staticmethod
     def consult_market() -> List[PriceMonitoringResponse]:
          return [
               PriceMonitoringResponse(response_code="00", message="OK")
          ]
          