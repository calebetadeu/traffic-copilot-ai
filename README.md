# Traffic Copilot AI 🚀

> **Gestor Autônomo de Tráfego Pago com IA para E-commerce e Moda**  
> Criação contínua de criativos, execução segura via Meta Marketing API e otimização autônoma 24/7 com stop-loss e interface via WhatsApp.

---

## 🎯 Proposta de Valor
* **Esteira Infinita de Criativos:** IA multimodal analisa fotos/vídeos de produtos de vestuário e gera 10+ variações com ganchos de alta conversão.
* **Stop-Loss de Trader:** Sentinela em tempo real que monitora CPA, CTR e ROAS a cada hora, pausando anúncios perdedores e escalando vencedores.
* **Copiloto no WhatsApp:** O lojista aprova campanhas e recebe resumos de vendas diários direto no celular.
* **Segurança e Anti-Bloqueio:** Travas físicas de orçamento no código e filtros de políticas da Meta.

---

## 🛠️ Stack Tecnológica
* **Linguagem:** Python 3.11+
* **Framework:** FastAPI
* **IA Multimodal:** Google Gemini 2.0 Flash (`google-genai`)
* **Processamento Visual:** Pillow (PIL) + Rembg
* **Agendamento de Tarefas:** APScheduler
* **Banco de Dados:** SQLModel (SQLite / PostgreSQL)
* **Integrações:** Meta Marketing API (Graph API v21.0) & Evolution API (WhatsApp)

---

## 📂 Estrutura do Projeto

```
traffic-copilot-ai/
├── src/
│   ├── api/            # Webhooks do WhatsApp e rotas REST
│   ├── core/           # Configurações, segurança e scheduler
│   ├── models/         # Schemas do banco (Clientes, Campanhas, Métricas)
│   ├── services/       # Gemini, Meta API, Image Engine, Stop-loss
│   └── main.py         # Entrypoint FastAPI
├── docs/               # Documentação técnica e arquitetura
├── tests/              # Testes unitários e de integração
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚦 Roadmap de Versões
- [x] **v0.1.0-alpha:** Inicialização do repositório e arquitetura de software.
- [ ] **v0.2.0:** Motor de criativos com Gemini Multimodal (Copy + Visual).
- [ ] **v0.3.0:** Integração com Meta Marketing API (Leitor de Insights & Auditor de DNA).
- [ ] **v0.4.0:** Sentinela de Stop-Loss & Escala com APScheduler.
- [ ] **v0.5.0:** Webhook do WhatsApp (Fluxo completo de aprovação).

---

## 📄 Licença
Propriedade privada de Calebe Tadeu. Todos os direitos reservados.
