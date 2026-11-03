"""Modelos de dados (Pydantic) para geração de criativos estruturados."""

from typing import List, Optional
from pydantic import BaseModel, Field


class CreativeAngle(BaseModel):
    """Representa uma variação única de criativo para teste A/B/n."""
    angle_name: str = Field(
        ...,
        description="Nome do ângulo de venda (ex: 'Frescor no Calor', 'Não Amassa', 'Combo Econômico')"
    )
    hook: str = Field(
        ...,
        description="Gancho de abertura (primeira linha do anúncio ou áudio do criativo para prender a atenção)"
    )
    headline: str = Field(
        ...,
        max_length=50,
        description="Título curto que aparece abaixo da imagem na Meta (máximo 50 caracteres)"
    )
    primary_text: str = Field(
        ...,
        description="Texto principal do anúncio (copy persuasiva com dor, solução, prova social e CTA)"
    )
    call_to_action: str = Field(
        default="Comprar agora",
        description="Botão de CTA (ex: 'Comprar agora', 'Saiba mais', 'Obter oferta')"
    )
    suggested_visual_overlay: Optional[str] = Field(
        default=None,
        description="Texto do selo ou sticker a ser aplicado na imagem (ex: 'Frete Grátis no Combo')"
    )


class CreativeBatchResponse(BaseModel):
    """Lote de criativos gerados pela IA multimodal."""
    product_summary: str = Field(
        ...,
        description="Diagnóstico da peça identificada na foto (tipo de peça, tecido aparente, estilo e diferenciais)"
    )
    target_persona: str = Field(
        ...,
        description="Perfil do comprador ideal (idade, ocasiões de uso, prioridades de estilo)"
    )
    suggested_interests: List[str] = Field(
        default_factory=list,
        description="Públicos/interesses recomendados para direcionamento na Meta (ex: Moda masculina, Roupas casuais)"
    )
    variations: List[CreativeAngle] = Field(
        ...,
        min_length=3,
        description="Lista de variações criativas para alimentar a esteira de testes"
    )
    policy_check_passed: bool = Field(
        default=True,
        description="True se o texto respeita 100% as diretrizes da Meta Ads"
    )
    policy_notes: str = Field(
        default="Aprovado: sem promessas exageradas, sem menção a atributos pessoais, sem clickbait.",
        description="Justificativa da verificação de conformidade com políticas"
    )
