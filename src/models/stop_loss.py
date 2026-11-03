"""Modelos de dados (Pydantic) para o motor de Stop-Loss e Otimização."""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AdActionType(str, Enum):
    PAUSE = "PAUSE"                    # Pausa imediata (stop-loss ativado)
    SCALE = "SCALE"                    # Sugestão de aumento de orçamento
    KEEP = "KEEP"                      # Mantém rodando normalmente
    ALERT_FATIGUE = "ALERT_FATIGUE"    # Anúncio perdendo tração / CTR baixo


class ActionDecision(BaseModel):
    """Decisão tomada pelo sentinela para um anúncio específico."""
    ad_id: str
    ad_name: str
    action: AdActionType
    reason: str
    spend: float = 0.0
    purchases: int = 0
    cpa: Optional[float] = None
    roas: Optional[float] = None
    ctr: float = 0.0
    executed: bool = Field(
        default=False,
        description="True se a ação (ex: pausar) foi executada com sucesso na API da Meta"
    )


class StopLossCycleSummary(BaseModel):
    """Resumo de uma rodada de checagem do Sentinela."""
    timestamp: str
    ads_checked: int = 0
    ads_paused: int = 0
    ads_scaled: int = 0
    ads_kept: int = 0
    decisions: List[ActionDecision] = Field(default_factory=list)
