from pydantic import BaseModel
from typing import Optional

class ServiceRequest(BaseModel):
    titulo: str
    subtitulo: str
    descricao: str
    status: str = "Em andamento"
    user_id: Optional[str]