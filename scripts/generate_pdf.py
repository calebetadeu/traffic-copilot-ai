"""Script para geração de PDF executivo de apresentação técnica e comercial do Traffic Copilot AI."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Adiciona numeração de páginas profissional no rodapé."""
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
        
        # Linha fina de rodapé
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 35, 572, 35)
        
        # Texto de rodapé
        self.drawString(40, 22, "Traffic Copilot AI • Documento de Apresentação Técnica & Comercial • Confidencial")
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

    # Estilos customizados
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
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
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
        leftIndent=15,
        spaceAfter=4
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
    # HEADER / CABEÇALHO
    # =========================================================================
    story.append(Paragraph("TRAFFIC COPILOT AI 🚀", title_style))
    story.append(Paragraph("Sistema Autônomo de Tráfego Pago & Criação Contínua para Moda / E-commerce", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=10))

    meta_info_text = (
        "<b>Parceria Estratégica:</b> Calebe Tadeu (Engenharia de Software) & Alexandre (Comercial / Vestuário)<br/>"
        "<b>Objetivo:</b> Integrar fornecimento de roupas à gestão inteligente de anúncios para marcas em escala.<br/>"
        "<b>Status do Sistema:</b> v0.4.0-alpha • 100% Testado e Operacional em Ambiente Dev."
    )
    story.append(Paragraph(meta_info_text, body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SEÇÃO 1: FUNCIONALIDADES JÁ DESENVOLVIDAS (100% OPERACIONAIS)
    # =========================================================================
    story.append(Paragraph("1. Funcionalidades Já Desenvolvidas (Prontas para o Piloto)", h1_style))
    story.append(Paragraph(
        "A base tecnológica principal do robô já está construída, com código versionado no GitHub e 9 testes unitários aprovados com nota máxima de segurança.",
        body_style
    ))

    features_developed = [
        (
            "🧠 Motor de Criativos com IA Multimodal (Gemini 2.0 Flash)",
            "• <b>Visão Computacional:</b> Analisa a foto da camisa/peça identificando corte, caimento e tipo de tecido.<br/>"
            "• <b>Máquina de Variações:</b> Gera de 5 a 10 copys com ângulos estratégicos (Conforto térmico, Anti-encolhimento, Durabilidade, Combo atacado/varejo).<br/>"
            "• <b>Filtros Anti-Bloqueio:</b> Bloqueia termos proibidos pela Meta (sem falsas promessas, sem atributos pessoais)."
        ),
        (
            "🎨 Processador Visual Automático de Imagens (Pillow Engine)",
            "• <b>Padronização de Formatos:</b> Gera automaticamente a versão <b>Feed (1:1)</b> e <b>Stories/Reels (9:16)</b>.<br/>"
            "• <b>Enquadramento Inteligente:</b> Centraliza a peça em fundo neutro de moda com respiro visual de 90%.<br/>"
            "• <b>Aplicação de Selos:</b> Aplica automaticamente selos modernos (ex: <i>'100% Algodão Nobre'</i>, <i>'Frete Grátis no Combo'</i>)."
        ),
        (
            "🕵️ Auditor de DNA da Meta Ads (Engenharia Reversa Histórica)",
            "• <b>Varredura Automática:</b> Puxa os dados dos últimos 3 a 6 meses de anúncios da conta via API oficial.<br/>"
            "• <b>Filtro de Campeões:</b> Identifica os criativos históricos que mais geraram compras e maior ROAS.<br/>"
            "• <b>Aprendizado Rápido:</b> Extrai o tom de voz e ganchos vencedores para o robô nunca começar do zero."
        ),
        (
            "🛡️ Despachante Seguro para Meta Ads (Proteção de Caixa)",
            "• <b>Modo Rascunho Blindado:</b> Toda campanha, conjunto ou anúncio é criado como <b>PAUSED</b> (nenhum anúncio entra no ar sem aprovação humana).<br/>"
            "• <b>Trava Física de Orçamento:</b> O código aborta fisicamente qualquer tentativa de definir orçamento acima de R$ 50/dia por conjunto, blindando a conta contra estouros acidentais."
        ),
        (
            "⏱️ Sentinela Autônomo ('Lógica Trader' de Stop-Loss)",
            "• <b>Corte Imediato de Prejuízo:</b> Se o anúncio gastar 1x o CPA teto sem compras, o robô <b>pausa o anúncio sozinho na Meta</b>.<br/>"
            "• <b>Detector de Vencedores:</b> Identifica anúncios com ROAS &ge; 3.0x para recomendação de aumento de verba.<br/>"
            "• <b>Alerta de Fadiga Criativa:</b> Detecta anúncios com CTR &lt; 0.8% após 1.000 impressões para substituição."
        ),
        (
            "⏰ Agendador 24/7 em Background (APScheduler)",
            "• Sentinela de proteção roda a cada 60 minutos monitorando métricas.<br/>"
            "• Rotina diária agendada para as 20h para consolidação de vendas e envio de resumo financeiro."
        )
    ]

    for title, desc in features_developed:
        t_data = [
            [Paragraph(f"<b>{title}</b>", card_header_style)],
            [Paragraph(desc, bullet_style)]
        ]
        t = Table(t_data, colWidths=[532])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SEÇÃO 2: FUNCIONALIDADES EM DESENVOLVIMENTO & ROADMAP DE EXPANSÃO
    # =========================================================================
    story.append(Paragraph("2. O Que Conseguimos Desenvolver a Seguir (Roadmap de Escala)", h1_style))
    story.append(Paragraph(
        "Módulos complementares para transformar o agente em uma plataforma SaaS completa de alta escala:",
        body_style
    ))

    roadmap_items = [
        (
            "📱 Copiloto de Bolso no WhatsApp (Evolution API / Z-API)",
            "• O lojista manda a foto da peça no WhatsApp e o robô responde com os criativos prontos em 30 segundos.<br/>"
            "• <b>Aprovação em 1 Clique:</b> O cliente responde apenas <b>'1' (Aprovar)</b> ou <b>'2' (Editar)</b> para ativar a campanha."
        ),
        (
            "🔒 Trava de Assinatura & Inadimplência (Multi-Tenant)",
            "• Sistema multi-cliente isolado. Caso o lojista atrase a mensalidade (R$ 399/mês), o robô tranca o acesso e suspende a criação de novos anúncios automaticamente."
        ),
        (
            "🎥 Editor e Clonador de Vídeos Curtos (Reels / TikTok)",
            "• Ingestão de vídeos brutos das camisas no corpo com corte automático de ganchos, legendas dinâmicas e trilhas em alta para formato 9:16."
        ),
        (
            "📢 Disparador Inteligente para a Base de Contatos (5k a 6k Leads)",
            "• Disparos humanizados e segmentados em números separados para convidar a base para lançamentos e grupos VIP de compradores."
        ),
        (
            "🛒 Integração Direta com Plataformas de E-commerce",
            "• Leitura direta de catálogo, estoque e pixel via Shopify, Nuvemshop, Yampi e WooCommerce."
        )
    ]

    for title, desc in roadmap_items:
        t_data = [
            [Paragraph(f"<b>{title}</b>", card_header_style)],
            [Paragraph(desc, bullet_style)]
        ]
        t = Table(t_data, colWidths=[532])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#93C5FD")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # =========================================================================
    # SEÇÃO 3: MODELO COMERCIAL & ECONOMIA DA PARCERIA
    # =========================================================================
    story.append(Paragraph("3. Modelo Comercial: Venda Casada & Recorrência", h1_style))
    story.append(Paragraph(
        "A combinação do fornecimento físico de camisetas com o robô de tráfego cria uma oferta irresistível no mercado:",
        body_style
    ))

    table_data = [
        [
            Paragraph("<b>Plano</b>", card_header_style),
            Paragraph("<b>Público-Alvo</b>", card_header_style),
            Paragraph("<b>Valor Mensal</b>", card_header_style),
            Paragraph("<b>Entregáveis Principais</b>", card_header_style)
        ],
        [
            Paragraph("<b>Entrada (Starter)</b>", body_style),
            Paragraph("Marcas iniciando (mín. R$ 30/dia em ads)", body_style),
            Paragraph("<b>R$ 399,00 / mês</b>", body_style),
            Paragraph("Esteira de criativos, Stop-Loss diário e aprovação via WhatsApp", body_style)
        ],
        [
            Paragraph("<b>Escala (Growth)</b>", body_style),
            Paragraph("Marcas consolidadas com alto volume de vendas", body_style),
            Paragraph("<b>R$ 799 a R$ 899 / mês</b>", body_style),
            Paragraph("Volume estendido de criativos, auditorias contínuas e escala de orçamento", body_style)
        ]
    ]

    t_pricing = Table(table_data, colWidths=[100, 150, 110, 172])
    t_pricing.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_pricing)

    story.append(Spacer(1, 12))

    summary_box = [
        [Paragraph("<b>Projeção de Faturamento Recorrente (MRR):</b>", card_header_style)],
        [Paragraph(
            "• <b>30 clientes ativos:</b> R$ 11.970,00 / mês<br/>"
            "• <b>50 clientes ativos:</b> R$ 19.950,00 / mês<br/>"
            "• <b>100 clientes ativos:</b> R$ 39.900,00 / mês<br/>"
            "<i>(Custo operacional de infraestrutura e IA por cliente: menos de R$ 15,00/mês).</i>",
            bullet_style
        )]
    ]
    t_sum = Table(summary_box, colWidths=[532])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(t_sum)

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] PDF gerado com sucesso em: {filename}")


if __name__ == "__main__":
    out_dir = "C:/Users/Pichau/Documents/traffic-copilot-ai/docs"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Traffic_Copilot_AI_Apresentacao_Executiva.pdf")
    build_pdf(pdf_path)
