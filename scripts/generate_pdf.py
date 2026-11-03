"""Script para geração de PDF executivo comercial do Traffic Copilot AI (Posicionamento Multicategoria / Qualquer Nicho)."""

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
        
        self.drawString(40, 22, "Traffic Copilot AI • Gestão Autônoma de Tráfego & IA para Qualquer Nicho")
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
    story.append(Paragraph("O Gestor Autônomo de Tráfego Pago & Criação para Empresas e E-commerce", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=10))

    intro_box = [
        [Paragraph(
            "<b>Visão Geral da Solução:</b> O <b>Traffic Copilot AI</b> é um ecossistema inteligente de marketing e vendas que assume 100% da operação de tráfego pago de qualquer empresa direto pelo <b>WhatsApp</b>. Não importa o nicho (moda, cosméticos, eletrônicos, suplementos, acessórios ou serviços): o empresário apenas envia a foto ou informações do produto e a IA analisa, cria os anúncios, formata os banners, sobe as campanhas na Meta e protege o orçamento 24 horas por dia.",
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
    story.append(Paragraph("O Que o Sistema Entrega para o Seu Negócio (Funcionalidades)", h1_style))

    features = [
        (
            "1. 🧠 Máquina Contínua de Criativos com Inteligência Adaptativa",
            "• <b>Visão Computacional Multicategoria:</b> Analisa a foto ou vídeo do produto (roupas, cosméticos, eletrônicos, calçados, joias, etc.) e identifica automaticamente os diferenciais, proposta de valor e apelo visual.<br/>"
            "• <b>Múltiplos Ângulos de Conversão:</b> Gera de 5 a 10 variações de textos persuasivos focando nos motivos reais de compra do cliente: resolução de dor, praticidade, custo-benefício, exclusividade e kits/combos.<br/>"
            "• <b>Filtros Anti-Bloqueio:</b> Textos rigorosamente calibrados com as diretrizes da Meta (sem clickbait ou termos sensíveis que possam restringir a conta)."
        ),
        (
            "2. 🎨 Design e Banners Automáticos com Selos da sua Oferta",
            "• <b>Multi-Formatos Prontos para Anúncio:</b> Gera instantaneamente a versão quadrada para <b>Feed (1:1)</b> e vertical para <b>Stories/Reels (9:16)</b>.<br/>"
            "• <b>Enquadramento e Fundo Profissional:</b> Centraliza o produto mantendo respiro elegante e fundo limpo de alto padrão.<br/>"
            "• <b>Aplicação Dinâmica de Selos:</b> Aplica automaticamente selos de conversão adequados ao seu produto (ex: <i>'Frete Grátis'</i>, <i>'Compre 2 Leve 3'</i>, <i>'Envio em 24h'</i>, <i>'Garantia Estendida'</i>)."
        ),
        (
            "3. 🛡️ Sentinela 24 Horas & 'Stop-Loss de Trader' (Proteção de Caixa)",
            "• <b>Corte Imediato de Prejuízo:</b> Se um anúncio gastar o valor teto estipulado de uma venda sem converter, o sistema <b>pausa o anúncio sozinho na Meta</b> para não queimar o dinheiro da empresa.<br/>"
            "• <b>Detector de Campeões (Escala):</b> Identifica criativos com alto retorno (ROAS &ge; 3.0x) e recomenda aumento seguro do orçamento.<br/>"
            "• <b>Detector de Fadiga:</b> Alerta quando o público cansa de um anúncio e já prepara novos criativos para manter as vendas em alta."
        ),
        (
            "4. 📱 Gestão de Bolso Direto pelo WhatsApp (Zero Complexidade)",
            "• <b>Sem Painéis Complicados:</b> O dono do negócio não precisa perder tempo abrindo computador ou aprendendo o Gerenciador de Anúncios.<br/>"
            "• <b>Aprovação em 1 Clique:</b> O cliente recebe a prévia do anúncio no WhatsApp e responde apenas <b>'1' (Aprovar)</b> ou <b>'2' (Ajustar)</b> para colocar a campanha no ar.<br/>"
            "• <b>Resumo Diário às 20h:</b> Relatório limpo enviado no celular com investimento do dia, número de vendas e retorno financeiro."
        ),
        (
            "5. 🚀 Subida Técnica Segura & Travas Físicas de Orçamento",
            "• <b>Estrutura de Grandes Marcas:</b> Campanhas montadas com foco em vendas reais (`OUTCOME_SALES`), pixel configurado e públicos qualificados de compradores.<br/>"
            "• <b>Trava Física Anti-Erro:</b> Limite rígido de orçamento diário travado no sistema, garantindo que nenhum bug ou erro operacional ultrapasse o teto acordado."
        ),
        (
            "6. 🧬 Auditoria de DNA do Negócio (Aproveitamento de Histórico)",
            "• <b>Engenharia Reversa da Conta:</b> O robô analisa o histórico da conta de anúncios para descobrir quais produtos, textos e públicos mais geraram lucro no passado.<br/>"
            "• <b>Aprendizado Contínuo:</b> A IA começa a rodar já sabendo o tom de voz e o comportamento do cliente do seu negócio."
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
    # MODELO COMERCIAL & ESCALA DO NEGÓCIO
    # =========================================================================
    story.append(Paragraph("Modelo Comercial: Gestão Autônoma de Alta Margem", h1_style))
    story.append(Paragraph(
        "Uma solução com barreira de entrada baixa e alto valor percebido, aplicável tanto para vendas casadas quanto para captação de clientes de qualquer setor:",
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
            Paragraph("Negócios iniciando no tráfego (mínimo R$ 30/dia em ads)", body_style),
            Paragraph("<b>R$ 399,00 / mês</b>", body_style),
            Paragraph("Esteira contínua de criativos, proteção 24h de Stop-Loss e aprovações via WhatsApp", body_style)
        ],
        [
            Paragraph("<b>Growth (Escala)</b>", body_style),
            Paragraph("Empresas consolidadas com alto volume de vendas", body_style),
            Paragraph("<b>R$ 799 a R$ 899 / mês</b>", body_style),
            Paragraph("Volume estendido de criativos semanais, escala de orçamento e auditorias avançadas", body_style)
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

    comp_box = [
        [Paragraph("<b>Comparativo com o Mercado Tradicional:</b>", card_header_style)],
        [Paragraph(
            "• <b>Agências / Gestores Humanos:</b> Cobram de R$ 2.000 a R$ 4.000/mês, demoram dias para subir um anúncio e atendem dezenas de clientes sem dedicação exclusiva.<br/>"
            "• <b>Nossa Tecnologia:</b> A partir de R$ 399/mês, velocidade instantânea, personalização para qualquer nicho e vigilância financeira 24h por dia.",
            bullet_style
        )],
        [Paragraph("<b>Potencial de Recorrência (MRR):</b>", card_header_style)],
        [Paragraph(
            "• <b>30 empresas ativas:</b> R$ 11.970,00 / mês<br/>"
            "• <b>50 empresas ativas:</b> R$ 19.950,00 / mês<br/>"
            "• <b>100 empresas ativas:</b> R$ 39.900,00 / mês<br/>"
            "<i>(Aplicável a lojistas de moda, cosméticos, eletrônicos, infoprodutores e serviços locais em todo o Brasil).</i>",
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
    print(f"[OK] PDF Multicategoria gerado com sucesso em: {filename}")


if __name__ == "__main__":
    out_dir = "C:/Users/Pichau/Documents/traffic-copilot-ai/docs"
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, "Traffic_Copilot_AI_Apresentacao_Executiva.pdf")
    build_pdf(pdf_path)
