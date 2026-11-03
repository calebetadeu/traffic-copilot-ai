"""Modelos de dados (Pydantic) para integração com a Meta Marketing API."""

from typing import List, Optional
from pydantic import BaseModel, Field


class AdInsightMetric(BaseModel):
    """Métricas consolidadas de um anúncio específico."""
    ad_id: str
    ad_name: str
    spend: float = Field(default=0.0, description="Valor gasto em R$")
    impressions: int = Field(default=0)
    clicks: int = Field(default=0)
    ctr: float = Field(default=0.0, description="Taxa de clique em %")
    cpc: float = Field(default=0.0, description="Custo por clique em R$")
    purchases: int = Field(default=0, description="Quantidade de compras registradas pelo Pixel")
    cpa: Optional[float] = Field(default=None, description="Custo por aquisição (venda) em R$")
    roas: Optional[float] = Field(default=None, description="Retorno sobre investimento em anúncios")


class WinningCreativeSummary(BaseModel):
    """Resumo de um criativo campeão de vendas extraído na auditoria."""
    ad_id: str
    ad_name: str
    headline: Optional[str] = None
    primary_text: Optional[str] = None
    media_url: Optional[str] = None
    purchases: int = 0
    roas: float = 0.0
    cpa: float = 0.0


class AccountAuditReport(BaseModel):
    """Relatório da Auditoria de DNA gerado pela varredura da conta."""
    ad_account_id: str
    period: str = "last_90d"
    total_spend: float = 0.0
    total_purchases: int = 0
    average_roas: float = 0.0
    average_cpa: float = 0.0
    winning_creatives: List[WinningCreativeSummary] = Field(default_factory=list)
    key_findings: List[str] = Field(
        default_factory=list,
        description="Descobertas automáticas sobre públicos, ganchos e formatos que mais venderam"
    )


class CampaignCreationRequest(BaseModel):
    """Parâmetros de criação segura de campanha."""
    name: str
    objective: str = "OUTCOME_SALES"  # Otimizado para vendas no e-commerce
    status: str = "PAUSED"            # Segurança: sempre PAUSED por padrão
    daily_budget_reais: float = Field(
        default=30.00,
        description="Orçamento diário em Reais (será convertido para centavos para a Meta)"
    )
