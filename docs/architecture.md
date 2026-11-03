# Especificação Técnica: Agente de Tráfego Autônomo para E-commerce

Este documento detalha as funcionalidades, stack tecnológica, fluxo de dados e arquitetura de software para o **Agente Autônomo de Tráfego Pago** voltado para o nicho de vestuário/moda, integrando WhatsApp, Meta Marketing API e IA Multimodal.

---

## 1. Elenco de Funcionalidades (O que o sistema faz)

O sistema é dividido em **6 módulos essenciais**:

### Módulo 1: Onboarding e Auditoria de DNA (Zero Setup Manual)
* **1.1 Varredura de Histórico Meta:** Conecta via API à conta do cliente e puxa os últimos 3 a 6 meses de métricas (`GET /insights`).
* **1.2 Extração dos Campeões:** Filtra os anúncios com maior ROAS e menor CPA.
* **1.3 Síntese do DNA de Marca:** O Gemini analisa os criativos campeões + histórico do ChatGPT do cliente e extrai:
  * Tom de voz da marca;
  * Dores e argumentos do público-alvo;
  * Regiões de maior conversão;
  * CPA teto aceitável.

### Módulo 2: Motor de Criativos (A Máquina de Opções)
* **2.1 Ingestão Multimodal:** Recebe fotos ou vídeos brutos das camisas enviados pelo cliente no WhatsApp.
* **2.2 Geração de Copys Blindadas:** Gera 10 variações diárias com ganchos diferentes (estilo, caimento, tecido, oferta). Passa por filtro anti-bloqueio de políticas da Meta.
* **2.3 Processamento Visual Automatizado:** 
  * Redimensionamento para Feed (1:1 / 4:5) e Stories/Reels (9:16);
  * Remoção de fundo (`rembg`);
  * Aplicação de templates dinâmicos (Selos "Frete Grátis", "Compre 2 Leve 3", avaliações).

### Módulo 3: Despachante Meta Ads (Execução Segura)
* **3.1 Montagem de Campanhas:** Criação de campanha, conjunto de anúncios e criativos dinâmicos (formato 3:2:2).
* **3.2 Modo Rascunho / Aprovação:** Nenhum anúncio entra em `ACTIVE` sem a confirmação do cliente. Cria como `PAUSED`.
* **3.3 Travas Físicas de Orçamento:** Verificação no código que impede definir orçamento acima do limite acordado (ex: R$ 30 - R$ 50/dia por conjunto).

### Módulo 4: Sentinela de Otimização ("Stop-Loss de Trader")
* **4.1 Monitoramento de Hora em Hora:** Polling de métricas da Meta via agendador em background.
* **4.2 Regra de Stop-Loss:** Se um criativo gastar 1x o CPA teto (ex: R$ 35) com zero vendas, o robô pausa o anúncio automaticamente.
* **4.3 Regra de Escala:** Se o anúncio tiver ROAS > 3.0 e CPA saudável, o robô notifica o lojista e sugere aumento de orçamento de 15% a 20%.

### Módulo 5: Interface Conversacional no WhatsApp (O Copiloto)
* **5.1 Recebimento via Webhook:** Escuta fotos, textos e áudios enviados pelo cliente.
* **5.2 Aprovação em 1 Clique:** Envia preview do anúncio + botão ou comando numérico: `[1] Aprovar`, `[2] Ajustar texto`.
* **5.3 Resumo Diário às 20h:** Mensagem com gasto do dia, faturamento e ROAS.

### Módulo 6: Gestão Multi-Tenant & Trava de Inadimplência
* **6.1 Multi-Tenancy:** Estrutura preparada para gerenciar múltiplos lojistas simultaneamente (Alexandre + clientes da base).
* **6.2 Kill-Switch de Mensalidade:** Se o status da assinatura for `inadimplente`, a automação é suspensa (não sobe novos anúncios nem otimiza).

---

## 2. Stack Tecnológica (A Escolha para Vibe Coding)

| Camada | Tecnologia Escolhida | Justificativa Técnica |
| :--- | :--- | :--- |
| **Linguagem** | **Python 3.11+** | Ecossistema padrão de IA, processamento de imagem, tipagem moderna e libs de dados. |
| **Web Framework** | **FastAPI** | Ultra rápido, assíncrono (`async/await`), validação nativa com Pydantic e documentação Swagger automática. |
| **IA / Cérebro** | **Google Gemini 2.0 Flash** (`google-genai`) | Multimodal nativo (analisa foto/vídeo + texto), structured output garantido (JSON), ultra rápido e custo insignificante. |
| **Processamento Visual** | **Pillow (PIL) + Rembg** | Manipulação rápida de imagens, aplicação de selos/banners e remoção de fundo com IA local. |
| **Agendador de Tarefas** | **APScheduler** | Roda dentro do próprio processo Python em background (tarefas a cada 1h para stop-loss e crons diários). |
| **Banco de Dados** | **SQLite (Dev) ➔ PostgreSQL / Supabase (Prod)** | Simples de rodar localmente no início com SQLAlchemy/SQLModel; fácil migração para PostgreSQL. |
| **Meta Ads SDK** | **HTTPX / Requests Assíncrono** | Controle total de chamadas REST na Graph API v21.0 sem complexidade desnecessária de SDKs legados. |
| **Gateway WhatsApp** | **Evolution API (Docker)** | API open-source que conecta um WhatsApp ao FastAPI via Webhook sem custo por mensagem. |
