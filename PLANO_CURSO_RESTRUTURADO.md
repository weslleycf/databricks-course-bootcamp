# 🎓 Plano de Curso Reestruturado — Especialista Databricks
**Versão**: Agosto 2026 | **Duração**: 22 semanas (19 núcleo + 3 bônus opcionais) | **Dedicação**: 2–3h/dia, 6 dias/semana
**Objetivo**: do zero absoluto ao **Especialista Databricks requisitado no mercado internacional** — engenharia de dados, governança, ML/MLOps, GenAI, agentes, apps e Lakebase — preparado para as certificações oficiais (DEA, DEP, GenAI Engineer Associate, MLP) e para entrevistas técnicas em inglês.
**Pré-requisitos**: SQL e Python básicos. Zero conhecimento de Spark/Databricks/IA.

---

## 1. O que mudou e por quê (análise do plano original)

| Problema no fluxo original | Correção nesta versão | Benefício |
|---|---|---|
| GenAI/agentes (sem. 4–7) intercalados com DE avançado (sem. 8–9) | Toda a engenharia de dados primeiro (1–10), depois GenAI (11–13), agentes (14–15) | Sem lacunas: RAG usa Prata/Ouro prontos; SCD/CDC não dependem de conhecimento de IA |
| DABs na semana 3 sem ensinar Git | Git/GitHub na Semana 2, Repos + DABs na Semana 6 | Deploy versionado sem "pular etapas" |
| MLflow espalhado e tardio | Semana 10 dedicada (experiments, registry, evaluate) ANTES da avaliação de RAG | `mlflow.evaluate` e tracing exigem base; também prepara MLP |
| Sem SQL analítico/BI no início | Semanas 1–2: SQL profundo + Databricks SQL + dashboards + Genie | DEA 2026 é "ELT with Spark SQL and Python"; analistas são o mercado mais amplo |
| Modelagem dimensional só na Semana 8 | Conceitos na Semana 2, star schema real na Semana 4, SCD na Semana 8 | Progressão natural: conceito → prática → evolução |
| Streaming só na Semana 8 | Auto Loader + Structured Streaming na Semana 5 | CDC/SCD da Semana 8 dependem de streaming; DLT (Semana 5) também |
| Spark internals (shuffle, AQE, DAG) só na Semana 8 | Fundamentos na Semana 3, aprofundamento de tuning na Semana 8 | Tuning com base, não decoreba |
| Módulo "Novidades DAIS 2026" isolado (sem. 19–20) | Integrado como callouts no contexto de cada semana | Aprender no contexto real; nada de aula de "notícias" |
| Módulo 4 (app YAML) obrigatório no fim | Mantido como **capstone opcional** (sem. 20–22) | Núcleo fica enxuto; quem quiser portfólio empresarial faz |
| Certificação MLP apenas tocada | Semana 10 + 13 cobrem Feature Engineering, Model Serving, Lakehouse Monitoring | 4ª certificação alcançável; exigida em vagas sênior |
| Sem conteúdo de plataforma (CLI, REST API, system tables, Federation, Delta Sharing) | Espalhado nas Semanas 6–9 | Perfil de administrador/plataforma, cobrado em entrevistas |

**Adições para o mercado internacional**: Spark Connect + pandas API (Spark Dev Assoc 2026), Lakehouse Federation, Delta Sharing, serverless + Lakeflow Connect (DEP 2026), custos/observabilidade profunda, glossário EN-PT, simulados alinhados aos domínios 2026, 30 perguntas de entrevista em inglês e salários US/EU/UK.

---

## 2. Mapa de dependências (sem lacunas nem pré-requisitos não cobertos)

| Semana | Depende de | Por quê |
|---|---|---|
| 2 (SQL avançado, Git, modelagem) | 1 | SQL é a língua da plataforma; Git é pré-requisito do DABs |
| 3 (Spark) | 1–2 | Spark SQL pressupõe SQL; DEA exige "ELT with Spark SQL and Python" |
| 4 (Delta + Medallion) | 3 | Transformações Spark são o motor da Medallion |
| 5 (Auto Loader, Streaming, DLT, Jobs) | 3–4 | DLT consome tabelas Delta/Spark; streaming amplia ingestão |
| 6 (Repos, DABs, CI/CD) | 2 (Git), 5 | DABs deploya pipelines DLT/Jobs; CI/CD precisa de Git |
| 7 (Governança UC) | 1 (UC básico), 6 | Permissões sobre objetos já criados; RLS protege Ouro |
| 8 (Performance, CDC, SCD2) | 3 (internals), 4 (Delta), 5 (streaming) | Tuning exige entender Spark; CDC/SCD exige Delta + streaming |
| 9 (Observabilidade, Custos, Serverless, Genie) | 7–8 | Monitoring/custos medem o que foi construído |
| 10 (MLflow, Feature Eng, modelo de vendas) | 4 (Ouro), 9 | Modelo consome Ouro; MLflow é base de toda avaliação GenAI |
| 11–13 (GenAI) | 10 (MLflow), 4 (Ouro), 1 (UC) | Avaliação RAG usa mlflow; RAG consulta tabelas Ouro e UC |
| 14–15 (Agentes) | 12 (LangGraph), 4 (Ouro), 7 (RLS) | Text-to-SQL consulta Ouro seguro; tools usam UC functions |
| 16–18 (Apps, Lakebase) | 13–15 (serving, RAG), 4 | Apps publicam RAG/agentes; Lakebase hospeda vetores/transacional |
| 19 (Projeto final + simulados) | Todas | Integração de ponta a ponta |
| 20–22 (Bônus: app YAML) | 17 (Lakebase), 16 (Apps), 5 (DLT) | Capstone opcional de portfólio |

**Regra de ouro**: nenhuma semana avança sem o entregável da anterior fechado (checklist no fim de cada notebook).

---

## 3. Mapa Free Edition vs Versão Paga (atualizado, base oficial)

> ⚠️ A **Community Edition foi aposentada em junho/2025** → sucessora é a **Free Edition** (serverless-only, uso não comercial, sem SLA, pode ser excluída após inatividade prolongada). Quotas: 1 SQL warehouse (2X-Small), máx. 5 jobs concorrentes, **1 pipeline Lakeflow ativo por tipo**, até 3 Apps (auto-stop 24h), **1 projeto Lakebase**, 1 endpoint AI Search (1 unidade), model serving sem GPU/provisioned throughput, internet de saída restrita (verificação LinkedIn destrava GPU limitada + internet), sem R/Scala, sem external locations/account console/SSO.

| Funcionalidade | Free Edition | Versão paga (trial 14d / conta corporativa) |
|---|---|---|
| Notebooks serverless, SQL, UC, Delta, Volumes, dashboards, Genie básico | ✅ Sim | ✅ |
| Foundation Model APIs (quota limitada) | ✅ Sim (com quota de uso) | ✅ sem quota |
| Mosaic AI Vector Search / AI Search | ✅ 1 endpoint, 1 unidade | ✅ escala, Direct Vector Access |
| Lakeflow pipelines (DLT) + Jobs | ✅ 1 pipeline ativo por tipo; 5 jobs concorrentes | ✅ ilimitado (conforme conta) |
| Databricks Apps | ✅ até 3 apps, auto-stop 24h | ✅ ilimitado, sempre ligado |
| Lakebase + pgvector + Lakebase Search | ✅ 1 projeto, scale-to-zero | ✅ múltiplos projetos |
| MLflow (tracking, registry, evaluate, tracing) | ✅ Sim | ✅ |
| Model Serving (custom CPU, FMA endpoints) | ⚠️ Endpoints limitados, sem custom GPU/batch | ✅ completo |
| Unity AI Gateway (avançado: cache semântico, fallback) | ⚠️ Conceito + endpoints básicos | ✅ completo |
| Fine-tuning (LoRA/QLoRA com GPU) | ❌ (verificação LinkedIn libera GPU limitada) | ✅ GPU dedicada |
| DABs `validate`/`plan` + CLI local | ✅ Sim (local) | ✅ `deploy`/`run` real |
| DABs deploy + CI/CD com GitHub Actions | ❌ (deploy exige workspace pago) | ✅ |
| External locations / storage credentials | ❌ | ✅ |
| Lakehouse Federation, Lakeflow Connect | ❌ | ✅ |
| Lakehouse Monitoring avançado, System tables completas | ⚠️ Parcial | ✅ |
| R, Scala, Photon dedicado, cluster policies, instance pools, Terraform | ❌ | ✅ |
| Genie Ontology, Agent Bricks 2.0 completo, Knowledge Assistant | ⚠️ Parcial/conceitual | ✅ |

**Estratégia de trial pago**: usar os 14 dias de trial de forma concentrada nas Semanas 6 (deploy DABs), 7 (external locations), 9 (Lakeflow Connect), 13 (fine-tune GPU, gateway), 15 (agent serving) e 18–19 (apps em escala + projeto final). Cada dia `🔑` traz: (a) o que roda na Free para validar conceito, (b) passo a passo exato na UI paga.

---

## 4. Visão geral — 6 fases + bônus

| Fase | Semanas | Tema | Certificações |
|---|---|---|---|
| **0 — Fundações** | 1–2 | Plataforma, Lakehouse, SQL analítico, Git, modelagem dimensional | DEA, DAA |
| **1 — Engenharia de Dados Core** | 3–6 | Spark, Delta, Medallion, Auto Loader, Streaming, DLT, Jobs, DABs, CI/CD | DEA, DEP |
| **2 — Governança, Performance, BI** | 7–9 | Unity Catalog, tuning, CDC/SCD2, observabilidade, custos, serverless, Genie | DEA (UC 30%), DEP, DAA |
| **3 — ML/MLOps** | 10 | MLflow completo, Feature Engineering in UC, modelo de vendas | MLP, MLA |
| **4 — GenAI** | 11–13 | RAG do zero à produção, avaliação, AI Gateway, fine-tuning | GenAI Assoc, MLP |
| **5 — Agentes** | 14–15 | ReAct, tools, text-to-SQL, multi-agente, Agent Framework, Genie Ontology | GenAI Assoc |
| **6 — Aplicações** | 16–19 | Databricks Apps, Lakebase, vetorização, full-stack, projeto final, simulados | Todas |
| **Bônus (opcional)** | 20–22 | App de Parametrização e Ingestão Governada por YAML | Portfólio empresarial |

---

## 5. Detalhamento por semana

> **Notebooks**: cada dia = 1 notebook `NN_semanaX_diaY_tema_sem_acento.ipynb` em `notebooks/` (ex.: `07_semana2_dia3_git_github.ipynb`). Anatomia obrigatória: cabeçalho (tema, objetivo, certificação alvo, entregável, plano Free/Pago, tempo ≤2h) → teoria enxuta com diagrama → 3–6 células que rodam na Free Edition → 3–5 exercícios com gabarito → 2–3 dicas "cai na prova" → checklist.
> **Nota de migração**: o notebook já criado `01_semana1_ambiente_lakehouse.ipynb` deve ser dividido nos 6 notebooks da Semana 1.

---

### FASE 0 — FUNDAÇÕES

#### Semana 1 — Plataforma, Lakehouse e primeiros dados (✅ Free)
**Objetivo**: conta Free Edition, ambiente serverless, Unity Catalog, dados do projeto em Bronze, primeiro SQL e dashboard.
**Certificação**: DEA (fundações) | 🎯 DAIS 2026: AI Assistant integrado

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Conta Free Edition (sucessora da Community Edition), tour da UI, notebook serverless, comandos mágicos (%python/%sql/%md/%fs), cluster vs serverless | ✅ | Notebook `00_bem_vindo` |
| 2 | Arquitetura Lakehouse (7 características), UC 3 níveis (catalog.schema.table), DBFS vs **Volumes** (padrão 2026) | ✅ | Diagrama + notas |
| 3 | Datasets do projeto (Online Retail ~540k), upload/FileStore, leitura CSV/JSON/Parquet/Delta, inspeção (printSchema, describe) | ✅ | Dados lidos |
| 4 | SQL Warehouse (2X-Small), queries analíticas, views temporárias, ponte Python↔SQL | ✅ | 10 queries |
| 5 | SQL analítico: SELECT/GROUP BY/HAVING/CASE/joins + criação das tabelas `vendas_bronze` e `voos_bronze` com `_ingested_at` | ✅ | Bronze criado |
| 6 | Primeiro dashboard (AI/BI) + checklist da semana | ✅ | Dashboard simples |

#### Semana 2 — SQL avançado, Git e modelagem dimensional (✅ Free)
**Objetivo**: base SQL da prova DEA ("ELT with Spark SQL and Python"), Git para DABs, conceitos de modelagem.
**Certificação**: DEA, DAA

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | SQL avançado: CTEs, subqueries, window functions (ROW_NUMBER/LAG/RANK), PIVOT, filtros eficientes | ✅ | Exercícios |
| 2 | Qualidade de dados: 6 dimensões (completude, unicidade, validade, pontualidade, precisão, consistência), profiling, CHECK/NOT NULL constraints | ✅ | Regras de qualidade no Bronze |
| 3 | **Git e GitHub do zero**: repo, commits, branches, merge/PR, .gitignore — por que versionar pipelines | ✅ (local) | Repo do curso |
| 4 | Modelagem dimensional: fato vs dimensão, star schema, SCD 1/2/3 (conceito), convenções (dim_, fato_, _vw) | ✅ | Modelo conceitual do projeto |
| 5 | Databricks SQL: dashboards, alerts, query history, visualizações, queries agendadas | ✅ | Relatório SQL |
| 6 | Entregável da semana + **simulado parcial DEA (domínio SQL/UC)** | ✅ | Resultado ≥ 70% |

---

### FASE 1 — ENGENHARIA DE DADOS CORE

#### Semana 3 — Spark: DataFrame API, Spark SQL e internals (✅ Free)
**Objetivo**: dominar transformações ELT com Python e Spark SQL + entender o motor (base do tuning na Semana 8).
**Certificação**: DEA (núcleo), Spark Developer Associate (opcional)

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Spark: driver/executors, lazy evaluation, DataFrame vs RDD (conceitual — RDD fora da prova), Catalyst/AQE visão geral, DAG | ✅ | Diagramas mentais |
| 2 | Leitura/escrita: formatos, opções, schema enforcement vs inferSchema, paths (Volumes/DBFS) | ✅ | Leituras nos 4 formatos |
| 3 | Transformações: select/withColumn/filter/joins (inner/left/anti/semi)/union/agregações | ✅ | Exercícios |
| 4 | Window functions no Spark, UDFs Python (quando evitar), **pandas API on Spark + Spark Connect** (Spark Dev 2026) | ✅ | Exercícios |
| 5 | Internals: partitions, shuffle, broadcast vs sort-merge join, cache/persist, Spark UI e plano físico, pitfalls comuns | ✅ | Análise de plano físico |
| 6 | Entregável: pipeline Python de limpeza + **simulado parcial DEA (Spark)** | ✅ | Pipeline rodando |

#### Semana 4 — Delta Lake + Medallion completa (✅ Free)
**Objetivo**: construir Bronze → Prata → Ouro do projeto com Delta e modelagem correta.
**Certificação**: DEA | 🎯 DAIS 2026: Liquid Clustering 2.0, TTL nativo

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Delta: ACID, `_delta_log`, **Time Travel** (history/version/restore), VACUUM | ✅ | Time travel exercitado |
| 2 | MERGE/upsert, schema evolution/enforcement, constraints (CHECK/NOT NULL), generated columns | ✅ | Constraints aplicadas |
| 3 | Otimização: OPTIMIZE, **Liquid Clustering (CLUSTER BY — padrão 2026)** vs Z-ORDER (legado), bin-packing, autotune | ✅ | Tabelas clusterizadas |
| 4 | Camada Prata: `dim_cliente` (dedup/tipagem), `dim_produto`, `dim_tempo`, `fato_vendas` (star schema real) | ✅ | Prata completa |
| 5 | Camada Ouro: `vendas_por_dia`, `receita_por_pais`, `top_produtos` (denormalizado para BI) | ✅ | Ouro completo |
| 6 | Dashboard conectado ao Ouro + exercícios DEA (Delta) + checklist | ✅ | Dashboard + exercícios |

#### Semana 5 — Ingestão, Streaming e Lakeflow (DLT + Jobs) (✅ Free)
**Objetivo**: sair de notebooks manuais para pipelines declarativos com qualidade.
**Certificação**: DEA, DEP | 🎯 DAIS 2026: Lakeflow Designer

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | **Auto Loader**: ingestão incremental, schema inference/evolution, exactly-once, checkpoint | ✅ | Ingestão incremental |
| 2 | **Structured Streaming**: batch vs streaming, readStream/writeStream, trigger, watermark, checkpointing | ✅ | Streaming simples |
| 3 | **Lakeflow pipelines (DLT)**: @dlt.table/@dlt.view, live tables, streaming tables, UI do pipeline (1 ativa na Free) | ✅ | Pipeline Bronze→Prata |
| 4 | DLT Expectations: 3 níveis (expect, expect_or_drop, expect_or_fail), qualidade contínua, métricas | ✅ | Expectations aplicadas |
| 5 | **Lakeflow Jobs**: orquestração, dependências, retries, alertas, schedule (máx. 5 concorrentes na Free) | ✅ | Job agendado |
| 6 | Pipeline DLT completo + job rodando + exercícios | ✅ | Entregável da semana |

#### Semana 6 — Produção: Repos, DABs e CI/CD (✅ + 🔑 deploy)
**Objetivo**: pipelines versionados e implantados como código (IaC) — o diferencial mais cobrado no mercado.
**Certificação**: DEP | 🎯 DAIS 2026: DABs como padrão de deploy

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | **Databricks Repos**: conectar GitHub, branch workflow, workspace files, estrutura de pastas | ✅ | Repo conectado |
| 2 | **DABs**: conceito, `databricks.yml`, resources, targets dev/staging/prod; `bundle validate`/`plan` local | ✅ | Bundle validado |
| 3 | **Deploy real** no trial pago: `bundle deploy`/`run`, variáveis, resources (job + pipeline) por ambiente | 🔑 | Deploy dev/staging |
| 4 | **CI/CD**: GitHub Actions + DABs (blueprints oficiais), gatilhos por branch, testes em CI | 🔑 | Pipeline CI rodando |
| 5 | Databricks CLI + REST API 2.0 (jobs), secrets scope (conceito; produção 🔑) | ✅ + 🔑 | Scripts CLI |
| 6 | Entregável: repo versionado + primeiro deploy + **simulado parcial DEA (Lakeflow/Delta)** | ✅ + 🔑 | Entregável + simulado |

---

### FASE 2 — GOVERNANÇA, PERFORMANCE, BI

#### Semana 7 — Governança Unity Catalog completa (✅ + 🔑 externals)
**Objetivo**: segurança, LGPD e governança de nível empresarial (DEA: UC = ~30% da prova).
**Certificação**: DEA, DEP (Lakehouse Administrator alinhado)

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | UC profundo: namespace 3 níveis, managed vs external (external 🔑), Volumes para arquivos | ✅ + 🔑 | Volumes criados |
| 2 | Segurança: grupos, GRANT/REVOKE, dynamic views, **RLS** e **column masking** (PII) | ✅ | RLS + masking no Ouro |
| 3 | Linhagem (column-level), tags de classificação, audit logs e **system tables** (access/billing) | ✅ | Linhagem documentada |
| 4 | **Lakehouse Federation** (🔑) + **Delta Sharing** (protocolo aberto) | 🔑 + ✅ | Federated query + share |
| 5 | **LGPD/GDPR**: direito ao esquecimento, TTL/retention, purge, criptografia | ✅ | Política documentada |
| 6 | Entregável: segurança completa + exercícios DEA (UC) | ✅ | Entregável da semana |

#### Semana 8 — Performance, CDC, SCD2 e DLT avançado (✅ + 🔑 produção)
**Objetivo**: nível sênior — tuning de até 10x, versionamento de dados e mudanças incrementais.
**Certificação**: DEP | 🎯 DAIS 2026: TTL nativo Delta, Liquid Clustering 2.0

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Tuning Spark: AQE, broadcast join hints, shuffle partitions, skew, cache/persist estratégia, Photon (conceito) | ✅ | Benchmark antes/depois |
| 2 | Particionamento vs Liquid Clustering vs Z-ORDER; estratégia OPTIMIZE/VACUUM por tamanho de tabela | ✅ | Estratégia aplicada |
| 3 | **CDC**: Change Data Feed, leitura incremental de mudanças, MERGE com CDF | ✅ | CDF habilitado |
| 4 | **SCD1/SCD2** com `APPLY CHANGES INTO`: dim_cliente com histórico (SCD2) | ✅ | SCD2 rodando |
| 5 | DLT avançado: triggered vs continuous, expectations profundas, materialized vs streaming tables; produção 🔑 | ✅ + 🔑 | Pipeline avançado |
| 6 | Entregável: SCD2 + CDC + tuning + **simulado parcial DEP** | ✅ | Entregável + simulado |

#### Semana 9 — Observabilidade, Custos, Serverless, Genie + Simulado DEA (✅ + 🔑)
**Objetivo**: fechar DEA e DEP com monitoramento, custos e BI conversacional.
**Certificação**: DEA (prova real após esta semana), DEP, DAA | 🎯 DAIS 2026: Lakewatch

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | **Lakehouse Monitoring**: quality monitors, drift de schema/dados (🔑 avançado); system tables deep | ✅ + 🔑 | Monitor ativo |
| 2 | **Custos**: billing, tags, budget alerts, serverless vs classic, 10 regras de economia (cai em entrevista) | ✅ | Política de custos |
| 3 | **Serverless compute** (DEP 2026) + **Lakeflow Connect** (🔑) + quando usar cada compute | ✅ + 🔑 | Matriz de decisão |
| 4 | **Genie (AI/BI)**: spaces, perguntas em linguagem natural, Genie Code; ontologia (conceito) | ✅ | Genie space funcional |
| 5 | Dashboards avançados, alerts, SQL warehouse caching/query history | ✅ | Alertas configurados |
| 6 | 📜 **Simulado DEA completo (40 questões, domínios 2026)** + guia de agendamento da prova real | ✅ | Resultado ≥ 70% + prova agendada |

---

### FASE 3 — ML E MLOPS

#### Semana 10 — MLflow, ML lifecycle e Feature Engineering (✅ + 🔑 serving)
**Objetivo**: base de MLOps que sustenta toda a avaliação GenAI + certificação MLP.
**Certificação**: MLP, MLA

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | **MLflow**: experiments, runs, tracking, autologging, params/metrics/artifacts | ✅ | Primeiro experimento |
| 2 | Models: registry, **UC models**, aliases/stages, versionamento, permissões | ✅ | Modelo registrado |
| 3 | ML lifecycle: **modelo de previsão de vendas** (regressão/forecast simples no Ouro), AutoML (intro) | ✅ | Modelo treinado |
| 4 | **Feature Engineering in UC** (MLP 2026): feature tables, online/offline, serving (🔑) | ✅ + 🔑 | Feature table criada |
| 5 | **mlflow.evaluate**: métricas clássicas, avaliação de modelos, batch inference | ✅ | Avaliação rodada |
| 6 | Entregável: modelo com MLflow completo + **simulado parcial DEP/MLP** | ✅ | Entregável + simulado |

---

### FASE 4 — GENAI

#### Semana 11 — GenAI: fundamentos + primeiro RAG (✅ Free, quotas)
**Objetivo**: do zero ao primeiro RAG end-to-end funcional com bases sólidas (tokens, embeddings, chunking).
**Certificação**: GenAI Engineer Associate

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | LLMs: tokens, janela de contexto, temperature, chat vs completion; **Foundation Model APIs** (quota Free) e AI Playground | ✅ | Primeira chamada FMA |
| 2 | Prompt engineering: estrutura de 6 partes, few-shot, Chain-of-Thought, JSON mode, system prompts | ✅ | Promptbook |
| 3 | **Embeddings**: conceito, modelos, similaridade; **chunking** (tamanho/overlap, estratégias) | ✅ | Pipeline de chunking |
| 4 | **Mosaic AI Vector Search**: Delta Sync Index, endpoints (1 na Free), filtros de metadata | ✅ | Índice + endpoint |
| 5 | Primeiro RAG com LangChain: retrieval → augmentation → generation, citações de fontes | ✅ | RAG funcional |
| 6 | Análise qualitativa das respostas + checklist + exercícios | ✅ | Relatório |

#### Semana 12 — RAG avançado, avaliação e LangGraph (✅ + 🔑 rerank)
**Objetivo**: RAG com qualidade mensurável, debugável e pronto para agentes.
**Certificação**: GenAI Engineer Associate (domínio Evaluation & Monitoring ~20%)

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | **Avaliação com mlflow.evaluate** (LLM-as-judge): faithfulness, answer relevance, context precision, context recall; datasets e thresholds | ✅ | Métricas ≥ alvo |
| 2 | **MLflow Tracing**: spans, debug do pipeline completo | ✅ | Trace analisado |
| 3 | **Busca híbrida**: BM25 + semântica com RRF + reranking cross-encoder (🔑) | ✅ + 🔑 | Recall@5 melhorado |
| 4 | Chunking avançado: hierárquico/semântico, metadata, filtros; **RAG multimodal** (PDF/Excel/Word) | ✅ | RAG multimodal |
| 5 | **LangChain/LangGraph**: chains, state, nodes/edges, tools — base dos agentes | ✅ | Primeiro grafo |
| 6 | Entregável: RAG avaliado com gráficos de evolução | ✅ | Entregável da semana |

#### Semana 13 — GenAI em produção, AI Gateway e Fine-tuning (✅ + 🔑 GPU)
**Objetivo**: tirar IA do protótipo: escala, custo controlado, monitoramento contínuo.
**Certificação**: GenAI Engineer Associate, MLP | 🎯 DAIS 2026: Unity AI Gateway

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Os 7 pilares de GenAI em produção; Model Serving (FMA + custom 🔑); provisioned throughput 🔑 | ✅ + 🔑 | Endpoint FMA |
| 2 | **Unity AI Gateway**: roteamento, fallback, cache semântico (-60% custo), auditoria (🔑 avançado) | ✅ + 🔑 | Gateway configurado |
| 3 | **Fine-tuning**: quando vale vs quando NUNCA vale (regra de decisão); LoRA/QLoRA; dataset de treino; demo GPU 🔑 (LinkedIn unlock alternativo) | 🔑 | Demo executada |
| 4 | MLOps para LLMs: versionar prompts/dados/modelos, avaliação contínua, A/B | ✅ | Registros versionados |
| 5 | Monitoramento de RAG: qualidade, custo, latência, segurança + alertas | ✅ | Monitor ativo |
| 6 | Entregável: RAG em produção + **simulado parcial GenAI** | ✅ | Entregável + simulado |

---

### FASE 5 — AGENTES

#### Semana 14 — Agentes: ReAct, tools e Text-to-SQL (✅ Free)
**Objetivo**: primeiro agente seguro e auditável que consulta o próprio Lakehouse.
**Certificação**: GenAI Engineer Associate

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Agente vs LLM, ciclo ReAct, 5 componentes; tool calling; **Unity Catalog Functions como ferramentas** | ✅ | UC functions |
| 2 | Primeiro agente LangGraph: ferramentas (catálogo, cálculo, Ouro), decisão automática | ✅ | Agente funcional |
| 3 | **Text-to-SQL em produção**: dicionário de dados, anti-DELETE/UPDATE/DROP, auto-correção, RLS embutida | ✅ | Agente SQL seguro |
| 4 | Memória de conversa, guardrails, filtros de segurança, tabela de auditoria | ✅ | Auditoria ativa |
| 5 | Avaliação de agentes: MLflow tracing, testes de regressão, métricas (contraste com LangSmith) | ✅ | Suite de testes |
| 6 | Entregável: agente text-to-SQL com 4+ ferramentas + auditoria | ✅ | Entregável da semana |

#### Semana 15 — Agentes avançados, Agent Framework e Genie (✅ + 🔑)
**Objetivo**: agentes com auto-melhoria, multi-especialistas e padrão oficial Databricks.
**Certificação**: GenAI Engineer Associate | 🎯 DAIS 2026: Agent Bricks 2.0 + Omnigent, Genie Ontology

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Arquiteturas: ReAct vs **Reflexion** vs **Multi-agente** (coordenador + especialistas) | ✅ | Multi-agente rodando |
| 2 | **Mosaic AI Agent Framework**: Agent Bricks, evaluation, guardrails (🔑 partes) | ✅ + 🔑 | Agente avaliado |
| 3 | **Genie + Genie Ontology** (🔑): camada semântica de métricas — agente não erra conta | 🔑 | Ontologia criada |
| 4 | Deploy: agente via Model Serving (🔑), API; **MCP**; Slack/Teams; app com agente | ✅ + 🔑 | Deploy UI/API |
| 5 | Segurança empresarial: sandbox Python isolado, PII, auditoria total, governança de agentes | ✅ | Política de segurança |
| 6 | Entregável: multi-agente avaliado + deploy + **simulado parcial GenAI (agentes)** | ✅ | Entregável + simulado |

---

### FASE 6 — APLICAÇÕES E LAKEBASE

#### Semana 16 — Databricks Apps: fundamentos (✅ Free, até 3 apps)
**Objetivo**: publicar dashboards e RAG como apps web com auth nativa.
**Certificação**: GenAI Assoc (deploy), portfólio

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Apps: arquitetura, `app.yaml`, deploy pela UI, auth, limites Free (auto-stop 24h) | ✅ | Hello app |
| 2 | Dashboard Streamlit com Ouro (KPIs, vendas por dia/país) | ✅ | App BI |
| 3 | App RAG com UI (chat, citações, feedback) | ✅ | App RAG |
| 4 | Backend FastAPI + integração com Model Serving, logs | ✅ | API integrada |
| 5 | CI/CD para apps (DABs), scale-to-zero, observabilidade | ✅ | Pipeline de app |
| 6 | Entregável: 2 apps publicados e monitorados | ✅ | Entregável da semana |

#### Semana 17 — Lakebase + Vetorização nativa (✅ Free, 1 projeto)
**Objetivo**: camada transacional + busca vetorial/híbrida nativas (substitui Postgres + FAISS).
**Certificação**: GenAI Assoc (retrieval avançado) | 🎯 DAIS 2026: LTAP, Lakebase Search

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | **Lakebase**: arquitetura LTAP, Delta vs Lakebase, projeto, schema, scale-to-zero | ✅ | Projeto criado |
| 2 | CRUD transacional, **Instant Branching**, PITR; caso de uso: transacional do agente | ✅ | Camada transacional |
| 3 | **pgvector**: embeddings, índices HNSW vs IVFFlat, consultas de similaridade | ✅ | Índice criado |
| 4 | **Lakebase Search**: BM25 + híbrido + RRF, filtros de metadata, sync | ✅ | Busca híbrida |
| 5 | Escala vetorial: arquitetura 1B+ vetores, reranking, custo; Vector Search vs Lakebase | ✅ | Decisão documentada |
| 6 | Entregável: RAG com armazenamento vetorial Lakebase + busca híbrida | ✅ | Entregável da semana |

#### Semana 18 — Apps full-stack (React/Next.js) + MCP (✅ + 🔑 escala)
**Objetivo**: UI profissional de agente com streaming e integrações modernas.
**Certificação**: portfólio (full-stack) | 🎯 DAIS 2026: AI Dev Kit

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Frontend: React/Next.js + SDK Databricks Apps, componentes | ✅ | Componentes |
| 2 | Full-stack: Next.js ↔ API ↔ dados; autenticação e RBAC | ✅ | App full-stack |
| 3 | Agente com UI profissional: streaming de respostas, feedback, estados | ✅ | Chat streaming |
| 4 | **MCP**: servidores/ferramentas, integração com agentes (padrão 2026) | ✅ + 🔑 | MCP conectado |
| 5 | Segurança, performance, testes, observabilidade de apps | ✅ | App testado |
| 6 | Entregável: app full-stack com agente publicado | ✅ | Entregável da semana |

#### Semana 19 — Projeto Final, Simulados e Carreira (✅ + 🔑 deploy final)
**Objetivo**: unificar tudo, validar com simulados 2026 e preparar mercado internacional.
**Certificação**: DEA, DEP, GenAI Assoc, MLP (revisão final)

| Dia | Tema e conteúdo | Plano | Entregável |
|---|---|---|---|
| 1 | Arquitetura do projeto final: diagrama completo, decisões e trade-offs documentados | ✅ | Diagrama |
| 2 | **Projeto ponta a ponta**: DLT + qualidade + RAG + agente + app + DABs (código completo) | ✅ + 🔑 | Projeto final |
| 3 | 📜 **Simulado DEP** (40 questões, domínios 2026) + gabarito comentado | ✅ | Resultado ≥ 70% |
| 4 | 📜 **Simulado GenAI Associate** (40 questões) + gabarito comentado | ✅ | Resultado ≥ 70% |
| 5 | **30 perguntas de entrevista internacional (EN)** com respostas; salários US/EU/UK; LinkedIn e GitHub | ✅ | Material de entrevista |
| 6 | Checklist de competências (32+), estrutura final do repositório, roadmap de recertificação, contribuições a projetos open source (databricks-industry-solutions) | ✅ | Repo finalizado |

---

### MÓDULO BÔNUS (OPCIONAL) — PORTFÓLIO EMPRESARIAL

#### Semanas 20–22 — App de Parametrização e Ingestão Governada por YAML (🔑 partes)
**Recomendado** para quem quer portfólio enterprise. Mantido do seu pedido original como capstone opcional — só inicie após a Semana 19.

| Semana | Tema | Entregável |
|---|---|---|
| 20 | Fundações + Seção Admin: arquitetura, modelo de 6 tabelas **Lakebase**, **JSON Schema validador de YAML**, editor com syntax highlight/diff/rollback, permissões por fluxo | Admin 100% funcional + 4 fluxos YAML (Metas, Descontos, Preços, Clientes) |
| 21 | Motor de validações em 4 camadas (estrutura → tipo/formato → consistência SQL → regra de negócio Python), upload CSV com relatório de erros, formulário dinâmico gerado do YAML com combos do Lakehouse | Motor completo + CSV + formulário |
| 22 | Aprovação obrigatória, gravação Bronze → disparo DLT automático, histórico/rastreabilidade/LGPD, UI por perfil, deploy Databricks App com CI/CD | App DataFlow Admin pronto para uso empresarial |

---

## 6. Estratégia de certificações (2026)

| Certificação | Semanas | Quando agendar | Domínios-chave 2026 |
|---|---|---|---|
| **Data Engineer Associate (DEA)** | 1–9 | Logo após a Semana 9 | ELT com Spark SQL/Python, Unity Catalog ≈ 30%, Delta Lake, Lakeflow, medallion, qualidade |
| **GenAI Engineer Associate** | 11–15 | Após a Semana 15 | Design ~20%, Data Prep/Vector Search ~20%, App Dev/LangChain ~25%, Governance/AI Gateway ~15%, Evaluation & Monitoring ~20% |
| **Data Engineer Professional (DEP)** | 5–10 + 13 | Após a Semana 19 | Serverless, Lakeflow Connect, DLT avançado, CDC/SCD2, performance, governança |
| **ML Professional (MLP)** | 10 + 13 | Após a Semana 19 (opcional) | Mosaic AI Model Serving, Lakehouse Monitoring, Feature Engineering, MLflow |

**Ordem recomendada**: DEA → GenAI Associate → DEP → MLP (opcional). Todas são independentes (sem pré-requisito oficial), mas esta ordem maximiza aproveitamento e aproveita o desconto de estudante/primeira prova onde disponível.
**Detalhes práticos**: provas via Pearson VUE/OnVUE; validade de 2 anos com recertificação; simulados do curso cobrem os domínios com pesos aproximados dos reais; consultar sempre o *Exam Guide* oficial na Databricks Academy antes de agendar.

---

## 7. Checklist de competências para o mercado internacional (32+)

**Plataforma** (1–5): workspace/notebooks serverless, SQL warehouses, Unity Catalog 3 níveis, Volumes, compute (serverless vs classic).
**Engenharia de dados** (6–13): Spark SQL + DataFrame API, Delta Lake (ACID/time travel/MERGE), Medallion, Auto Loader, Structured Streaming, DLT/Lakeflow pipelines, Lakeflow Jobs, DABs + CI/CD.
**Governança e plataforma** (14–20): RLS/masking/dynamic views, linhagem, system tables/audit, Lakehouse Federation, Delta Sharing, custos/budget, CLI/REST API.
**Performance** (21–23): Liquid Clustering vs particionamento, OPTIMIZE/VACUUM, tuning (AQE/broadcast/cache).
**ML/MLOps** (24–26): MLflow (tracking/registry/evaluate/tracing), Feature Engineering in UC, Model Serving.
**GenAI** (27–30): FMA + prompting, embeddings/chunking, Vector Search + híbrido/rerank, avaliação RAG, AI Gateway, fine-tuning (quando vale).
**Agentes** (31–34): ReAct/Reflexion/multi-agente, tools + UC functions, text-to-SQL seguro, Agent Framework, MCP, Genie Ontology.
**Aplicações** (35–38): Databricks Apps (Streamlit/full-stack), Lakebase + pgvector, segurança de apps, observabilidade.
**Carreira** (39–40): entrevistas técnicas em inglês, comunicação de arquitetura, portfólio no GitHub.

---

## 8. Glossário EN-PT essencial (para entrevistas internacionais)

| Termo (EN) | Português |
|---|---|
| Lakehouse / Medallion architecture | Lakehouse / arquitetura Medallion (Bronze, Silver, Gold) |
| Data quality / expectations | Qualidade de dados / expectativas (DLT) |
| Upsert / Change Data Capture | Upsert / captura de mudanças |
| Lineage / audit logs | Linhagem / logs de auditoria |
| Column masking / row-level security | Mascaramento de coluna / segurança em nível de linha |
| Time travel / vacuum | Viagem no tempo / limpeza física |
| Vector search / embeddings / chunking | Busca vetorial / embeddings / divisão em blocos |
| Retrieval-Augmented Generation (RAG) | Geração aumentada por recuperação |
| Guardrails / sandbox | Salvaguardas / ambiente isolado |
| Model serving / endpoint | Servir modelos / endpoint de inferência |
| Scale-to-zero / serverless | Escala até zero / sem servidor gerenciado |

---

## 9. Entregáveis finais do curso

1. Plataforma Lakehouse completa (Bronze→Prata→Ouro) com governança, qualidade e performance
2. Pipeline DLT + Jobs + DABs versionados com CI/CD (3 ambientes)
3. Modelo de ML com MLflow completo (tracking, registry, evaluation) + feature table
4. RAG de produção com avaliação quantificada, busca híbrida e monitoramento
5. Agente text-to-SQL seguro e auditável + multi-agente com deploy UI/API
6. 2+ Databricks Apps publicados (BI + RAG + full-stack)
7. Camada Lakebase transacional + busca vetorial híbrida
8. Repositório GitHub profissional com README, diagramas e explicação para entrevistas
9. (Opcional) App DataFlow Admin de parametrização por YAML

---

## 10. Material oficial (apenas fontes oficiais)

- Databricks Academy (Exams + cursos): https://partner-academy.databricks.com
- Documentação oficial: https://docs.databricks.com (guia de limitações da Free Edition: docs.databricks.com/aws/en/getting-started/free-edition-limitations)
- Certificações: https://www.databricks.com/learn/certification
- Exemplos de produção: https://github.com/databricks-industry-solutions
- Blog de lançamentos: https://www.databricks.com/blog
