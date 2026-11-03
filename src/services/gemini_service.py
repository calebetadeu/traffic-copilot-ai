"""Motor de IA Multimodal (Google Gemini) para geração de criativos de alta conversão em moda."""

import os
from typing import Optional, Union
from PIL import Image
import io

from google import genai
from google.genai import types

from src.core.config import settings
from src.models.creative import CreativeBatchResponse


SYSTEM_INSTRUCTION = """
Você é um Diretor de Criação e Copywriter Sênior especializado em Tráfego Pago (Meta Ads) para marcas de roupas e e-commerce de moda.

Sua missão:
Receber a foto de uma peça de vestuário (camisa, polo, linho, camiseta básica, calça, etc.) e as informações da loja para gerar um lote de variações de criativos de alta conversão para testes A/B/n na Meta.

DIRETRIZES DE MODA E CONVERSÃO:
1. FOCO NO BENEFÍCIO REAL: Os clientes de moda não compram apenas tecido, compram caimento, elegância sem esforço, conforto térmico (não esquentar no calor) e durabilidade (não encolher na primeira lavagem, gola que não laceia).
2. DIVERSIDADE DE ÂNGULOS: Gere variações explorando diferentes motivações:
   - Ângulo Praticidade: Tecido nobre que não amarrota fácil, rápido de passar, pronto para vestir.
   - Ângulo Conforto Térmico: Respirabilidade, toque macio, ideal para o dia a dia e clima quente.
   - Ângulo Versatilidade/Estilo: Da reunião de trabalho ao happy hour / jantar no fim de semana.
   - Ângulo Oferta/Combo: Leve mais por menos (Kit 3 peças, frete grátis no combo).
   - Ângulo Caimento: Valoriza o corpo sem apertar, costura alinhada e acabamento premium.

FILTROS ANTI-BLOQUEIO META ADS (OBRIGATÓRIO):
- NUNCA use menções diretas a atributos pessoais negativos ("Você se veste mal?", "Cansado de passar vergonha?").
- NUNCA use promessas milagrosas ou superlativos vazios ("A melhor camisa do universo").
- NUNCA faça clickbait apelativo. Mantenha tom sofisticado, confiável e comercialmente atraente.
- Títulos (Headlines) devem ser diretos e ter no máximo 50 caracteres.
"""


class GeminiCreativeService:
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError(
                "GEMINI_API_KEY não foi configurada! Defina a chave no arquivo .env ou passe no construtor."
            )
        self.client = genai.Client(api_key=key)
        self.model = settings.GEMINI_MODEL

    def generate_creatives_from_image(
        self,
        image_input: Union[str, bytes, Image.Image],
        product_notes: str = "",
        brand_dna: Optional[str] = None,
        num_variations: int = 5
    ) -> CreativeBatchResponse:
        """
        Analisa uma imagem de produto e gera variações de criativos estruturados.
        
        Args:
            image_input: Caminho do arquivo (str), bytes da imagem, ou objeto PIL Image.
            product_notes: Notas rápidas do lojista (preço, tecido, oferta, frete).
            brand_dna: Contexto acumulado da marca (tom de voz, persona, histórico).
            num_variations: Quantidade de variações de ângulos a gerar.
        """
        # Preparar a imagem para a API
        if isinstance(image_input, str):
            image = Image.open(image_input)
        elif isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, Image.Image):
            image = image_input
        else:
            raise ValueError("Formato de imagem inválido. Forneça caminho, bytes ou PIL Image.")

        prompt = f"""
Analise detalhadamente a peça de vestuário na foto anexada.

INFORMAÇÕES FORNECIDAS PELO LOJISTA:
{product_notes or "Nenhuma informação extra fornecida. Extraia os dados visuais da foto."}

CONTEXTO / DNA DA MARCA:
{brand_dna or "Loja de moda contemporânea, foco em qualidade, caimento impecável e excelente custo-benefício."}

TAREFA:
1. Faça o diagnóstico da peça (tipo de gola, corte, tecido aparente, ocasião de uso).
2. Defina a persona ideal e interesses para segmentação na Meta Ads.
3. Gere exatamente {num_variations} variações criativas completas com ângulos diferentes.
4. Garanta 100% de conformidade com as políticas anti-bloqueio da Meta.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=[prompt, image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CreativeBatchResponse,
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            )
        )

        # O SDK já faz o parse ou entrega o JSON validado pelo schema
        return response.parsed

    def generate_creatives_text_only(
        self,
        product_description: str,
        brand_dna: Optional[str] = None,
        num_variations: int = 5
    ) -> CreativeBatchResponse:
        """Gera criativos a partir de descrição em texto quando não houver imagem."""
        prompt = f"""
Crie criativos de alta conversão para o seguinte produto de vestuário:

DESCRIÇÃO DO PRODUTO:
{product_description}

CONTEXTO DA MARCA:
{brand_dna or "Loja de moda moderna, peças de qualidade superior e caimento perfeito."}

Gere {num_variations} variações completas com ângulos diferentes, títulos curtos e copys persuasivas.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CreativeBatchResponse,
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            )
        )
        return response.parsed
