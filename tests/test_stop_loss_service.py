"""Testes unitários para o motor de Stop-Loss e Scheduler."""

import pytest
from src.models.meta import AdInsightMetric
from src.models.stop_loss import AdActionType
from src.services.stop_loss_service import StopLossService
from src.core.scheduler import TrafficScheduler


def test_stop_loss_pause_rule():
    """Valida se o anúncio é pausado quando estoura o CPA teto sem vendas."""
    service = StopLossService()
    target_cpa = 35.00

    # Anúncio gastou R$ 40,00 e não teve nenhuma compra
    metric = AdInsightMetric(
        ad_id="ad_bad_01",
        ad_name="Camiseta Linho - Ângulo Fraco",
        spend=40.00,
        impressions=1200,
        clicks=25,
        ctr=2.08,
        cpc=1.60,
        purchases=0
    )

    decision = service.evaluate_ad(metric, target_cpa=target_cpa)
    assert decision.action == AdActionType.PAUSE
    assert "Stop-Loss ativado" in decision.reason
    print("[OK] Regra de Stop-Loss pausou anúncio sem conversão!")


def test_scale_winner_rule():
    """Valida se o anúncio com alto ROAS e CPA saudável é marcado para escala."""
    service = StopLossService()
    target_cpa = 35.00

    # Anúncio gastou R$ 50,00, gerou 3 compras (CPA R$ 16,66) e ROAS 4.5x
    metric = AdInsightMetric(
        ad_id="ad_winner_01",
        ad_name="Polo Piquet - Ângulo Conforto",
        spend=50.00,
        impressions=2500,
        clicks=90,
        ctr=3.60,
        cpc=0.55,
        purchases=3,
        cpa=16.66,
        roas=4.5
    )

    decision = service.evaluate_ad(metric, target_cpa=target_cpa)
    assert decision.action == AdActionType.SCALE
    assert "Criativo Vencedor" in decision.reason
    print("[OK] Regra de Escala identificou criativo campeão!")


def test_fatigue_alert_rule():
    """Valida se anúncio com muitas impressões e CTR baixo é sinalizado com fadiga."""
    service = StopLossService()
    target_cpa = 35.00

    # 1500 impressões e CTR de apenas 0.40%
    metric = AdInsightMetric(
        ad_id="ad_fatigue_01",
        ad_name="Básica Preta - Gancho Antigo",
        spend=15.00,
        impressions=1500,
        clicks=6,
        ctr=0.40,
        cpc=2.50,
        purchases=0
    )

    decision = service.evaluate_ad(metric, target_cpa=target_cpa)
    assert decision.action == AdActionType.ALERT_FATIGUE
    assert "Fadiga/Gancho fraco" in decision.reason
    print("[OK] Alerta de fadiga criativa disparado com sucesso!")


def test_batch_and_whatsapp_formatting():
    """Valida processamento de lote em modo dry-run e geração do texto do WhatsApp."""
    service = StopLossService()
    metrics = [
        AdInsightMetric(
            ad_id="ad_1",
            ad_name="Camisa A",
            spend=45.00,
            impressions=1000,
            clicks=10,
            ctr=1.0,
            cpc=4.5,
            purchases=0
        ),
        AdInsightMetric(
            ad_id="ad_2",
            ad_name="Camisa B",
            spend=30.00,
            impressions=1500,
            clicks=50,
            ctr=3.3,
            cpc=0.6,
            purchases=2,
            cpa=15.0,
            roas=4.2
        )
    ]

    summary = service.process_metrics_batch(metrics, target_cpa=35.00, dry_run=True)
    assert summary.ads_checked == 2
    assert summary.ads_paused == 1
    assert summary.ads_scaled == 1

    msg = service.format_whatsapp_notification(summary)
    assert msg is not None
    assert "Sentinela de Tráfego" in msg
    assert "Camisa A" in msg
    assert "Camisa B" in msg
    print("[OK] Mensagem de alerta formatada perfeitamente para WhatsApp!")


def test_scheduler_setup():
    """Valida o registro correto dos jobs no agendador."""
    sched = TrafficScheduler()
    dummy_task = lambda: None
    sched.setup_jobs(
        stop_loss_task=dummy_task,
        daily_digest_task=dummy_task,
        stop_loss_interval_minutes=30
    )
    job_ids = [job.id for job in sched.scheduler.get_jobs()]
    assert "stop_loss_sentinel" in job_ids
    assert "daily_digest_report" in job_ids
    print("[OK] APScheduler configurou os jobs com sucesso!")
