"""Agendador de Tarefas em Segundo Plano (APScheduler).

Gerencia:
1. Ciclo de Stop-Loss a cada hora (Sentinela de Proteção de Caixa);
2. Resumo Diário de Performance às 20h para o WhatsApp do Lojista.
"""

import logging
from typing import Optional, Callable
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("traffic_copilot.scheduler")


class TrafficScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._is_running = False

    def setup_jobs(
        self,
        stop_loss_task: Callable,
        daily_digest_task: Callable,
        stop_loss_interval_minutes: int = 60
    ):
        """Registra as rotinas recorrentes no agendador."""
        # 1. Sentinela de Stop-Loss a cada 60 minutos
        self.scheduler.add_job(
            stop_loss_task,
            trigger=IntervalTrigger(minutes=stop_loss_interval_minutes),
            id="stop_loss_sentinel",
            name="Sentinela de Stop-Loss Horário",
            replace_existing=True
        )
        logger.info(f"Job 'stop_loss_sentinel' configurado para rodar a cada {stop_loss_interval_minutes} min.")

        # 2. Resumo Diário de Performance às 20:00
        self.scheduler.add_job(
            daily_digest_task,
            trigger=CronTrigger(hour=20, minute=0),
            id="daily_digest_report",
            name="Resumo Diário de Vendas às 20h",
            replace_existing=True
        )
        logger.info("Job 'daily_digest_report' configurado para rodar todos os dias às 20:00.")

    def start(self):
        """Inicia o agendador em background caso ainda não esteja rodando."""
        if not self._is_running:
            self.scheduler.start()
            self._is_running = True
            logger.info("APScheduler iniciado com sucesso.")

    def shutdown(self):
        """Encerra graciosamente o agendador."""
        if self._is_running:
            self.scheduler.shutdown(wait=False)
            self._is_running = False
            logger.info("APScheduler encerrado.")


# Instância global
traffic_scheduler = TrafficScheduler()
