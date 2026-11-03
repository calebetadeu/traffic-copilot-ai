"""Configurações globais e variáveis de ambiente do Traffic Copilot AI."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Geral
    ENVIRONMENT: str = Field(default="development", description="development, staging ou production")
    LOG_LEVEL: str = Field(default="INFO")
    
    # Google Gemini
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Chave da API do Google Gemini")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", description="Modelo padrão do Gemini")
    
    # Meta Marketing API
    META_APP_ID: Optional[str] = Field(default=None)
    META_APP_SECRET: Optional[str] = Field(default=None)
    META_ACCESS_TOKEN: Optional[str] = Field(default=None, description="System User ou Long-lived Access Token")
    META_AD_ACCOUNT_ID: Optional[str] = Field(default=None, description="ID da conta ex: act_123456789")
    META_GRAPH_VERSION: str = Field(default="v21.0")
    
    # Travas de Segurança (Hardcoded Guards)
    MAX_DAILY_BUDGET_PER_ADSET: float = Field(
        default=50.00,
        description="Limite máximo de orçamento diário em R$ por conjunto (trava contra estouro de verba)"
    )
    DEFAULT_STOP_LOSS_MULTIPLIER: float = Field(
        default=1.0,
        description="Múltiplo do CPA teto para acionar pausa automática (ex: 1x CPA sem compra = pausa)"
    )
    
    # WhatsApp Gateway (Evolution API)
    EVOLUTION_API_URL: str = Field(default="http://localhost:8080")
    EVOLUTION_API_KEY: Optional[str] = Field(default=None)
    EVOLUTION_INSTANCE_NAME: str = Field(default="traffic-copilot")
    
    # Banco de Dados
    DATABASE_URL: str = Field(default="sqlite:///./traffic_copilot.db")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instância singleton para uso em toda a aplicação
settings = Settings()
