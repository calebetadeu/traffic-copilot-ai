"""Teste do pipeline de criativos (Processador de Imagem + Schemas)."""

import os
from PIL import Image, ImageDraw
from src.core.config import settings
from src.services.image_service import ImageProcessorService
from src.models.creative import CreativeAngle, CreativeBatchResponse


def create_dummy_product_image(output_path: str = "temp/dummy_shirt.jpg"):
    """Cria uma imagem de teste representando uma camiseta preta."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (800, 800), (230, 230, 230))
    draw = ImageDraw.Draw(img)
    # Desenhar um formato simples de camiseta
    draw.rectangle([250, 200, 550, 650], fill=(25, 25, 28))
    draw.polygon([(250, 200), (150, 300), (220, 350), (250, 280)], fill=(25, 25, 28))
    draw.polygon([(550, 200), (650, 300), (580, 350), (550, 280)], fill=(25, 25, 28))
    img.save(output_path, quality=90)
    return output_path


def test_image_processor():
    print("[1/3] Testando geracao de imagem dummy...")
    dummy_path = create_dummy_product_image()
    assert os.path.exists(dummy_path)
    print(f" -> Imagem criada em: {dummy_path}")

    print("[2/3] Testando ImageProcessorService (Feed 1:1 e Stories 9:16 com Selo)...")
    service = ImageProcessorService(output_dir="temp/test_output")
    assets = service.prepare_ad_assets(dummy_path, badge_text="100% Algodão Nobre")
    
    assert os.path.exists(assets["feed_1x1"])
    assert os.path.exists(assets["stories_9x16"])
    print(f" -> Feed 1:1 gerado: {assets['feed_1x1']}")
    print(f" -> Stories 9:16 gerado: {assets['stories_9x16']}")

    print("[3/3] Testando Schemas Pydantic de Criativos...")
    sample_batch = CreativeBatchResponse(
        product_summary="Camiseta Básica Preta, gola redonda, algodão encorpado",
        target_persona="Homens de 25-40 anos que buscam peças básicas de alta durabilidade",
        suggested_interests=["Moda masculina", "Roupas casuais", "Estilo minimalista"],
        variations=[
            CreativeAngle(
                angle_name="Praticidade Anti-Encolhimento",
                hook="Cansado de camiseta que vira 'cropped' na primeira lavagem?",
                headline="Algodão Nobre Que Não Encolhe",
                primary_text="Nossa camiseta básica foi feita com fibra longa penteada que não deforma, não desbota e não encolhe após lavar. Conforto absoluto para o dia a dia.",
                suggested_visual_overlay="Frete Grátis Acima de 2 Peças"
            ),
            CreativeAngle(
                angle_name="Conforto Térmico",
                hook="Camiseta que respira e não esquenta no calor.",
                headline="Toque Macio & Ultra Frescor",
                primary_text="Desenvolvida com linho e algodão respirável, você se mantém alinhado e fresco mesmo nos dias mais quentes. Peça versátil para qualquer ocasião.",
                suggested_visual_overlay="Edição Limitada"
            ),
            CreativeAngle(
                angle_name="Combo Econômico",
                hook="Renove seus básicos da semana com preço de fábrica.",
                headline="Kit 3 Camisetas Essenciais",
                primary_text="Garanta 3 peças indispensáveis no seu guarda-roupa com frete grátis e desconto progressivo. Qualidade premium para vestir todos os dias.",
                suggested_visual_overlay="Kit 3 Peças com Desconto"
            )
        ]
    )
    assert len(sample_batch.variations) == 3
    print(f" -> Schema validado com sucesso! {len(sample_batch.variations)} variacoes configuradas.")
    print("\n[OK] TODOS OS TESTES PASSARAM COM SUCESSO!")


if __name__ == "__main__":
    test_image_processor()
