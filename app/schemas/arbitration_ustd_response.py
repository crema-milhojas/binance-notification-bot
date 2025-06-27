from pydantic import BaseModel
from typing import Any

class ArbitrationUstdResponse(BaseModel):
    response_code: str
    message: str
    data: Any