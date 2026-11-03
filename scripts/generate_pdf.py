"""Script para geração de PDF executivo comercial do Traffic Copilot AI (Visão de Produto Final)."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Numeração elegante no rodapé."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 35, 572, 35)
        
        self.drawString(40, 22, "Traffic Copilot AI • Proposta Comercial & Apresentação Executiva")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(572, 22, page_str)
        self.restoreState()


def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2563EB"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        spaceAfter=3
    )

    card_header_style = ParagraphStyle(
        'CardHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # HEADER / CABEÇALHO EXECUTIVO
    # =========================================================================
    story.append(Paragraph("TRAFFIC COPILOT AI 🚀", title_style))
    story.append(Paragraph("O Gestor Autônomo de Tráfego Pago & Criação para Marcas de Moda", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=10))

    intro_box = [
        [Paragraph(
            "<b>Visão Geral da Solução:</b> O <b>Traffic Copilot AI</b> é um ecossistema inteligente de marketing e vendas que assume 100% da operação de tráfego pago da loja direto pelo <b>WhatsApp</b>. O lojista apenas envia as fotos das peças e o sistema cria os anúncios, formata as imagens, sobe as campanhas na Meta e protege o orçamento 24 horas por dia.",
            body_style
        )]
    ]
    t_intro = Table(intro_box, colWidths=[532])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 8))

    # =========================================================================
    # OS 6 PILARES DE FUNCIONALIDADES ENTREGUES
    # =========================================================================
    story.append(Paragraph("O Que o Sistema Entrega para o Lojista (Funcionalidades)", h1_style))

    features = [
        (
            "1. 🧠 Máquina Contínua de Criativos com Inteligência de Moda",
            "• <b>Análise Visual Instantânea:</b> O sistema analisa a foto da peça (corte, caimento, linho, algodão, gola) e entende a proposta do produto.<br/>"
            "• <b>Multi-Ângulos de Conversão:</b> Gera de 5 a 10 variações de textos vendedores explorando o que realmente faz vender: frescor no calor, tecido que não encolhe nem amarrota, durabilidade e combos de kit.<br/>"
            "• <b>Filtros Anti-Bloqueio:</b> Textos 100% em conformidade com as diretrizes da Meta (sem promessas falsas ou gatilhos que causem restrição)."
        ),
        (
            "2. 🎨 Design e Formatação Automática de Banners",
            "• <b>Multi-Formatos Oficiais:</b> Gera na hora a versão quadrada para <b>Feed (1:1)</b> e vertical para <b>Stories/Reels (9:16)</b>.<br/>"
            "• <b>Enquadramento Profissional:</b> Centraliza a roupa mantendo respiro e fundo neutro de moda.<br/>"
            "• <b>Aplicação Dinâmica de Selos:</b> Aplica automaticamente selos de alto impacto (ex: <i>'100% Algodão Nobre'</i>, <i>'Frete Grátis no Combo'</i>, <i>'Compre 2 Leve 3'</i>)."
        ),
        (
            "3. 🛡️ Sentinela 24 Horas & 'Stop-Loss de Trader' (Proteção de Caixa)",
            "• <b>Corte Imediato de Prejuízo:</b> Se um anúncio gastar o valor teto de uma venda sem converter, o sistema <b>pausa o anúncio automaticamente na Meta</b>.<br/>"
            "• <b>Detector de Campeões (Escala):</b> Identifica anúncios com ROAS acima de 3.0x e avisa para aumentar a verba com segurança.<br/>"
            "• <b>Detector de Fadiga:</b> Alerta quando um criativo cansou e já prepara novos anúncios para substituir."
        ),
        (
            "4. 📱 Gestão de Bolso Direto pelo WhatsApp (Zero Complexidade)",
            "• <b>Sem Painéis Complicados:</b> O dono da marca não precisa abrir o computador nem entender o Gerenciador da Meta.<br/>"
            "• <b>Aprovação em 1 Clique:</b> O lojista recebe a prévia do anúncio no WhatsApp e responde apenas <b>'1' (Aprovar)</b> ou <b>'2' (Ajustar)</b> para colocar no ar.<br/>"
            "• <b>Resumo Diário às 20h:</b> Relatório limpo no celular com gasto do dia, vendas realizadas e faturamento."
        ),
        (
            "5. 🚀 Subida Técnica Perfeita & Travas Físicas de Segurança",
            "• <b>Campanhas Profissionais:</b> Montagem de campanhas de vendas com pixel calibrado e públicos qualificados de compradores online.<br/>"
            "• <b>Trava Física Anti-Erro:</b> Limite estrito de orçamento travado no sistema, garantindo que nenhum erro gaste mais do que o combinado com o cliente."
        ),
        (
            "6. 🧬 Auditoria de DNA da Marca (Aproveitamento de Histórico)",
            "• <b>Engenharia Reversa:</b> Conecta na conta existente e identifica quais foram os anúncios mais lucrativos da história da loja.<br/>"
            "• <b>Aprendizado Contínuo:</b> O robô já começa sabendo o tom de voz e o público que mais compra na loja."
        )
    ]

    for title, desc in features:
        t_data = [
            [Paragraph(f"<b>{title}</b>", card_header_style)],
            [Paragraph(desc, bullet_style)]
        ]
        t = Table(t_data, colWidths=[532])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 6))

    # =========================================================================
    # MODELO DE NEGÓCIO & OFERTA COMERCIAL (VENDA CASADA)
    # =========================================================================
    story.append(Paragraph("Modelo Comercial: Fornecimento + Tecnologia (Venda Casada)", h1_style))
    story.append(Paragraph(
        "A oferta une o <b>fornecimento das peças/camisetas</b> ao <b>robô de vendas no WhatsApp</b>, eliminando a maior barreira de quem compra vestuário: conseguir vender no digital.",
        body_style
    ))

    table_data = [
        [
            Paragraph("<b>Plano</b>", card_header_style),
            Paragraph("<b>Perfil do Cliente</b>", card_header_style),
            Paragraph("<b>Mensalidade</b>", card_header_style),
            Paragraph("<b>O Que Entrega</b>", card_header_style)
        ],
        [
            Paragraph("<b>Starter (Entrada)</b>", body_style),
            Paragraph("Marcas iniciando (mínimo R$ 30/dia em ads)", body_style),
            Paragraph("<b>R$ 399,00 / mês</b>", body_style),
            Paragraph("Esteira contínua de criativos, proteção 24h de Stop-Loss e aprovações via WhatsApp", body_style)
        ],
        [
            Paragraph("<b>Growth (Escala)</b>", body_style),
            Paragraph("Marcas consolidadas com alto volume de vendas", body_style),
            Paragraph("<b>R$ 799 a R$ 899 / mês</b>", body_style),
            Paragraph("Volume ampliado de criativos semanais, escala de orçamento e auditorias avançadas", body_style)
        ]
    ]

    t_pricing = Table(table_data, colWidths=[100, 145, 115, 172])
    t_pricing.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_pricing)

    story.append(Spacer(1, 8))

    # Comparativo com mercado e Projeção
    comp_box = [
        [Paragraph("<b>Por que a oferta fecha fácil? Comparativo de Mercado:</b>", card_header_style)],
        [Paragraph(
            "• <b>Agência / Gestor Tradicional:</b> Cobra de R$ 2.000 a R$ 4.000/mês, demora dias para criar um anúncio e atende vários clientes sem exclusividade.<br/>"
            "• <b>Nossa Solução:</b> R$ 399/mês (uma fração do custo), velocidade instantânea, foco no nicho de roupas e proteção de caixa 24h por dia.",
            bullet_style
        )],
        [Paragraph("<b>Projeção de Recorrência (MRR):</b>", card_header_style)],
        [Paragraph(
            "• <b>30 clientes ativos:</b> R$ 11.970,00 / mês<br/>"
            "• <b>50 clientes ativos:</b> R$ 19.950,00 / mês<br/>"
            "• <b>100 clientes ativos:</b> R$ 39.900,00 / mês",
            bullet_style
        )]
    ]
    t_comp = Table(comp_box, colWidths=[532])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_comp)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF Executivo regenerado com sucesso em: {filename}")


if __name__ == "__main__":
    out_dir = "C:/Users/Pichau/Documents/traffic-copilot-ai/docs"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Traffic_Copilot_AI_Apresentacao_Executiva.pdf")
    build_pdf(pdf_path)
