from pydantic import BaseModel
from typing import Optional, Dict

class MercadoPagoNotificationData(BaseModel):
    id: Optional[str]  # ID do recurso (ex: payment ID)

class MercadoPagoNotification(BaseModel):
    action: Optional[str]
    api_version: Optional[str]
    data: Optional[MercadoPagoNotificationData]
    date_created: Optional[str]
    id: Optional[int]
    live_mode: Optional[bool]
    type: Optional[str]
    user_id: Optional[str]