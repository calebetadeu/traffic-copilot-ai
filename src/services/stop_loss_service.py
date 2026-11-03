"""Motor de Stop-Loss e Otimização Autônoma ('Lógica de Trader' para Meta Ads)."""

from datetime import datetime
from typing import List, Optional
import logging

from src.core.config import settings
from src.models.meta import AdInsightMetric
from src.models.stop_loss import AdActionType, ActionDecision, StopLossCycleSummary
from src.services.meta_service import MetaMarketingService

logger = logging.getLogger("traffic_copilot.stop_loss")


class StopLossService:
    def __init__(self, meta_service: Optional[MetaMarketingService] = None):
        self.meta_service = meta_service or MetaMarketingService()
        self.stop_loss_multiplier = settings.DEFAULT_STOP_LOSS_MULTIPLIER

    def evaluate_ad(
        self,
        metric: AdInsightMetric,
        target_cpa: float,
        min_ctr: float = 0.8
    ) -> ActionDecision:
        """
        Avalia o desempenho de um anúncio individual com base em regras matemáticas estritas.
        
        Regras:
        1. STOP-LOSS: Gastou >= 1x CPA alvo sem nenhuma venda -> PAUSE.
        2. ESCALA: Fez >= 2 compras, ROAS >= 3.0 e CPA <= CPA alvo -> SCALE.
        3. FADIGA / GANCHO RUIM: Mais de 1000 impressões e CTR < 0.8% -> ALERT_FATIGUE.
        4. REGULAR: Anúncio dentro dos parâmetros aceitáveis -> KEEP.
        """
        # Regra 1: Stop-Loss por estouro de CPA sem conversão
        stop_threshold = target_cpa * self.stop_loss_multiplier
        if metric.purchases == 0 and metric.spend >= stop_threshold:
            return ActionDecision(
                ad_id=metric.ad_id,
                ad_name=metric.ad_name,
                action=AdActionType.PAUSE,
                reason=(
                    f"Stop-Loss ativado: Gastou R$ {metric.spend:.2f} "
                    f"(limite R$ {stop_threshold:.2f}) com 0 compras."
                ),
                spend=metric.spend,
                purchases=metric.purchases,
                cpa=metric.cpa,
                roas=metric.roas,
                ctr=metric.ctr,
                executed=False
            )

        # Regra 2: Candidato a Escala (Winner)
        if metric.purchases >= 2 and (metric.roas or 0.0) >= 3.0:
            cpa = metric.cpa or (metric.spend / metric.purchases)
            if cpa <= target_cpa:
                return ActionDecision(
                    ad_id=metric.ad_id,
                    ad_name=metric.ad_name,
                    action=AdActionType.SCALE,
                    reason=(
                        f"Criativo Vencedor: {metric.purchases} vendas geradas, "
                        f"ROAS {metric.roas:.1f}x e CPA de R$ {cpa:.2f} (abaixo da meta de R$ {target_cpa:.2f})."
                    ),
                    spend=metric.spend,
                    purchases=metric.purchases,
                    cpa=round(cpa, 2),
                    roas=metric.roas,
                    ctr=metric.ctr,
                    executed=False
                )

        # Regra 3: Alerta de Fadiga Criativa ou Gancho Ruim
        if metric.impressions >= 1000 and metric.ctr < min_ctr:
            return ActionDecision(
                ad_id=metric.ad_id,
                ad_name=metric.ad_name,
                action=AdActionType.ALERT_FATIGUE,
                reason=(
                    f"Fadiga/Gancho fraco: CTR de {metric.ctr:.2f}% após {metric.impressions} impressões "
                    f"(mínimo esperado: {min_ctr:.2f}%)."
                ),
                spend=metric.spend,
                purchases=metric.purchases,
                cpa=metric.cpa,
                roas=metric.roas,
                ctr=metric.ctr,
                executed=False
            )

        # Regra 4: Anúncio saudável / em fase de aprendizado
        return ActionDecision(
            ad_id=metric.ad_id,
            ad_name=metric.ad_name,
            action=AdActionType.KEEP,
            reason="Performance normal ou dentro da margem de aprendizado.",
            spend=metric.spend,
            purchases=metric.purchases,
            cpa=metric.cpa,
            roas=metric.roas,
            ctr=metric.ctr,
            executed=True
        )

    def process_metrics_batch(
        self,
        metrics: List[AdInsightMetric],
        target_cpa: float,
        dry_run: bool = False
    ) -> StopLossCycleSummary:
        """
        Avalia um lote de métricas e executa as ações na API da Meta caso necessário.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        decisions: List[ActionDecision] = []
        paused_count = 0
        scaled_count = 0
        kept_count = 0

        for m in metrics:
            decision = self.evaluate_ad(m, target_cpa=target_cpa)

            if decision.action == AdActionType.PAUSE:
                if not dry_run:
                    try:
                        success = self.meta_service.pause_ad(decision.ad_id)
                        decision.executed = success
                        logger.info(f"Anúncio {decision.ad_id} pausado com sucesso na Meta.")
                    except Exception as e:
                        logger.error(f"Falha ao pausar anúncio {decision.ad_id}: {e}")
                        decision.executed = False
                else:
                    decision.executed = True  # Simulado
                paused_count += 1

            elif decision.action == AdActionType.SCALE:
                scaled_count += 1
            else:
                kept_count += 1

            decisions.append(decision)

        return StopLossCycleSummary(
            timestamp=now_str,
            ads_checked=len(metrics),
            ads_paused=paused_count,
            ads_scaled=scaled_count,
            ads_kept=kept_count,
            decisions=decisions
        )

    def format_whatsapp_notification(self, summary: StopLossCycleSummary) -> Optional[str]:
        """Formata uma notificação em português amigável para envio via WhatsApp."""
        if summary.ads_paused == 0 and summary.ads_scaled == 0:
            return None  # Não incomodar o lojista se nada crítico aconteceu

        lines = [f"🛡️ *Sentinela de Tráfego: Atualização ({summary.timestamp})*"]

        if summary.ads_paused > 0:
            lines.append(f"\n⚠️ *{summary.ads_paused} anúncio(s) pausado(s) por Stop-Loss:*")
            for d in summary.decisions:
                if d.action == AdActionType.PAUSE:
                    lines.append(f" • *{d.ad_name}*: {d.reason}")

        if summary.ads_scaled > 0:
            lines.append(f"\n🚀 *{summary.ads_scaled} anúncio(s) de alta performance identificados:*")
            for d in summary.decisions:
                if d.action == AdActionType.SCALE:
                    lines.append(f" • *{d.ad_name}*: ROAS {d.roas}x | {d.purchases} vendas. Sugestão: aumentar verba em 15%.")

        return "\n".join(lines)
