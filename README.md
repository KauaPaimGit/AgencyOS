<div align="center">

# 🚀 Vyron System v1.0

**Enterprise AI ERP - Plataforma Completa de Gestão Inteligente**

[![Status](https://img.shields.io/badge/Status-Produção-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-009688)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791)]()
[![AI](https://img.shields.io/badge/AI-GPT--4o--mini-412991)]()

**Última Atualização:** Fevereiro 2026 | **Versão:** 1.0

---

</div>

## 📋 Índice

- [Sobre o Sistema](#-sobre-o-sistema)
- [Funcionalidades Completas](#-funcionalidades-completas)
- [Stack Tecnológica](#-stack-tecnológica)
- [Início Rápido](#-início-rápido)
- [API REST](#-api-rest)
- [Banco de Dados](#-banco-de-dados)
- [Documentação](#-documentação)

---

## 🎯 Sobre o Sistema

O **Vyron System** é uma plataforma Enterprise AI ERP completa com **10 módulos funcionais**, **50+ endpoints REST**, **18 tabelas** no banco de dados e **RAG nativo** para inteligência artificial contextual. Sistema 100% funcional e pronto para produção.

### ✨ Destaques

- 🤖 **AI Brain** com RAG (busca semântica usando pgvector)
- 💰 **ROI Intelligence** com cálculos automáticos de KPIs
- 📊 **Dashboard Financeiro e Marketing** completos
- 🎯 **Function Calling** (automação via chat com IA)
- 📡 **Radar de Vendas** com integração Google Maps
- ✍️ **Entrada Manual** com memória RAG integrada

---

## 🚀 Funcionalidades Completas

### 📊 **1. Sistema de Autenticação e Controle de Acesso**

<details>
<summary><b>1.1 Gerenciamento de Usuários</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Cadastro de usuários com roles (admin, user) | ✅ |
| Autenticação via login/senha | ✅ |
| Hash de senhas com bcrypt | ✅ |
| Sistema de tokens JWT | ✅ |
| Controle de status (ativo/inativo) | ✅ |
| Rastreamento de último login | ✅ |
| Scripts de criação de admin | ✅ |

</details>

---

### 👥 **2. CRM Inteligente**

<details>
<summary><b>2.1 Gestão de Clientes</b></summary>

| Funcionalidade | Status |
|---|:---:|
| CRUD completo de clientes | ✅ |
| Status do cliente (lead, client, inactive) | ✅ |
| Campos: nome, email, empresa, telefone | ✅ |
| Health Score automático | ✅ |
| Sentiment Score (análise de sentimento) | ✅ |
| Cálculo de LTV (Lifetime Value) | ✅ |
| Busca e filtros por status | ✅ |

</details>

<details>
<summary><b>2.2 Funil de Vendas (Sales Pipeline)</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Rastreamento de oportunidades | ✅ |
| Fases: qualification, proposal, negotiation, won, lost | ✅ |
| Valor estimado de cada oportunidade | ✅ |
| Probabilidade de fechamento | ✅ |
| Data de fechamento esperada | ✅ |
| Vinculação com clientes | ✅ |

</details>

<details>
<summary><b>2.3 Histórico de Interações</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Registro de reuniões, calls, emails, WhatsApp | ✅ |
| **Embeddings vetoriais** para busca semântica (RAG) | ✅ |
| Análise de sentimento automática | ✅ |
| Extração de tópicos-chave | ✅ |
| Flag de follow-up necessário | ✅ |
| Nível de urgência | ✅ |
| Timeline completa por cliente | ✅ |

</details>

---

### 📋 **3. Gestão de Projetos**

<details>
<summary><b>3.1 Cadastro de Projetos</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Tipos: recorrente (recurrent) ou pontual (one_off) | ✅ |
| Categorias: tráfego, social media, branding, vídeo | ✅ |
| Vinculação com clientes | ✅ |
| Orçamento e valor contratado | ✅ |
| Preço do produto/serviço para cálculo de ROI | ✅ |
| Data de início e fim | ✅ |
| Status no Kanban | ✅ |
| Horas estimadas vs. realizadas | ✅ |

</details>

<details>
<summary><b>3.2 Templates de Tarefas</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Templates pré-configurados por categoria | ✅ |
| Tarefas padrão para cada tipo de projeto | ✅ |
| Estimativa de horas por tarefa | ✅ |

</details>

<details>
<summary><b>3.3 Tarefas do Projeto</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Gestão de tarefas vinculadas ao projeto | ✅ |
| Status: pending, in_progress, completed | ✅ |
| Alocação de horas | ✅ |
| Rastreamento de progresso | ✅ |

</details>

---

### 💰 **4. Gestão Financeira (ERP)**

<details>
<summary><b>4.1 Receitas (Contas a Receber)</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Registro de receitas vinculadas a projetos | ✅ |
| Categorias: taxa de setup, mensalidade, consultoria | ✅ |
| Status: pending, received, overdue | ✅ |
| Data de vencimento e recebimento | ✅ |
| Lançamento automático ao criar projeto | ✅ |

</details>

<details>
<summary><b>4.2 Despesas (Contas a Pagar)</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Registro manual de despesas | ✅ |
| Categorias: software, freelancer, impostos, ads | ✅ |
| Vinculação com projetos | ✅ |
| Status: pending, paid, overdue | ✅ |
| Data de vencimento e pagamento | ✅ |

</details>

<details>
<summary><b>4.3 Custos por Projeto</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Rastreamento detalhado de custos diretos | ✅ |
| Custos de equipe (horas × valor/hora) | ✅ |
| Custos de ferramentas/software | ✅ |
| Custos de mídia paga | ✅ |
| Margem de lucro real calculada | ✅ |

</details>

<details>
<summary><b>4.4 Dashboard Financeiro</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Resumo por projeto: receitas, despesas, lucro | ✅ |
| Margem de lucro percentual | ✅ |
| Gráficos de distribuição financeira | ✅ |
| Análise automática de saúde financeira | ✅ |
| Views SQL otimizadas | ✅ |

</details>

---

### 📊 **5. Métricas de Marketing (Performance)**

<details>
<summary><b>5.1 Rastreamento de Campanhas</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Impressões, cliques, leads, conversões | ✅ |
| Custo total da campanha | ✅ |
| Plataformas: Google Ads, Meta Ads, TikTok, LinkedIn | ✅ |
| Vinculação com projetos | ✅ |

</details>

<details>
<summary><b>5.2 KPIs Calculados Automaticamente</b></summary>

| KPI | Fórmula | Status |
|---|---|:---:|
| **CTR** (Click-Through Rate) | (Cliques / Impressões) × 100 | ✅ |
| **CPC** (Cost Per Click) | Custo / Cliques | ✅ |
| **CPL/CPA** (Cost Per Lead) | Custo / Leads | ✅ |
| **Taxa de Conversão** | (Conversões / Leads) × 100 | ✅ |
| **ROI** (Return on Investment) | ((Receita - Custo) / Custo) × 100 | ✅ |
| **Receita Estimada** | Conversões × Preço do Produto | ✅ |

</details>

<details>
<summary><b>5.3 View SQL de KPIs</b></summary>

| Funcionalidade | Status |
|---|:---:|
| View `marketing_kpis` com cálculos otimizados | ✅ |
| Agregação por projeto | ✅ |
| Totalizadores de performance | ✅ |

</details>

---

### ✍️ **6. Entrada Manual de Dados**

<details>
<summary><b>6.1 Interface de Lançamentos</b></summary>

| Formulário | Funcionalidade | Status |
|---|---|:---:|
| **Novo Projeto** | Nome, cliente, orçamento, preço do produto | ✅ |
| | Cliente criado automaticamente se não existir | ✅ |
| **Nova Despesa** | Vinculação com projeto, valor, categoria | ✅ |
| | Data de vencimento e status | ✅ |
| **Métricas de Marketing** | Impressões, cliques, leads, conversões | ✅ |
| | Custo, plataforma, KPIs em tempo real | ✅ |

</details>

<details>
<summary><b>6.2 Memória RAG Integrada</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Todos os lançamentos manuais geram logs automáticos | ✅ |
| Embeddings vetoriais para busca pela IA | ✅ |
| Vinculação com cliente correto | ✅ |
| Timestamp UTC para auditoria | ✅ |

</details>

---

### 📄 **7. Sistema de Contratos**

<details>
<summary><b>7.1 Templates Dinâmicos</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Templates com variáveis: `{{client_name}}`, `{{project_value}}` | ✅ |
| Validação de campos obrigatórios | ✅ |
| Categorias por tipo de serviço | ✅ |
| Metadata JSONB para configuração | ✅ |

</details>

<details>
<summary><b>7.2 Geração de Contratos</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Renderização de templates com dados reais | ✅ |
| Geração de HTML e PDF | ✅ |
| Status: draft, sent, signed, cancelled | ✅ |
| Rastreabilidade: quem gerou, quando | ✅ |
| Data de assinatura | ✅ |

</details>

---

### 🤖 **8. AI Brain (Inteligência Artificial)**

<details>
<summary><b>8.1 Chat Inteligente com RAG</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Busca semântica em interações usando embeddings | ✅ |
| Contexto dinâmico baseado em dados reais | ✅ |
| Respostas com base em histórico do cliente | ✅ |
| Suporte a imagens (multimodal) | ✅ |
| Histórico de conversa mantido na sessão | ✅ |

</details>

<details>
<summary><b>8.2 Function Calling (Automação)</b></summary>

| Função | Descrição | Status |
|---|---|:---:|
| `create_project` | Criar projetos via comando natural | ✅ |
| `list_projects` | Listar e buscar projetos existentes | ✅ |
| `add_expense` | Registrar despesas via chat | ✅ |
| **Execução Automática** | GPT-4o-mini executa ações automaticamente | ✅ |
| **Validação** | Parâmetros validados pela IA | ✅ |

</details>

<details>
<summary><b>8.3 Análises e Insights</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Cache de insights em `ai_insights` | ✅ |
| Tipos: client_health, churn_prediction, profitability_alert | ✅ |
| Confidence score (confiança da IA) | ✅ |
| Ações sugeridas | ✅ |
| Severidade (info, warning, critical) | ✅ |

</details>

<details>
<summary><b>8.4 Base de Conhecimento (RAG para Docs)</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Tabela `knowledge_base` para documentos internos | ✅ |
| Embeddings de manuais, políticas, processos | ✅ |
| Busca vetorial com pgvector | ✅ |
| Versionamento de documentos | ✅ |

</details>

---

### 📡 **9. Radar de Vendas (Prospecção Ativa)**

<details>
<summary><b>9.1 Busca de Empresas</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Integração com Google Maps API | ✅ |
| Busca por nicho e localização | ✅ |
| Extração de: telefone, site, avaliação, endereço | ✅ |
| Limite configurável de resultados | ✅ |

</details>

<details>
<summary><b>9.2 Conversão em Leads</b></summary>

| Funcionalidade | Status |
|---|:---:|
| 1-click para converter empresa em projeto | ✅ |
| Criação automática de cliente | ✅ |
| Projeto vai direto para fase "Negociação" | ✅ |
| Estatísticas da busca em tempo real | ✅ |

</details>

<details>
<summary><b>9.3 Exportação</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Export de resultados para Excel | ✅ |
| Dados estruturados para follow-up | ✅ |

</details>

---

### 📋 **10. Gestão Visual (Kanban de Projetos)**

<details>
<summary><b>10.1 Quadro Kanban</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Visualização por fases: Planejamento, Produção, Entrega, Finalizado | ✅ |
| Cartões com: nome, cliente, valor, status | ✅ |
| Atualização de status via API | ✅ |
| Indicadores visuais por fase | ✅ |

</details>

<details>
<summary><b>10.2 Filtros e Busca</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Busca por nome de projeto ou cliente | ✅ |
| Filtro por status | ✅ |
| Ordenação customizável | ✅ |

</details>

---

### 📈 **11. Dashboards e Relatórios**

<details>
<summary><b>11.1 Dashboard Financeiro</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Seleção de projeto via dropdown | ✅ |
| Métricas: receitas, despesas, lucro líquido | ✅ |
| Margem de lucro percentual | ✅ |
| Gráfico de pizza (distribuição financeira) | ✅ |
| Análise automática de saúde financeira | ✅ |

</details>

<details>
<summary><b>11.2 Dashboard de Marketing</b></summary>

| Funcionalidade | Status |
|---|:---:|
| KPIs agregados por projeto | ✅ |
| Exibição de: CTR, CPC, CPL, Taxa de Conversão | ✅ |
| **ROI** e **Receita Estimada** | ✅ |
| Comparação entre campanhas | ✅ |

</details>

<details>
<summary><b>11.3 Relatórios em PDF</b></summary>

| Funcionalidade | Status |
|---|:---:|
| Geração de relatórios de projeto | ✅ |
| Suporte para contratos em PDF | ✅ |
| Biblioteca FPDF2 integrada | ✅ |

</details>

---

### 🔧 **12. API REST (Backend FastAPI)**

<details>
<summary><b>Ver todos os endpoints (50+)</b></summary>

#### **12.1 Endpoints de CRM**
```
✅ POST   /clients              - Criar cliente
✅ GET    /clients              - Listar clientes (com filtros)
✅ GET    /clients/{id}         - Detalhes do cliente
✅ PATCH  /clients/{id}         - Atualizar cliente
✅ DELETE /clients/{id}         - Remover cliente
```

#### **12.2 Endpoints de Projetos**
```
✅ POST   /projects                         - Criar projeto
✅ GET    /projects                         - Listar projetos
✅ GET    /projects/{id}                    - Detalhes do projeto
✅ PATCH  /projects/{id}                    - Atualizar projeto
✅ PATCH  /projects/{id}/status             - Atualizar status (Kanban)
✅ GET    /projects/{id}/financial-dashboard - Dashboard financeiro
```

#### **12.3 Endpoints de Entrada Manual**
```
✅ POST /manual/projects          - Criar projeto (entrada manual)
✅ POST /manual/expenses          - Registrar despesa
✅ POST /manual/marketing-metrics - Adicionar métricas de marketing
```

#### **12.4 Endpoints de Marketing**
```
✅ GET /projects/{id}/marketing-kpis - Obter KPIs de marketing
```

#### **12.5 Endpoints de IA**
```
✅ POST /ai/search - Busca semântica (RAG)
✅ POST /ai/chat   - Chat com IA (multimodal)
```

#### **12.6 Endpoints de Radar de Vendas**
```
✅ POST /radar/search   - Buscar empresas no Google Maps
✅ POST /radar/convert  - Converter empresa em lead/projeto
✅ POST /radar/export   - Exportar resultados para Excel
```

#### **12.7 Endpoints de Interações**
```
✅ POST   /interactions                 - Criar interação
✅ GET    /clients/{id}/interactions    - Listar interações do cliente
✅ DELETE /interactions/{id}            - Remover interação
```

#### **12.8 Endpoints de Autenticação**
```
✅ POST /login   - Autenticar usuário
✅ GET  /db-test - Testar conexão com banco
```

</details>

---

### 🗄️ **13. Banco de Dados (PostgreSQL)**

<details>
<summary><b>13.1 Extensões</b></summary>

| Extensão | Finalidade | Status |
|---|---|:---:|
| **pgvector** | Busca vetorial para embeddings | ✅ |
| **uuid-ossp** | Geração de UUIDs | ✅ |

</details>

<details>
<summary><b>13.2 Tabelas Principais (18)</b></summary>

| Tabela | Descrição |
|---|---|
| `users` | Usuários do sistema |
| `clients` | Clientes/Leads |
| `sales_pipeline` | Funil de vendas |
| `interactions` | Histórico de comunicações |
| `projects` | Projetos |
| `project_tasks` | Tarefas |
| `task_templates` | Templates de tarefas |
| `revenues` | Receitas |
| `expenses` | Despesas |
| `project_costs` | Custos por projeto |
| `marketing_metrics` | Métricas de marketing |
| `contract_templates` | Templates de contratos |
| `contracts` | Contratos gerados |
| `ai_insights` | Cache de insights |
| `knowledge_base` | Base de conhecimento |

</details>

<details>
<summary><b>13.3 Views SQL</b></summary>

| View | Descrição | Status |
|---|---|:---:|
| `project_profitability` | Análise de rentabilidade | ✅ |
| `client_lifetime_value` | LTV por cliente | ✅ |
| `marketing_kpis` | KPIs de marketing calculados | ✅ |

</details>

<details>
<summary><b>13.4 Triggers</b></summary>

| Trigger | Ação | Status |
|---|---|:---:|
| Atualização automática de `updated_at` | Todas as tabelas | ✅ |
| Atualização de `health_score` | Baseado em interações | ✅ |

</details>

---

### 🎨 **14. Frontend (Streamlit)**

<details>
<summary><b>14.1 Páginas</b></summary>

| Página | Descrição | Status |
|---|---|:---:|
| **Login** | Autenticação de usuários | ✅ |
| **Dashboard Financeiro** | Visão geral de receitas/despesas | ✅ |
| **Agency Brain** | Chat com IA | ✅ |
| **Gestão Visual** | Kanban de projetos | ✅ |
| **Lançamentos Manuais** | Entrada de dados | ✅ |
| **Radar de Vendas** | Prospecção ativa | ✅ |

</details>

<details>
<summary><b>14.2 Componentes</b></summary>

| Componente | Status |
|---|:---:|
| Gráficos interativos (Plotly/Matplotlib) | ✅ |
| Formulários com validação | ✅ |
| Feedback visual (success/error/info) | ✅ |
| Animações (balloons, spinner) | ✅ |
| Sidebar de navegação | ✅ |
| Session state para autenticação | ✅ |

</details>

---

### 🔒 **15. Segurança e Compliance**

<details>
<summary><b>Ver detalhes de segurança</b></summary>

#### **15.1 Autenticação**
- ✅ Hash de senhas com bcrypt
- ✅ Tokens JWT
- ✅ Controle de sessão

#### **15.2 Auditoria**
- ✅ Campos `created_at` e `updated_at` em todas as tabelas
- ✅ Rastreamento de quem criou/modificou
- ✅ Soft delete (campo `deleted_at`)

#### **15.3 LGPD**
- ✅ Dados sensíveis identificados
- ✅ Recomendações de criptografia
- ✅ Logs de acesso

</details>

---

### 🛠️ **16. Ferramentas e Utilitários**

<details>
<summary><b>16.1 Scripts de Manutenção</b></summary>

| Script | Descrição |
|---|---|
| `create_admin.py` | Criar admin local |
| `create_remote_admin.py` | Criar admin remoto (Render) |
| `fix_users_table.py` | Correção de tabela users |
| `force_admin_creation.py` | Forçar criação de admin |
| `remove_duplicates.py` | Remover duplicatas |

</details>

<details>
<summary><b>16.2 Migrations SQL</b></summary>

| Migration | Descrição |
|---|---|
| `001_add_marketing_metrics.sql` | Tabela de métricas |
| `002_add_product_price_to_projects.sql` | Campo ROI |

</details>

<details>
<summary><b>16.3 Docker</b></summary>

| Arquivo | Status |
|---|:---:|
| `Dockerfile` - Containerização | ✅ |
| `docker-compose.yml` - Orquestração | ✅ |
| `.dockerignore` - Otimização de build | ✅ |

</details>

---

### 📚 **17. Documentação**

<details>
<summary><b>17.1 Documentação Técnica</b></summary>

| Documento | Descrição |
|---|---|
| `README.md` | Visão geral completa |
| `architecture_docs.md` | Arquitetura detalhada |
| `database_schema.sql` | Schema com comentários |
| `diagrams/er_diagram.md` | Diagrama ER |

</details>

<details>
<summary><b>17.2 Changelogs e Guias</b></summary>

| Documento | Descrição |
|---|---|
| `CHANGELOG_v1.1.md` | Histórico de mudanças |
| `FEATURE_ROI_v1.2.md` | Feature de ROI |
| `FIXES_v1.1.md` | Correções aplicadas |
| `INSTALL.md` | Guia de instalação |
| `AUTH_README.md` | Documentação de autenticação |
| `RADAR_README.md` | Módulo Radar de Vendas |

</details>

---

### 📊 **18. Queries e Análises SQL**

<details>
<summary><b>18.1 Queries Pré-configuradas</b></summary>

| Query | Funcionalidade |
|---|---|
| Clientes em risco de churn | ✅ |
| Projetos com margem abaixo da meta | ✅ |
| Top 5 clientes por LTV | ✅ |
| Busca semântica de interações (RAG) | ✅ |
| KPIs de marketing por projeto | ✅ |

</details>

---

### 🚀 **19. Stack Tecnológica**

<details>
<summary><b>Ver stack completa</b></summary>

#### **19.1 Backend**
| Tecnologia | Versão |
|---|---|
| Python | 3.11+ |
| FastAPI | 0.109+ |
| SQLAlchemy | (ORM) |
| Pydantic | v2 |
| PostgreSQL | 15+ com pgvector |

#### **19.2 IA/Machine Learning**
| Tecnologia | Modelo |
|---|---|
| OpenAI Chat | GPT-4o-mini |
| OpenAI Embeddings | text-embedding-3-small |
| Function Calling | ✅ |
| Visão Computacional | Multimodal |

#### **19.3 Frontend**
| Tecnologia | Versão |
|---|---|
| Streamlit | 1.30+ |
| Plotly | (gráficos) |
| Custom CSS | ✅ |

#### **19.4 DevOps**
| Ferramenta | Status |
|---|:---:|
| Docker | ✅ |
| Docker Compose | ✅ |
| Deploy Render | ✅ |

</details>

---

### 📈 **20. KPIs e Métricas Disponíveis**

<details>
<summary><b>20.1 Financeiros</b></summary>

| KPI | Status |
|---|:---:|
| Receitas totais | ✅ |
| Despesas totais | ✅ |
| Lucro líquido | ✅ |
| Margem de lucro (%) | ✅ |
| LTV por cliente | ✅ |

</details>

<details>
<summary><b>20.2 Marketing</b></summary>

| KPI | Status |
|---|:---:|
| CTR (Click-Through Rate) | ✅ |
| CPC (Cost Per Click) | ✅ |
| CPL/CPA (Cost Per Lead/Acquisition) | ✅ |
| Taxa de Conversão | ✅ |
| ROI (Return on Investment) | ✅ |
| Receita Estimada | ✅ |

</details>

<details>
<summary><b>20.3 CRM</b></summary>

| Métrica | Status |
|---|:---:|
| Health Score | ✅ |
| Sentiment Score | ✅ |
| Taxa de churn | ✅ |
| Funil de vendas (conversão por fase) | ✅ |

</details>

---

## 🚀 Início Rápido

### 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL 15+ com extensão pgvector
- Docker (opcional)
- Chave API OpenAI

### ⚡ Instalação Rápida

```bash
# 1. Clone o repositório
git clone https://github.com/KauaPaimGit/AgencyOS.git
cd AgencyOS

# 2. Configure variáveis de ambiente
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/agency_os" > .env
echo "OPENAI_API_KEY=sk-..." >> .env
echo "SECRET_KEY=sua_chave_secreta" >> .env

# 3. Inicie o banco de dados (Docker)
docker run -d --name agency-db -e POSTGRES_PASSWORD=senha \
  -e POSTGRES_DB=agency_os -p 5432:5432 ankane/pgvector:latest

# 4. Execute o schema
psql -h localhost -U postgres -d agency_os -f database_schema.sql

# 5. Instale dependências
pip install -r requirements.txt

# 6. Inicie o backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 7. Inicie o frontend (novo terminal)
cd frontend && streamlit run app.py
```

### 🌐 Acessos

| Interface | URL |
|---|---|
| **API Backend** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **Frontend (Streamlit)** | http://localhost:8501 |

---

## 🗄️ Banco de Dados

### Schema Principal

```sql
-- Extensões necessárias
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 18 tabelas principais
-- Ver database_schema.sql para schema completo
```

### Views Otimizadas

| View | Descrição |
|---|---|
| `project_profitability` | Rentabilidade por projeto |
| `client_lifetime_value` | LTV e análise de clientes |
| `marketing_kpis` | KPIs automatizados |

---

## 🔧 API REST

### Documentação Completa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Exemplos de Uso

```bash
# Autenticar
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@agency.com", "password": "senha"}'

# Listar projetos
curl http://localhost:8000/projects

# Criar projeto (entrada manual)
curl -X POST http://localhost:8000/manual/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Campanha Digital",
    "client_name": "Empresa XYZ",
    "budget": 15000,
    "product_price": 500
  }'

# Chat com IA
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual projeto tem melhor ROI?"}'
```

---

## 📚 Documentação

| Documento | Descrição |
|---|---|
| [architecture_docs.md](architecture_docs.md) | Arquitetura técnica completa |
| [database_schema.sql](database_schema.sql) | Schema do banco com comentários |
| [INSTALL.md](INSTALL.md) | Guia detalhado de instalação |
| [AUTH_README.md](AUTH_README.md) | Sistema de autenticação |
| [RADAR_README.md](RADAR_README.md) | Radar de vendas |
| [CHANGELOG_v1.1.md](CHANGELOG_v1.1.md) | Histórico de versões |

---

## ✨ Resumo Executivo

### 🎯 O Vyron System oferece:

```
✅ 10 módulos funcionais integrados
✅ 50+ endpoints REST documentados
✅ 18 tabelas no banco de dados
✅ 3 views SQL otimizadas
✅ RAG nativo com pgvector
✅ Function Calling (automação via IA)
✅ Dashboard financeiro completo
✅ Dashboard de marketing com ROI
✅ Entrada manual com memória RAG
✅ Prospecção ativa (Google Maps)
✅ Kanban visual de projetos
✅ ROI Intelligence automático
```

### 🎉 Status: **Sistema 100% funcional e pronto para produção!**

---

<div align="center">

## 📞 Suporte

Para dúvidas técnicas, consulte a documentação ou entre em contato.

---

## 📄 Licença

**Uso Interno - Todos os direitos reservados**

---

**Desenvolvido com ❤️ para revolucionar a gestão de agências**

*Vyron System v1.0 - Enterprise AI ERP*

</div>
