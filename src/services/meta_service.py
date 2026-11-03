"""Serviço de integração com a Meta Marketing API (Graph API v21.0).

Inclui:
- Auditoria de DNA (extração de criativos campeões do histórico da conta);
- Criação segura de campanhas, conjuntos e anúncios com status PAUSED;
- Travas rígidas contra estouro de orçamento diário;
- Gatilho de Stop-Loss para pausa imediata de anúncios com baixa performance.
"""

from typing import Optional, List, Dict, Any
import httpx

from src.core.config import settings
from src.models.meta import (
    AccountAuditReport,
    WinningCreativeSummary,
    AdInsightMetric
)


class BudgetExceededSecurityError(Exception):
    """Exceção levantada quando um orçamento viola as travas físicas de segurança."""
    pass


class MetaMarketingService:
    def __init__(
        self,
        access_token: Optional[str] = None,
        ad_account_id: Optional[str] = None,
        graph_version: Optional[str] = None
    ):
        self.access_token = access_token or settings.META_ACCESS_TOKEN
        raw_account = ad_account_id or settings.META_AD_ACCOUNT_ID or ""
        
        # Garante prefixo 'act_' exigido pela Graph API
        if raw_account and not raw_account.startswith("act_"):
            self.ad_account_id = f"act_{raw_account}"
        else:
            self.ad_account_id = raw_account

        self.graph_version = graph_version or settings.META_GRAPH_VERSION
        self.base_url = f"https://graph.facebook.com/{self.graph_version}"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    # =========================================================================
    # 1. AUDITORIA DE DNA E EXTRAÇÃO DE MÉTRICAS HISTÓRICAS
    # =========================================================================

    def get_account_insights(self, date_preset: str = "last_90d") -> Dict[str, Any]:
        """Puxa os dados consolidados da conta para o período especificado."""
        if not self.access_token or not self.ad_account_id:
            raise ValueError("META_ACCESS_TOKEN e META_AD_ACCOUNT_ID são obrigatórios.")

        url = f"{self.base_url}/{self.ad_account_id}/insights"
        params = {
            "fields": "spend,impressions,clicks,cpc,ctr,actions,action_values,purchase_roas",
            "date_preset": date_preset
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [{}])[0] if data.get("data") else {}

    def audit_winning_creatives(
        self,
        limit: int = 5,
        date_preset: str = "last_90d"
    ) -> AccountAuditReport:
        """
        Executa a 'Engenharia Reversa' na conta da Meta:
        1. Identifica os anúncios que geraram mais vendas com menor CPA e maior ROAS;
        2. Extrai os textos, títulos e mídias desses anúncios vencedores;
        3. Monta o Dossiê Inicial do negócio para alimentar o Gemini.
        """
        if not self.access_token or not self.ad_account_id:
            raise ValueError("Credenciais da Meta não configuradas.")

        url = f"{self.base_url}/{self.ad_account_id}/insights"
        params = {
            "level": "ad",
            "fields": "ad_id,ad_name,spend,actions,action_values,purchase_roas,ctr,cpc",
            "date_preset": date_preset,
            "limit": 100
        }

        with httpx.Client(timeout=30.0) as client:
            res = client.get(url, headers=self._get_headers(), params=params)
            res.raise_for_status()
            insights = res.json().get("data", [])

        # Processar métricas de compras e ROAS por anúncio
        ranked_ads = []
        total_spend = 0.0
        total_purchases = 0

        for row in insights:
            ad_id = row.get("ad_id")
            spend = float(row.get("spend", 0.0))
            total_spend += spend

            # Extrair compras das ações
            purchases = 0
            for action in row.get("actions", []):
                if action.get("action_type") in ("purchase", "omni_purchase"):
                    purchases += int(action.get("value", 0))

            total_purchases += purchases

            # Extrair ROAS
            roas = 0.0
            roas_list = row.get("purchase_roas", [])
            if roas_list:
                roas = float(roas_list[0].get("value", 0.0))

            cpa = (spend / purchases) if purchases > 0 else 0.0

            if purchases > 0 or roas > 0:
                ranked_ads.append({
                    "ad_id": ad_id,
                    "ad_name": row.get("ad_name", "Anúncio"),
                    "purchases": purchases,
                    "spend": spend,
                    "roas": roas,
                    "cpa": cpa
                })

        # Ordenar por mais compras e maior ROAS
        ranked_ads.sort(key=lambda x: (x["purchases"], x["roas"]), reverse=True)
        top_ads = ranked_ads[:limit]

        # Puxar os criativos dos anúncios top
        winning_summaries = []
        with httpx.Client(timeout=30.0) as client:
            for item in top_ads:
                ad_id = item["ad_id"]
                ad_url = f"{self.base_url}/{ad_id}"
                ad_res = client.get(
                    ad_url,
                    headers=self._get_headers(),
                    params={"fields": "creative{title,body,image_url,thumbnail_url}"}
                )
                
                headline = None
                primary_text = None
                media_url = None

                if ad_res.status_code == 200:
                    creative = ad_res.json().get("creative", {})
                    headline = creative.get("title")
                    primary_text = creative.get("body")
                    media_url = creative.get("image_url") or creative.get("thumbnail_url")

                winning_summaries.append(
                    WinningCreativeSummary(
                        ad_id=ad_id,
                        ad_name=item["ad_name"],
                        headline=headline,
                        primary_text=primary_text,
                        media_url=media_url,
                        purchases=item["purchases"],
                        roas=item["roas"],
                        cpa=round(item["cpa"], 2)
                    )
                )

        avg_roas = (
            sum(w.roas for w in winning_summaries) / len(winning_summaries)
            if winning_summaries else 0.0
        )
        avg_cpa = (total_spend / total_purchases) if total_purchases > 0 else 0.0

        return AccountAuditReport(
            ad_account_id=self.ad_account_id,
            period=date_preset,
            total_spend=round(total_spend, 2),
            total_purchases=total_purchases,
            average_roas=round(avg_roas, 2),
            average_cpa=round(avg_cpa, 2),
            winning_creatives=winning_summaries,
            key_findings=[
                f"Conta analisada no período '{date_preset}'. Total investido: R$ {total_spend:.2f}.",
                f"Identificados {len(winning_summaries)} anúncios campeões históricos com vendas consistentes.",
                f"CPA médio histórico de compras: R$ {avg_cpa:.2f}."
            ]
        )

    # =========================================================================
    # 2. CRIAÇÃO SEGURA DE CAMPANHAS E CONJUNTOS (MODO RASCUNHO)
    # =========================================================================

    def create_campaign(
        self,
        name: str,
        objective: str = "OUTCOME_SALES",
        status: str = "PAUSED"
    ) -> Dict[str, Any]:
        """Cria uma nova campanha na Meta com status sempre PAUSED por segurança."""
        url = f"{self.base_url}/{self.ad_account_id}/campaigns"
        payload = {
            "name": name,
            "objective": objective,
            "status": status,
            "special_ad_categories": ["NONE"]
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()

    def create_adset(
        self,
        campaign_id: str,
        name: str,
        daily_budget_reais: float,
        targeting: Optional[Dict[str, Any]] = None,
        status: str = "PAUSED"
    ) -> Dict[str, Any]:
        """
        Cria um conjunto de anúncios aplicando travas rígidas de orçamento.
        """
        # TRAVA FÍSICA NO CÓDIGO
        if daily_budget_reais > settings.MAX_DAILY_BUDGET_PER_ADSET:
            raise BudgetExceededSecurityError(
                f"Bloqueio de segurança: Orçamento de R$ {daily_budget_reais:.2f} "
                f"excede o teto diário permitido de R$ {settings.MAX_DAILY_BUDGET_PER_ADSET:.2f}."
            )

        # A Meta exige o orçamento em centavos (R$ 30,00 -> 3000 centavos)
        budget_cents = int(daily_budget_reais * 100)

        # Segmentação padrão caso não seja fornecida (Brasil, 24-55 anos)
        default_targeting = {
            "geo_locations": {"countries": ["BR"]},
            "age_min": 24,
            "age_max": 55
        }

        url = f"{self.base_url}/{self.ad_account_id}/adsets"
        payload = {
            "campaign_id": campaign_id,
            "name": name,
            "daily_budget": budget_cents,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "OFFSITE_CONVERSIONS",
            "targeting": targeting or default_targeting,
            "status": status
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json()

    # =========================================================================
    # 3. GATILHO DE STOP-LOSS (O PAUSADOR AUTOMÁTICO)
    # =========================================================================

    def pause_ad(self, ad_id: str) -> bool:
        """Pausa imediatamente um anúncio que violou as regras de stop-loss."""
        url = f"{self.base_url}/{ad_id}"
        payload = {"status": "PAUSED"}

        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json().get("success", False)

    def resume_ad(self, ad_id: str) -> bool:
        """Ativa um anúncio pausado mediante aprovação do lojista."""
        url = f"{self.base_url}/{ad_id}"
        payload = {"status": "ACTIVE"}

        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            return response.json().get("success", False)
