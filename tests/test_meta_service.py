"""Testes unitários para o serviço da Meta Marketing API."""

import pytest
from src.core.config import settings
from src.services.meta_service import MetaMarketingService, BudgetExceededSecurityError
from src.models.meta import AccountAuditReport, WinningCreativeSummary


def test_meta_account_id_formatting():
    """Garante que o ID da conta sempre receba o prefixo 'act_' exigido pela Meta."""
    service1 = MetaMarketingService(access_token="fake_token", ad_account_id="123456789")
    assert service1.ad_account_id == "act_123456789"

    service2 = MetaMarketingService(access_token="fake_token", ad_account_id="act_987654321")
    assert service2.ad_account_id == "act_987654321"


def test_budget_exceeded_security_guard():
    """
    TESTE DE SEGURANÇA CRÍTICO:
    Garante que tentar definir orçamento acima do teto estipulado dispara exceção
    física no código e NUNCA faz a requisição para a Meta.
    """
    service = MetaMarketingService(access_token="fake_token", ad_account_id="123456789")
    
    # Orçamento permitido (ex: R$ 30,00 quando teto é R$ 50,00)
    # Apenas validação lógica antes da chamada de rede
    assert 30.00 <= settings.MAX_DAILY_BUDGET_PER_ADSET

    # Orçamento proibido (ex: R$ 150,00 quando teto é R$ 50,00)
    with pytest.raises(BudgetExceededSecurityError) as exc_info:
        service.create_adset(
            campaign_id="camp_123",
            name="Teste Conjunto",
            daily_budget_reais=settings.MAX_DAILY_BUDGET_PER_ADSET + 10.00
        )
    
    assert "Bloqueio de segurança" in str(exc_info.value)
    print("\n[OK] Trava física de orçamento disparou com sucesso e impediu a execução!")


def test_audit_report_schema():
    """Valida o modelo de dados de auditoria de DNA."""
    report = AccountAuditReport(
        ad_account_id="act_123456789",
        period="last_90d",
        total_spend=30250.00,
        total_purchases=850,
        average_roas=4.2,
        average_cpa=35.58,
        winning_creatives=[
            WinningCreativeSummary(
                ad_id="ad_001",
                ad_name="Camisa Linho - Gancho Conforto",
                headline="Algodão Nobre que Não Encolhe",
                primary_text="A peça definitiva para os dias quentes.",
                purchases=320,
                roas=5.1,
                cpa=28.40
            )
        ]
    )
    assert report.total_purchases == 850
    assert len(report.winning_creatives) == 1
    assert report.winning_creatives[0].roas == 5.1
    print("[OK] Schema de Auditoria de DNA validado com sucesso!")


if __name__ == "__main__":
    test_meta_account_id_formatting()
    test_budget_exceeded_security_guard()
    test_audit_report_schema()
    print("\n[SUCESSO] TODOS OS TESTES DA META PASSARAM!")
