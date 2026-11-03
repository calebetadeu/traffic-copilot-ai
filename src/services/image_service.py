"""Processador visual de imagens (Pillow) para padronização de formatos e aplicação de selos promocionais."""

import os
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont


class ImageProcessorService:
    """Padroniza fotos de roupas para formatos oficiais da Meta e aplica selos dinâmicos."""

    # Resoluções recomendadas pela Meta
    RATIOS = {
        "1:1": (1080, 1080),     # Feed Instagram / Facebook
        "4:5": (1080, 1350),     # Feed Retrato (maior ocupação de tela no mobile)
        "9:16": (1080, 1920),    # Stories e Reels
    }

    def __init__(self, output_dir: str = "temp/processed_images"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def format_to_ratio(
        self,
        image: Image.Image,
        ratio: str = "1:1",
        bg_color: Tuple[int, int, int] = (248, 249, 250)  # Off-white neutro para moda
    ) -> Image.Image:
        """
        Redimensiona e centraliza a peça de vestuário na proporção desejada sem distorcer.
        """
        target_size = self.RATIOS.get(ratio, (1080, 1080))
        target_w, target_h = target_size

        # Converte para RGB caso esteja em RGBA ou outro modo
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Redimensiona proporcionalmente mantendo margem elegante de respiro (90% do canvas)
        canvas_w = int(target_w * 0.90)
        canvas_h = int(target_h * 0.90)
        
        img_copy = image.copy()
        img_copy.thumbnail((canvas_w, canvas_h), Image.Resampling.LANCZOS)

        # Cria tela de fundo neutra
        canvas = Image.new("RGB", target_size, bg_color)
        
        # Centraliza a peça
        offset_x = (target_w - img_copy.width) // 2
        offset_y = (target_h - img_copy.height) // 2
        canvas.paste(img_copy, (offset_x, offset_y))

        return canvas

    def apply_badge_overlay(
        self,
        image: Image.Image,
        badge_text: str,
        badge_color: Tuple[int, int, int] = (17, 17, 17),  # Preto premium
        text_color: Tuple[int, int, int] = (255, 255, 255)  # Branco
    ) -> Image.Image:
        """
        Desenha um selo estilo 'pill' moderno no canto superior do anúncio.
        Ex: 'FRETE GRÁTIS NO COMBO', '100% ALGODÃO NOBRE'.
        """
        if not badge_text:
            return image

        img = image.copy()
        draw = ImageDraw.Draw(img)

        # Tenta carregar fonte padrão ou sans-serif do sistema
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            font = ImageFont.load_default()

        # Medir tamanho do texto
        bbox = draw.textbbox((0, 0), badge_text.upper(), font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        padding_x = 32
        padding_y = 16
        box_w = text_w + (padding_x * 2)
        box_h = text_h + (padding_y * 2)

        # Posicionamento no canto superior esquerdo com margem de segurança
        margin = 48
        box_x = margin
        box_y = margin

        # Desenhar retângulo arredondado moderno
        draw.rounded_rectangle(
            [box_x, box_y, box_x + box_w, box_y + box_h],
            radius=16,
            fill=badge_color
        )

        # Desenhar o texto do selo centralizado no pill
        text_x = box_x + padding_x
        text_y = box_y + padding_y - 2
        draw.text((text_x, text_y), badge_text.upper(), fill=text_color, font=font)

        return img

    def prepare_ad_assets(
        self,
        image_path: str,
        badge_text: Optional[str] = None
    ) -> dict:
        """
        Gera o pacote completo de imagens para a campanha:
        - Versão Feed (1:1)
        - Versão Stories/Reels (9:16)
        """
        original = Image.open(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # 1. Gerar Feed 1:1
        feed_img = self.format_to_ratio(original, ratio="1:1")
        if badge_text:
            feed_img = self.apply_badge_overlay(feed_img, badge_text)
        feed_path = os.path.join(self.output_dir, f"{base_name}_feed_1x1.jpg")
        feed_img.save(feed_path, quality=95)

        # 2. Gerar Stories 9:16
        stories_img = self.format_to_ratio(original, ratio="9:16")
        if badge_text:
            stories_img = self.apply_badge_overlay(stories_img, badge_text)
        stories_path = os.path.join(self.output_dir, f"{base_name}_stories_9x16.jpg")
        stories_img.save(stories_path, quality=95)

        return {
            "feed_1x1": feed_path,
            "stories_9x16": stories_path
        }
