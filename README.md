# 🚀 Curso Especialista Databricks — 324 Notebooks (22 Semanas)

**Do zero ao Especialista Databricks** — Engenharia de Dados → ML/MLOps → GenAI → Agentes → Apps/Lakebase, com foco nas **certificações oficiais 2026** (DEA, DEP, GenAI Engineer Associate, MLP) e no **mercado internacional**.

**Plataforma**: Databricks **Free Edition** (sucessora da Community Edition, serverless-only) — ~85% do curso roda nela; os dias marcados `🔑 Versão paga` usam o **trial de 14 dias** estrategicamente.

---

## 📊 O que existe neste repositório

| Item | Quantidade |
|---|---|
| Notebooks de curso (`.ipynb`) | **324** (6 por semana × 22 semanas = 132, + 192 exercícios/gabaritos integrados) |
| Semanas | 22 (19 núcleo + 3 capstone opcional) |
| Células | ~3.900 (teoria + código + exercícios + gabarito + simulados) |
| Simulados no formato das provas | DEA (40q) · DEP (40q) · GenAI (40q) + parciais |
| Projeto único | Vendas de varejo (Online Retail) do Bronze ao app |

## 🗂️ Estrutura

```
databricks-course/
 ├── notebooks/            # 324 notebooks numerados (001_... até 324_...)
 ├── tools/
 │   ├── nbkit.py          # DSL para construir notebooks
 │   ├── nbgen.py          # gerador (python tools/nbgen.py)
 │   ├── validate_nb.py    # validador (python tools/validate_nb.py)
 │   └── specs/            # especificações das 22 semanas (semana1.py ... semana22.py)
 ├── legacy/               # notebook antigo da Semana 1 (substituído)
 ├── FONTES_DATASET.md     # fontes verificadas do dataset Online Retail (Databricks samples / GitHub oficial / UCI / Kaggle)
 ├── PLANO_CURSO_RESTRUTURADO.md   # o plano aprovado (22 semanas)
 └── PROMPT_PLANO_CURSO.md         # prompt melhorado para gerar o plano
```

## 🗺️ Mapa do curso (22 semanas)

| Fase | Semanas | Tema | Certificações |
|---|---|---|---|
| **0 — Fundações** | 1–2 | Plataforma, Lakehouse, SQL analítico, Git, modelagem | DEA, DAA |
| **1 — Eng. de Dados Core** | 3–6 | Spark, Delta, Medallion, Auto Loader, Streaming, DLT, Jobs, DABs, CI/CD | DEA, DEP |
| **2 — Governança/Perf/BI** | 7–9 | Unity Catalog, RLS/masking, tuning, CDC/SCD2, custos, Genie, **Simulado DEA** | DEA, DEP, DAA |
| **3 — ML/MLOps** | 10 | MLflow, Feature Engineering in UC, modelo de previsão | MLP, MLA |
| **4 — GenAI** | 11–13 | LLMs, prompts, embeddings, Vector Search, RAG, avaliação, gateway, fine-tuning | GenAI Assoc, MLP |
| **5 — Agentes** | 14–15 | ReAct, tools UC, Text-to-SQL, Reflexion, multi-agente, Agent Bricks, Ontologia | GenAI Assoc |
| **6 — Aplicações** | 16–19 | Apps, Lakebase/pgvector, full-stack, MCP, Projeto Final, **Simulados DEP+GenAI**, carreira | Todas |
| **Bônus** | 20–22 | App DataFlow Admin (parametrização/ingestão por YAML) | Portfólio |

## ▶️ Como usar

1. **Crie a conta**: https://www.databricks.com/try-databricks → **Free Edition** (anote o URL e a senha; verifique via LinkedIn para liberar GPU/internet).
2. **Importe os notebooks**: no workspace, `Workspace → Import → Upload` os arquivos de `notebooks/` (ou use o gerador para recriá-los).
3. **Siga a ordem**: `001_...` → `324_...`. Cada notebook tem: teoria → código rodável na Free Edition → exercícios → gabarito → dicas de prova → checklist.
4. **Regra de trial**: os dias `🔑 Versão paga` (DABs deploy, external locations, fine-tune GPU, rerank, Genie Ontology, agent serving) usam o **trial de 14 dias** — concentre-os nas Semanas 6, 7, 9, 13, 15 e 19.

## 🎯 Certificações cobertas (2026)

| Prova | Onde no curso | Destaques 2026 |
|---|---|---|
| **Data Engineer Associate** | Semanas 1–9 | ELT com Spark SQL/Python · UC ~30% · Lakeflow |
| **GenAI Engineer Associate** | Semanas 11–15 | 5 domínios (Design/DataPrep/AppDev/Governance/Eval) |
| **Data Engineer Professional** | Semanas 5–10 + 19 | Serverless, Lakeflow Connect, SCD/CDC, tuning |
| **ML Professional** (opcional) | Semanas 10 + 13 | Model Serving, Lakehouse Monitoring, Feature Eng |

Simulados completos: Semana 9 (DEA, 40q) · Semana 19 (DEP 40q + GenAI 40q).

## 📦 Entregáveis do curso

1. Plataforma Lakehouse (Bronze→Prata→Ouro) com governança e qualidade
2. Pipelines DLT + Jobs + DABs + CI/CD (3 ambientes)
3. Modelo de ML com MLflow completo + feature table
4. RAG de produção com avaliação (4 métricas) e busca híbrida
5. Agente Text-to-SQL seguro + multi-agente com deploy
6. 2+ Databricks Apps (BI + RAG + full-stack) + camada Lakebase
7. (Bônus) App DataFlow Admin — ingestão governada por YAML
8. Repositório de portfólio + material de entrevistas em inglês

## 🔗 Material oficial

- Databricks Academy: https://partner-academy.databricks.com
- Documentação: https://docs.databricks.com · Limitações Free: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- Certificações: https://www.databricks.com/learn/certification
- Exemplos de produção: https://github.com/databricks-industry-solutions

## 🛠️ Manutenção (para quem quer regenerar)

```bash
# Regenerar todos os notebooks a partir das especificações
python tools/nbgen.py

# Validar estrutura (JSON, ids, células)
python tools/validate_nb.py
```

> **Nota**: os notebooks usam nomenclatura e produtos 2026 (Lakeflow, Liquid Clustering, Mosaic AI, Free Edition, Lakebase). A Community Edition foi aposentada em jun/2025 — o curso inteiro foi escrito para a **Free Edition**.
