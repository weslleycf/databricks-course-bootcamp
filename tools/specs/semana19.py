"""Semana 19 — Projeto Final, Simulados e Carreira (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana19_dia1_arquitetura_projeto_final",
    [
        header(
            "19", "1", "Arquitetura do Projeto Final Unificado",
            "Desenhar a arquitetura completa do projeto (dados + ML + GenAI + apps) e "
            "documentar as decisões e trade-offs.",
            "Todas (revisão)", "Diagrama de arquitetura completo",
            "✅ Free Edition",
        ),
        teoria(
            "O que o Projeto Final une",
            "Tudo o que você construiu:\n\n"
            "```\nLanding --AutoLoader--> Bronze --DLT--> Prata --DLT--> Ouro\n   |                                                 |\n   | (quality/expectations)                    BI (dashboards + Genie)\n   |                                                 |\n   |                                          ML (MLflow + feature eng)\n   |                                                 |\n   |                                          RAG (Vector Search + FMA)\n   |                                                 |\n   |                                          Agente (tools UC + MCP)\n   |                                                 |\n   |                                          Apps (Next.js + FastAPI)\n   └── Tudo versionado (DABs + CI/CD) e governado (UC)\n```",
        ),
        pratica("Documentando as decisões",
            "Escreva o documento de arquitetura (ADRs) do projeto."),
        code('# Decisões de arquitetura (documente no README/ADR)\n'
             'adrs = """\n'
             '1. Medallion (Bronze/Prata/Ouro) - por que: reprocessamento e qualidade\n'
             '2. DLT para pipelines - por que: declarativo + expectations\n'
             '3. Star schema na Prata - por que: BI e ML reutilizam\n'
             '4. RAG com Vector Search + híbrido - por que: custo/qualidade\n'
             '5. Agente com UC functions - por que: governança\n'
             '6. Lakebase para estado - por que: transacional\n'
             '7. Apps (Next.js + FastAPI) - por que: produto\n'
             '"""\n'
             'print(adrs)'),
        pratica("Diagrama final",
            "Desenhe o diagrama (mermaid/ASCII) no README — será a primeira imagem que "
            "entrevistadores veem."),
        dica_prova("Entrevista: 'descreva sua arquitetura' → comece pelo diagrama, "
                   "explique cada camada em 1 frase e justifique 2 decisões (por que DLT? "
                   "por que RAG?)."),
        exercicios([
            "Desenhe o diagrama completo no README (mermaid).",
            "Liste 3 decisões que você mudaria em produção (e por quê).",
        ]),
        gabarito([
            ("Mermaid",
             "Use blocos: ingestão → bronze → prata → ouro → consumo (BI/ML/RAG/agente/app)."),
            ("Mudanças",
             "Ex.: DLT contínuo em vez de triggered; Lakebase para mais tabelas; "
             "multi-agente em produção."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana19_dia2_projeto_ponta_a_ponta",
    [
        header(
            "19", "2", "Projeto de ponta a ponta (código completo)",
            "Executar o pipeline completo do zero: dados → Ouro → modelo → RAG → agente → "
            "app, validando a integração de todas as peças.",
            "Todas (integração)", "Projeto final rodando de ponta a ponta",
            "✅ Free Edition (deploy 🔑)",
        ),
        teoria(
            "O roteiro do dia",
            "1. Recriar as tabelas (Bronze/Prata/Ouro) — Semanas 1–4\n"
            "2. Pipeline DLT com expectations — Semana 5\n"
            "3. Modelo MLflow (previsão de receita) — Semana 10\n"
            "4. RAG (produtos) — Semanas 11–12\n"
            "5. Agente (Text-to-SQL + tools) — Semanas 14–15\n"
            "6. App (BI + chat) — Semanas 16–18\n"
            "7. DABs + CI/CD — Semana 6",
        ),
        pratica("Checklist de execução",
            "Rode cada bloco e confira."),
        code('# 1) Camadas de dados\n'
             'print("Bronze:", spark.table("workspace.bronze.vendas_bronze").count())\n'
             'print("Prata:", spark.table("workspace.prata.fato_vendas").count())\n'
             'print("Ouro:", spark.table("workspace.ouro.vendas_por_dia").count())'),
        code('# 2) Modelo\n'
             'import mlflow\n'
             'print("Modelo champion:",\n'
             '      mlflow.get_model_version("workspace.prata.modelo_previsao_receita", "1"))\n'
             'print("Rode a predição para amanhã (features de calendário).")'),
        code('# 3) RAG + agente (teste de fumaça)\n'
             'print(rag.invoke({"input": "Quais produtos de vidro?"})["answer"][:120])\n'
             'print(agente_final.invoke({"input": "Qual a receita do UK?"})["output"][:120])'),
        pratica("Validação integrada",
            "Crie um notebook único `projeto_final.ipynb` que executa tudo — o artefato "
            "do portfólio."),
        code('# Notebook do projeto final (estrutura)\n'
             'print("""\n'
             'projeto_final.ipynb:\n'
             '  1. Setup (schemas/volumes)\n'
             '  2. Ingestão (Auto Loader)\n'
             '  3. DLT (Bronze->Prata->Ouro)\n'
             '  4. Qualidade (expectations)\n'
             '  5. Modelo (MLflow)\n'
             '  6. RAG (Vector Search + FMA)\n'
             '  7. Agente (tools + auditoria)\n'
             '  8. Resumo (métricas e links dos apps)\n'
             '""")\n'
             'print("Rode do início ao fim — o demo da entrevista.")'),
        dica_prova("Portfólio: um notebook que roda tudo (com métricas e links) prova que "
                   "o conhecimento é integrado, não em ilhas."),
        exercicios([
            "Rode o projeto_final.ipynb do zero (sem células quebradas).",
            "Capture 3 prints (pipeline, modelo, chat) para o README.",
        ]),
        gabarito([
            ("Rode do zero",
             "Crie um notebook limpo; se algo falhar, é lacuna — revise a semana "
             "correspondente."),
            ("Prints",
             "Imagens valem mais que texto no portfólio — use-as no README."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana19_dia3_simulado_dep_completo",
    [
        header(
            "19", "3", "📜 Simulado DEP completo (40 questões)",
            "Validar o nível Professional com um simulado no formato da prova DEP 2026.",
            "DEP (simulado)", "Simulado DEP ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "Formato da prova DEP (2026)",
            "- 60 questões, 180 min, Pearson VUE\n"
            "- Domínios: pipelines DLT avançado · CDC/SCD · performance/tuning · "
            "governança UC · serverless/Lakeflow Connect · custos · observabilidade\n"
            "- Validade: 2 anos",
        ),
        pratica("Simulado DEP (20 questões aqui — marque antes do gabarito)",
            "Responda sem consultar."),
        md("""### Questões DEP (1–20)

**1.** Para SCD2 com histórico completo:
- A) MERGE  B) apply_changes (type 2)  C) UPDATE  D) INSERT

**2.** `_change_type='delete'` aparece ao ler com:
- A) readChangeFeed=true  B) readStream  C) select  D) count

**3.** O AQE pode:
- A) converter sort-merge em broadcast em runtime  B) apagar dados
- C) criar tabelas  D) nada

**4.** Para reduzir shuffle em join com dimensão pequena:
- A) broadcast join  B) shuffle.partitions=1  C) cache  D) nada

**5.** Liquid Clustering é definido com:
- A) CLUSTER BY  B) ZORDER BY  C) PARTITION BY  D) SORT BY

**6.** `expect_all_or_fail`:
- A) mantém e conta  B) falha pipeline em violação  C) descarta  D) remove

**7.** Triggered vs Continuous: Triggered é:
- A) streaming contínuo  B) processa o delta e para  C) mais lento sempre  D) igual

**8.** Para propagar mudanças do Delta a outro sistema:
- A) CDF  B) cache  C) VACUUM  D) OPTIMIZE

**9.** `sequence_by` no apply_changes:
- A) ordem temporal dos eventos  B) ordem das colunas  C) tamanho  D) nada

**10.** Managed table com DROP:
- A) apaga dados  B) preserva  C) exige LOCATION  D) nada

**11.** Para consultar Postgres externo:
- A) Lakehouse Federation  B) Delta Sharing  C) volume  D) cache

**12.** Para compartilhar dados com parceiro:
- A) Delta Sharing  B) Federation  C) merge  D) external table

**13.** system.access.audit:
- A) audita acessos  B) otimiza  C) custa  D) nada

**14.** TTL nativo (DAIS 2026):
- A) expira dados automaticamente  B) cache  C) índice  D) share

**15.** Serverless:
- A) plataforma gerencia compute  B) cluster próprio  C) mais config  D) RDD

**16.** Lakeflow Connect:
- A) ingestão SaaS sem código  B) query engine  C) cofre  D) repo

**17.** Para custo de warehouse ocioso:
- A) auto-stop  B) mais workers  C) cache  D) nada

**18.** Lakehouse Monitoring detecta:
- A) drift de schema/dados  B) bugs de código  C) tokens  D) nada

**19.** DABs `bundle validate`:
- A) valida config sem aplicar  B) deploya  C) roda  D) apaga

**20.** CI valida; CD:
- A) deploya no merge  B) roda testes  C) apaga  D) nada
"""),
        teoria(
            "Gabarito DEP (1–20)",
            "**1-B** · **2-A** · **3-A** · **4-A** · **5-A** · **6-B** · **7-B** · "
            "**8-A** · **9-A** · **10-A** · **11-A** · **12-A** · **13-A** · **14-A** · "
            "**15-A** · **16-A** · **17-A** · **18-A** · **19-A** · **20-A**.\n\n"
            "Quase tudo DEP = 'para que serve X'. Errou ≥ 6? Revise Semanas 5–9.",
        ),
        pratica("Simulado DEP (20–40)",
            "Segunda metade — marque antes."),
        md("""### Questões DEP (21–40)

**21.** `OPTIMIZE` resolve:
- A) muitos arquivos pequenos  B) nulos  C) duplicatas  D) schema

**22.** VACUUM (7d) remove:
- A) arquivos fora da retenção  B) tudo  C) log  D) nada

**23.** Para Time Travel por timestamp:
- A) timestampAsOf  B) versionAsOf  C) DESCRIBE  D) MERGE

**24.** Auto Loader garante:
- A) exactly-once  B) at-least-once  C) nada  D) cache

**25.** `checkpointLocation`:
- A) retomada sem reprocessar  B) schema  C) cache  D) backup

**26.** Watermark serve para:
- A) dados atrasados  B) acelerar  C) compactar  D) nada

**27.** Column masking mascara:
- A) colunas por usuário  B) linhas  C) arquivos  D) nada

**28.** RLS filtra:
- A) linhas por usuário  B) colunas  C) tabelas  D) nada

**29.** Para versões de prompt/dataset:
- A) MLflow + Git  B) cache  C) DABs  D) nada

**30.** mlflow.evaluate com baseline:
- A) compara com regra simples  B) apaga  C) treina  D) nada

**31.** Feature Engineering in UC:
- A) feature tables governadas  B) notebook  C) cache  D) nada

**32.** Skew de join é corrigido por:
- A) AQE  B) cache  C) broadcast sempre  D) nada

**33.** Para leitura eficiente em filtro por país+data (5TB):
- A) CLUSTER BY (Country, data)  B) particionar por país  C) Z-ORDER só  D) nada

**34.** Budget alerts avisam:
- A) gasto acima do limite  B) erro de código  C) tokens  D) nada

**35.** Secrets devem ir em:
- A) secret scope  B) código  C) .env  D) README

**36.** Para deploy do mesmo job em 3 ambientes:
- A) DABs targets  B) 3 workspaces  C) cache  D) nada

**37.** External table:
- A) exige external location  B) é gerenciada  C) não existe  D) nada

**38.** Pseudonimização na Prata:
- A) reduz PII em consumo  B) aumenta  C) nada  D) cache

**39.** Result caching do warehouse:
- A) reusa resultados 24h  B) apaga  C) treina  D) nada

**40.** Para monitorar drift de coluna:
- A) Lakehouse Monitoring  B) cache  C) DABs  D) nada
"""),
        teoria(
            "Gabarito DEP (21–40)",
            "**21-A** · **22-A** · **23-A** · **24-A** · **25-A** · **26-A** · "
            "**27-A** · **28-A** · **29-A** · **30-A** · **31-A** · **32-A** · "
            "**33-A** · **34-A** · **35-A** · **36-A** · **37-A** · **38-A** · "
            "**39-A** · **40-A**.\n\n"
            "≥ 32/40 (80%) = agende a DEP. 28–31 = revise. < 28 = refaça semanas 5–9.",
        ),
        dica_prova("DEP é a prova do 'para que serve'. Antes de responder, pergunte-se: "
                   "qual problema a ferramenta resolve? A resposta certa é a que "
                   "descreve a função, não a implementação."),
        exercicios([
            "Marque sua nota e liste os temas errados.",
            "Agende a DEP real (ou data alvo).",
        ]),
        gabarito([
            ("Nota",
             "≥ 32/40 para agendar; temas errados → semana correspondente (5–9)."),
            ("Agendamento",
             "Pearson VUE → DEP → OnVUE. Validade 2 anos."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana19_dia4_simulado_genai_completo",
    [
        header(
            "19", "4", "📜 Simulado GenAI Associate completo (40 questões)",
            "Validar o nível GenAI com um simulado alinhado aos 5 domínios da prova 2026.",
            "GenAI Engineer Associate (simulado)", "Simulado GenAI ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "Domínios da prova GenAI Associate (2026)",
            "- Design (~20%): arquitetura RAG, chunking, embeddings\n"
            "- Data Prep (~20%): preprocessing, Vector Search, Delta Sync\n"
            "- Application Dev (~25%): LangChain, prompts, FMA\n"
            "- Governance (~15%): AI Gateway, acesso a modelos, custo\n"
            "- Evaluation & Monitoring (~20%): mlflow.evaluate, tracing, A/B",
        ),
        pratica("Simulado GenAI (20 questões)",
            "Marque antes do gabarito."),
        md("""### Questões GenAI (1–20)

**1.** Para responder sobre dados que mudam diariamente:
- A) RAG  B) fine-tuning  C) re-treinar  D) cache

**2.** A janela de contexto é:
- A) limite de tokens por chamada  B) tamanho do disco  C) GPU  D) nada

**3.** Embeddings aproximam:
- A) textos semelhantes  B) tokens  C) números  D) nada

**4.** Chunking serve para:
- A) caber na janela + relevância  B) comprimir  C) criptografar  D) nada

**5.** Índice que sincroniza com Delta:
- A) DELTA_SYNC  B) MANAGED  C) INDEX  D) AUTO

**6.** FMA é:
- A) Foundation Model APIs  B) um banco  C) cluster  D) job

**7.** Faithfulness mede:
- A) resposta segue o contexto  B) velocidade  C) custo  D) tokens

**8.** Answer relevance mede:
- A) resposta responde a pergunta  B) latência  C) GPU  D) nada

**9.** LLM-as-judge usa:
- A) um LLM para avaliar  B) humanos sempre  C) SQL  D) nada

**10.** RRF funde:
- A) rankings lexical e semântico  B) modelos  C) tabelas  D) nada

**11.** Reranking usa:
- A) cross-encoder no top-N  B) cache  C) GPU sempre  D) nada

**12.** Para o modelo seguir formato JSON da empresa:
- A) fine-tuning  B) RAG  C) cache  D) nada

**13.** AI Gateway NÃO faz:
- A) treinar  B) rotear  C) fallback  D) cache semântico

**14.** Tracing serve para:
- A) debugar spans  B) treinar  C) custo  D) nada

**15.** Metadata de chunk permite:
- A) filtro e citação  B) compressão  C) nada  D) cache

**16.** Para reduzir custo de LLM:
- A) cache semântico + roteamento  B) modelo maior  C) mais contexto  D) GPU

**17.** Provisioned throughput:
- A) recurso pago  B) gratuito  C) cache  D) nada

**18.** Golden set é:
- A) perguntas com resposta esperada  B) modelo  C) tabela Bronze  D) nada

**19.** Para debug de agente (tool chamada):
- A) traces  B) cache  C) DABs  D) nada

**20.** Vector Search + filtro de metadata:
- A) busca restrita por coluna  B) busca global  C) nada  D) cache
"""),
        teoria(
            "Gabarito GenAI (1–20)",
            "**1-A** · **2-A** · **3-A** · **4-A** · **5-A** · **6-A** · **7-A** · "
            "**8-A** · **9-A** · **10-A** · **11-A** · **12-A** · **13-A** · "
            "**14-A** · **15-A** · **16-A** · **17-A** · **18-A** · **19-A** · "
            "**20-A**.",
        ),
        pratica("Simulado GenAI (21–40)",
            "Segunda metade."),
        md("""### Questões GenAI (21–40)

**21.** Tool calling é:
- A) o LLM decide chamar tool  B) cache  C) SQL  D) nada

**22.** UC Functions servem para:
- A) tools governadas  B) storage  C) jobs  D) nada

**23.** Para Text-to-SQL seguro:
- A) SELECT only + validação  B) SQL livre  C) cache  D) nada

**24.** Guardrail de saída protege:
- A) PII na resposta  B) entrada  C) custo  D) nada

**25.** Reflexion é:
- A) gerar, avaliar, corrigir  B) mais tools  C) GPU  D) nada

**26.** Multi-agente usa:
- A) coordenador + especialistas  B) um LLM só  C) cache  D) nada

**27.** Agent Bricks oferece:
- A) avaliação + guardrails + deploy  B) só UI  C) só SQL  D) nada

**28.** Genie Ontology resolve:
- A) métricas com fórmula oficial  B) latência  C) custo  D) nada

**29.** MCP é:
- A) protocolo de ferramentas  B) modelo  C) banco  D) job

**30.** Sandbox Python:
- A) execução isolada  B) instala libs  C) acelera  D) nada

**31.** Para auditar agente:
- A) logar turnos em Delta  B) cache  C) DABs  D) nada

**32.** Tool correctness mede:
- A) tool certa chamada  B) velocidade  C) custo  D) tokens

**33.** Model Serving serve:
- A) FMA e custom  B) só GPU  C) notebooks  D) nada

**34.** Para sessão de agente transacional:
- A) Lakebase  B) Delta  C) cache  D) nada

**35.** pgvector HNSW:
- A) índice vetorial preciso  B) cache  C) SQL  D) nada

**36.** Lakebase Search:
- A) busca híbrida nativa  B) só BM25  C) só vetores  D) nada

**37.** Streaming de resposta melhora:
- A) percepção de velocidade  B) exatidão  C) custo  D) nada

**38.** Para avaliar regressão de RAG:
- A) golden set + mlflow.evaluate  B) cache  C) DABs  D) nada

**39.** Prompt injection é bloqueado por:
- A) guardrails  B) cache  C) GPU  D) nada

**40.** O padrão oficial de agentes no Databricks:
- A) Mosaic AI Agent Framework  B) cache  C) DABs  D) nada
"""),
        teoria(
            "Gabarito GenAI (21–40)",
            "**21-A** · **22-A** · **23-A** · **24-A** · **25-A** · **26-A** · "
            "**27-A** · **28-A** · **29-A** · **30-A** · **31-A** · **32-A** · "
            "**33-A** · **34-A** · **35-A** · **36-A** · **37-A** · **38-A** · "
            "**39-A** · **40-A**.\n\n"
            "≥ 32/40 = agende a GenAI. Errou ≥ 6 → revise Semanas 11–15.",
        ),
        dica_prova("GenAI: a prova testa decisão (RAG vs FT, qual ferramenta) e "
                   "conceito (janela, embeddings, métricas). Revise o glossário das "
                   "Semanas 11–15."),
        exercicios([
            "Marque sua nota e liste os domínios fracos.",
            "Agende a GenAI real (ou data alvo).",
        ]),
        gabarito([
            ("Nota",
             "≥ 32/40 para agendar; domínios fracos → semana correspondente."),
            ("Agendamento",
             "Pearson VUE → GenAI Associate → OnVUE."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana19_dia5_entrevistas_internacionais_carreira",
    [
        header(
            "19", "5", "Entrevistas internacionais, salários e estratégia de carreira",
            "Preparar entrevistas técnicas em inglês (com perguntas e respostas), "
            "entender o mercado (US/EU/UK) e montar a presença profissional.",
            "Carreira", "Material de entrevista pronto",
            "✅ Free Edition",
        ),
        teoria(
            "O mercado internacional Databricks (2026)",
            "- **EUA**: Senior DE $150–220k; GenAI Engineer $160–240k\n"
            "- **UK**: £75–130k; **UE (Alemanha/Holanda)**: €85–140k\n"
            "- **Remoto internacional**: comum para sênior (fuso e inglês)\n"
            "- Certificações pesam: DEA/DEP + GenAI = diferenciador imediato",
        ),
        pratica("30 perguntas de entrevista (amostra — respostas no gabarito)",
            "Pratique as 10 primeiras em voz alta, em inglês."),
        md("""### Perguntas técnicas (EN)

1. Explain the Medallion architecture and when you would use it.
2. What is the difference between a managed and an external table?
3. How does Delta Lake's Time Travel work?
4. When would you use Liquid Clustering vs partitioning?
5. What is a shuffle and why is it expensive?
6. How do DABs help with CI/CD?
7. What is RAG and when would you choose it over fine-tuning?
8. How do you evaluate a RAG system?
9. What is the ReAct loop?
10. How do you secure a Text-to-SQL agent?
"""),
        teoria(
            "Como responder (método STAR-técnico)",
            "Para cada pergunta: **Conceito** (1 frase) → **Como funciona** (mecânica) → "
            "**Exemplo do seu projeto** → **Trade-off/decisão**. Ex.:\n\n"
            "\"I use the Medallion architecture to separate raw, cleaned and aggregated "
            "data. In my retail project, Auto Loader ingests CSV into Bronze, DLT with "
            "expectations builds Silver, and Gold serves dashboards and ML. The trade-off "
            "is extra storage for reproducibility.\"",
        ),
        pratica("Portfólio e presença",
            "1. README do repo com diagrama + métricas + links dos apps.\n"
            "2. LinkedIn: título com 'Databricks' + certificações.\n"
            "3. GitHub: projeto_final.ipynb + apps + DABs.\n"
            "4. Contribua ao databricks-industry-solutions (open source).",
        ),
        dica_prova("Entrevista: menos decoreba, mais 'decisão + porquê'. Prepare 3 "
                   "histórias (pipelines, GenAI, governança) com o método STAR."),
        exercicios([
            "Grave-se respondendo 5 perguntas em inglês.",
            "Escreva seu perfil LinkedIn (EN) destacando o projeto.",
            "Complete as 30 perguntas (10/dia) com o gabarito.",
        ]),
        gabarito([
            ("Respostas 1–10",
             "1) Bronze/Prata/Ouro com reprocessamento e qualidade. 2) UC gerencia vs "
             "LOCATION externo; DROP apaga vs preserva. 3) _delta_log + versionAsOf/"
             "timestampAsOf. 4) Cardinalidade e filtros (cluster para alta cardinalidade). "
             "5) Movimento de dados entre partições (rede+disco). 6) IaC: validate/plan/"
             "deploy + targets. 7) RAG injeta contexto; FT muda comportamento. 8) 4 "
             "métricas de ouro + golden set. 9) Raciocina→age→observa. 10) SELECT-only + "
             "validação + RLS + auditoria."),
            ("Perfil LinkedIn",
             "Headline: 'Data & AI Engineer — Databricks (DEA/DEP/GenAI)'. Destaque o "
             "projeto com links."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana19_dia6_checklist_competencias_roadmap",
    [
        header(
            "19", "6", "Checklist de 40 competências, repositório final e roadmap",
            "Validar as 40 competências do especialista, finalizar o repositório e "
            "planejar a recertificação e evolução.",
            "Carreira", "Checklist completo + repo final",
            "✅ Free Edition",
        ),
        teoria(
            "As 40 competências do Especialista Databricks",
            "**Plataforma (1–5)**: workspace/notebooks · SQL warehouse · UC 3 níveis · "
            "Volumes · compute serverless\n"
            "**Engenharia (6–13)**: Spark SQL/DataFrame · Delta (ACID/time travel/merge) · "
            "Medallion · Auto Loader · Streaming · DLT · Jobs · DABs+CI/CD\n"
            "**Governança (14–20)**: RLS/masking · linhagem · system tables · Federation · "
            "Sharing · custos · CLI/API\n"
            "**Performance (21–23)**: Liquid Clustering · OPTIMIZE/VACUUM · tuning (AQE/"
            "broadcast/cache)\n"
            "**ML/MLOps (24–26)**: MLflow · Feature Engineering · Model Serving\n"
            "**GenAI (27–30)**: FMA+prompts · embeddings/chunking · Vector Search · "
            "avaliação/gateway\n"
            "**Agentes (31–34)**: ReAct/Reflexion/multi · tools UC · Text-to-SQL · "
            "MCP/Ontologia\n"
            "**Aplicações (35–38)**: Apps (Streamlit/Next.js) · Lakebase/pgvector · "
            "segurança · observabilidade\n"
            "**Carreira (39–40)**: entrevista EN · portfólio",
        ),
        pratica("Checklist interativo",
            "Marque as competências que você domina."),
        code('# Checklist (rode e marque 1 para dominadas)\n'
             'competencias = {\n'
             '    "Delta Time Travel": 1, "DLT expectations": 1, "SCD2": 1,\n'
             '    "DABs + CI/CD": 1, "RLS/masking": 1, "Liquid Clustering": 1,\n'
             '    "MLflow evaluate": 1, "RAG (4 métricas)": 1, "Agente ReAct": 1,\n'
             '    "Apps full-stack": 1, "Lakebase": 1, "MCP": 1,\n'
             '}\n'
             'dominadas = sum(competencias.values())\n'
             'print(f"{dominadas}/{len(competencias)} competências-chave dominadas")\n'
             'print("Objetivo: 12/12 — se faltar, revise a semana correspondente.")'),
        pratica("Repositório final",
            "Estrutura profissional do GitHub:"),
        code('# Estrutura do repo final\n'
             'print("""\n'
             'databricks-course/\n'
             ' ├── README.md          # arquitetura + links + métricas\n'
             ' ├── notebooks/         # 114 notebooks do curso\n'
             ' ├── apps/              # dashboard + chat RAG + full-stack\n'
             ' ├── bundles/           # DABs (jobs, pipelines, apps)\n'
             ' ├── .github/           # CI/CD\n'
             ' └── docs/              # ADRs, diagramas, glossário EN\n'
             '""")\n'
             'print("Estruture o repo e faça o commit final.")'),
        pratica("Roadmap pós-curso",
            "1. Agende as provas (DEA → GenAI → DEP → MLP opcional).\n"
            "2. Recertificação a cada 2 anos.\n"
            "3. Evolua: contribua a open source, blog sobre o projeto.\n"
            "4. Aplique para vagas (DE sênior / GenAI Engineer)."),
        dica_prova("O curso te deu: plataforma completa + 3–4 certificações + portfólio "
                   "real. O que falta é só agendar as provas e aplicar — o conhecimento "
                   "está construído."),
        exercicios([
            "Finalize o README com diagrama, métricas e links.",
            "Crie a lista de 10 empresas-alvo (internacionais) e os requisitos de cada vaga.",
        ]),
        gabarito([
            ("README",
             "Deve conter: visão, arquitetura (mermaid), tabela de entregáveis por fase, "
             "métricas do modelo/RAG, links dos apps, certificações."),
            ("Empresas",
             "Liste requisitos e compare com suas 40 competências — preencha as lacunas "
             "com os notebooks."),
        ]),
        footer([
            "Validei as 40 competências.",
            "Finalizei o repositório profissional.",
            "Tenho plano de certificações e recertificação.",
            "🎉 Curso concluído — Especialista Databricks!",
        ]),
    ],
))
