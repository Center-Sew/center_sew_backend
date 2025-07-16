from typing import Optional
from app.core.config import settings   # BACKEND_URL já definido no settings

def build_foto_url(nome: str | None) -> Optional[str]:
    if not nome:
        return None
    return f"{settings.BACKEND_URL}/imagens/perfil/{nome}"