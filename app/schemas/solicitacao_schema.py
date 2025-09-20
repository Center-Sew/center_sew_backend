from __future__ import annotations

from datetime import datetime, date, time, timezone
from typing import Optional, List, Union
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_validator

from app.models.perfil_desejado import PerfilDesejado
from app.schemas.base import BaseModelWithStrObjectId


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

_TZ_BR = ZoneInfo("America/Sao_Paulo")
_TZ_UTC = ZoneInfo("UTC")


def _to_utc_end_of_day_br(d: date) -> datetime:
    """Converte uma data (sem hora) para 23:59:59 no fuso de Brasília e retorna em UTC."""
    local_dt = datetime.combine(d, time(23, 59, 59), tzinfo=_TZ_BR)
    return local_dt.astimezone(_TZ_UTC)


def _normalize_to_utc(value: Union[str, date, datetime]) -> datetime:
    """
    Converte str/date/datetime para datetime timezone-aware em UTC.
    - str: aceita 'YYYY-MM-DD' ou ISO 8601 (com/sem timezone).
    - date: assume fim do dia em Brasília (23:59:59).
    - datetime: se vier sem tz, assume Brasília; depois converte para UTC.
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return _to_utc_end_of_day_br(value)

    if isinstance(value, str):
        # Tenta ISO first; fromisoformat aceita 'YYYY-MM-DD' e ISO padrão
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Formato inválido para data_prevista_entrega")
        if parsed.tzinfo is None:
            # Se veio só 'YYYY-MM-DD', parsed vira datetime sem tz à meia-noite → usar fim do dia BR
            if len(value) == 10:  # 'YYYY-MM-DD'
                return _to_utc_end_of_day_br(parsed.date())
            parsed = parsed.replace(tzinfo=_TZ_BR)
        return parsed.astimezone(_TZ_UTC)

    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=_TZ_BR)
        return value.astimezone(_TZ_UTC)

    raise ValueError("Tipo inválido para data_prevista_entrega")


# ──────────────────────────────────────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────────────────────────────────────

class SolicitationCreate(BaseModel):
    titulo: str
    descricao: str
    perfil_desejado: PerfilDesejado

    # ⬇️ Campo novo: aceita str/date/datetime; será normalizado para UTC
    data_prevista_entrega: Optional[Union[str, date, datetime]] = None

    @field_validator("data_prevista_entrega")
    @classmethod
    def _valida_normaliza_data_prevista(cls, v):
        if v is None:
            return None
        return _normalize_to_utc(v)


class UsuarioSlim(BaseModel):
    id: str
    nome: str
    email: str
    segmento: Optional[str] = None
    localizacao: Optional[dict] = None
    foto: Optional[str] = None


class SolicitationModel(BaseModelWithStrObjectId, SolicitationCreate):
    usuario_id: str
    usuario: Optional[UsuarioSlim] = None  # opcional na resposta

    status: str = Field(default="aberta")
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Herdado do create já normalizado: Optional[datetime] (em UTC)
    # data_prevista_entrega: Optional[datetime]

    interessados: int = 0
    imagens: List[str] = Field(default_factory=list)  # evita default mutável []