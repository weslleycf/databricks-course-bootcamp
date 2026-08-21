"""Semana 9 — Observabilidade, Custos, Serverless, Genie + Simulado DEA (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana9_dia1_lakehouse_monitoring_drift",
    [
        header(
            "9", "1", "Lakehouse Monitoring: qualidade e drift",
            "Monitorar a saúde dos dados: quality monitors, drift de schema e de dados, e "
            "alertas automáticos.",
            "DEP (observabilidade)", "Monitor ativo em tabela do projeto",
            "✅ Free Edition (básico) + 🔑 avançado (trial)",
        ),
        teoria(
            "O problema: dados degradam",
            "Dados mudam com o tempo: schema muda (coluna nova), distribuição muda "
            "(drift), qualidade cai (nulos sobem). Quem consome o Ouro precisa saber "
            "ANTES de quebrar.\n\n"
            "**Lakehouse Monitoring** cria **monitores** em tabelas que calculam métricas "
            "e **alertam em drift**:\n"
            "- drift de schema (colunas novas/removidas)\n"
            "- drift de dados (distribuição de valores/estatísticas)\n"
            "- qualidade (expectations/constraints violadas)",
        ),
        teoria(
            "Como funciona",
            "1. Você cria um monitor numa tabela (`CREATE MONITOR ...` via UI).\n"
            "2. O Databricks calcula perfis (contagem, min/max, quantis, nulos, tipos).\n"
            "3. Execuções seguintes comparam com a **baseline** e sinalizam drift.\n"
            "4. Alertas notificam a equipe.\n\n"
            "> Na Free Edition o monitor básico existe; o avançado (agendamento, "
            "integração com alertas) roda no trial pago.",
        ),
        pratica("Criando um monitor",
            "Pela UI: **Catalog → workspace.ouro.vendas_por_dia → Quality → Create Monitor**."),
        code('# Monitor via SQL (existe em contas com o recurso)\n'
             'monitor_sql = """\n'
             'CREATE MONITOR workspace.ouro.vendas_por_dia\n'
             'ON TABLE workspace.ouro.vendas_por_dia\n'
             'WITH (metric_type = \'data_quality\')\n'
             '"""\n'
             'print(monitor_sql)\n'
             'print("Na Free, prefira a UI: Catalog > tabela > Quality > Create Monitor.")'),
        code('# Ver os perfis calculados\n'
             'display(spark.sql("SELECT * FROM workspace.ouro.vendas_por_dia LIMIT 5"))\n'
             'print("O monitor grava métricas em tabela system/table de perfil.")'),
        pratica("Drift na prática",
            "Simule um drift (mudança de distribuição) e observe."),
        code('# Simular: adicionar muitas linhas de um país novo\n'
             'novo_pais = spark.table("workspace.bronze.vendas_bronze").filter("Country = \'France\'")\n'
             'novo_pais.write.mode("append").saveAsTable("workspace.ouro.vendas_por_dia")\n'
             'print("Drift simulado: distribuição por país mudou.")'),
        dica_prova("DEP: Lakehouse Monitoring cobre **drift de schema e de dados** e "
                   "**quality monitors**. Pergunta: 'como detectar que a distribuição de "
                   "uma coluna mudou?' → monitor de drift."),
        exercicios([
            "Crie um monitor na sua tabela Ouro favorita (UI).",
            "O que a baseline faz no monitor?",
            "Como você alertaria a equipe quando o drift passar de um limite?",
        ]),
        gabarito([
            ("Monitor",
             "Catalog → tabela → Quality → Create Monitor; escolha as colunas e métricas."),
            ("Baseline",
             "É o perfil inicial de referência; execuções seguintes comparam e calculam a "
             "magnitude do drift vs essa linha de base."),
            ("Alerta",
             "Configure alertas (e-mail/Slack) vinculados ao monitor — ou em produção, "
             "integração com o sistema de observabilidade da empresa."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana9_dia2_custos_otimizacao_10_regras",
    [
        header(
            "9", "2", "Gestão de custos: as 10 regras que economizam até 80%",
            "Entender a fatura do Databricks (DBU), tags, budget alerts e as 10 regras "
            "práticas de economia — tópico obrigatório em entrevistas.",
            "DEP (custos)", "Política de custos documentada",
            "✅ Free Edition (conceito) + 🔑 billing real (trial)",
        ),
        teoria(
            "Como o Databricks cobra",
            "A cobrança é por **DBU (Databricks Unit)**: uma unidade de processamento "
            "conforme o tipo de workload. Fatores da fatura:\n"
            "- Tipo de compute (serverless, SQL warehouse, jobs)\n"
            "- Tempo de execução × tamanho do cluster\n"
            "- Model serving / FMA (tokens)\n\n"
            "**Tags** marcam recursos por projeto/time/custo. **Budget alerts** avisam "
            "quando o gasto passa do limite.",
        ),
        teoria(
            "As 10 regras de economia",
            "1. **Pare o que não usa** — auto-stop de warehouses/clusters (maior economia)\n"
            "2. **Escolha o compute certo** — serverless para ad hoc; jobs para carga\n"
            "3. **Reduza o shuffle** — broadcast join, chaves boas\n"
            "4. **Use Delta/Liquid Clustering** — menos leitura, menos DBU\n"
            "5. **Filtre cedo** — não leia colunas/linhas que não precisa\n"
            "6. **Modo triggered** em vez de continuous quando possível\n"
            "7. **Cache e result caching** para dashboards\n"
            "8. **Evite UDFs** — expressões nativas\n"
            "9. **Frequência certa de jobs** — diário em vez de horário\n"
            "10. **Monitore** — system tables de billing, budget alerts",
        ),
        pratica("Tags e budget (trial)",
            "Na conta paga: Compute → SQL Warehouse → Tags; e Billing → Budget alerts."),
        code('# Tags nos recursos\n'
             'tags = """\n'
             '# Compute > SQL Warehouse > Tags\n'
             '# cost_center=curso\n'
             '# project=vendas\n'
             '# owner=wesll\n'
             '"""\n'
             'print(tags)\n'
             'print("Tags permitem faturamento por projeto — essencial em empresas.")'),
        code('# Consultar billing (produção)\n'
             'billing_sql = """\n'
             'SELECT usage_metadata.ws_id, sku_name,\n'
             '       SUM(usage_quantity) AS dbu\n'
             'FROM system.billing.usage\n'
             'GROUP BY 1, 2 ORDER BY dbu DESC\n'
             '"""\n'
             'print(billing_sql)'),
        dica_prova("Pergunta de entrevista garantida: 'como reduzir custo de pipeline?' — "
                   "cite 3 das 10 regras com justificativa. Na prova DEP, a pergunta vira "
                   "'qual configuração reduz custo X?' → auto-stop, triggered, serverless."),
        exercicios([
            "Liste 5 das 10 regras com uma frase de impacto cada.",
            "O que são tags e para que servem?",
            "Simule: um warehouse 2X-Small rodando 24h vs auto-stop em 15 min — onde está a economia?",
        ]),
        gabarito([
            ("5 regras",
             "Auto-stop, compute certo, menos shuffle, clustering, triggered — cada uma "
             "corta DBUs desperdiçados."),
            ("Tags",
             "Metadados (projeto/time/dono) nos recursos — base para chargeback e "
             "identificação de gasto anômalo."),
            ("Auto-stop",
             "O warehouse ligado 24h cobra DBU mesmo ocioso; auto-stop em 15 min zera o "
             "custo de inatividade — a economia nº 1."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana9_dia3_serverless_lakeflow_connect",
    [
        header(
            "9", "3", "Serverless compute e Lakeflow Connect",
            "Entender o modelo serverless (cobrado no DEP 2026) e a ingestão gerenciada "
            "com Lakeflow Connect.",
            "DEP (2026)", "Matriz de decisão de compute documentada",
            "✅ Free Edition (conceito) + 🔑 Lakeflow Connect (trial)",
        ),
        teoria(
            "Serverless compute (DEP 2026)",
            "O **serverless** elimina a gestão de clusters: o Databricks provisiona e "
            "escala o compute sob demanda (notebooks, jobs, SQL).\n\n"
            "Vantagens: zero configuração, scale-to-zero (paga só quando roda), manutenção "
            "automática. Trade-off: menos controle fino (pool, políticas) e preço por DBU "
            "diferente.\n\n"
            "**Quando usar**: ad hoc, workloads variáveis, times sem infra dedicada.\n"
            "**Quando usar clássico (pago)**: workload estável e previsível, necessidade "
            "de init scripts/policies, GPU dedicada.",
        ),
        teoria(
            "Lakeflow Connect (DEP 2026)",
            "O **Lakeflow Connect** é a ingestão **gerenciada e sem código** de fontes "
            "externas (SaaS como Salesforce, Workday, ServiceNow, bancos de dados) direto "
            "para o Lakehouse, com incrementais e schema automáticos.\n\n"
            "> ⚠️ Lakeflow Connect é recurso de conta paga — na Free estude o conceito e "
            "valide no trial.",
        ),
        pratica("Matriz de decisão de compute",
            "Complete a tabela de decisão do seu projeto."),
        code('# Matriz de decisão (complete com seus casos)\n'
             'matriz = """\n'
             '| Caso | Compute ideal | Por quê |\n'
             '|---|---|---|\n'
             '| Consulta ad hoc de BI | SQL Warehouse serverless | escala + auto-stop |\n'
             '| Job diário estável | Job cluster / serverless jobs | paga só na execução |\n'
             '| Streaming contínuo | Continuous (pago) | latência |\n'
             '| Notebook exploratório | Notebook serverless | sem config |\n'
             '| Fine-tune GPU | GPU cluster (pago) | GPU dedicada |\n'
             '"""\n'
             'print(matriz)'),
        code('# Lakeflow Connect — fluxo (trial)\n'
             'print("""\n'
             '1. Catalog > Add > Source (Lakeflow Connect)\n'
             '2. Escolha a fonte (Salesforce, Workday, Postgres...)\n'
             '3. Credenciais + tabelas/objetos\n'
             '4. Defina frequência (incremental automático)\n'
             '5. Pronto: tabelas bronze atualizadas sem código\n'
             '""")\n'
             'print("Ingestão gerenciada — padrão para integrar SaaS sem engenharia manual.")'),
        dica_prova("DEP 2026 adicionou **Serverless Compute** e **Lakeflow Connect** ao "
                   "escopo. Memorize: serverless = sem cluster próprio; Connect = ingestão "
                   "SaaS sem código."),
        exercicios([
            "Diferencie serverless de cluster clássico em 2 frases.",
            "Qual recurso ingere Salesforce sem código?",
            "Quando você escolheria cluster clássico em vez de serverless?",
        ]),
        gabarito([
            ("Serverless",
             "Serverless: plataforma gerencia tudo, escala sob demanda, paga por uso. "
             "Clássico: você controla máquinas, init scripts e políticas."),
            ("Lakeflow Connect",
             "Lakeflow Connect — ingestão gerenciada de SaaS/bancos direto para o "
             "Lakehouse."),
            ("Clássico",
             "Quando precisa de init scripts, cluster policies, GPU estável ou workloads "
             "previsíveis que justificam cluster dedicado."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana9_dia4_genie_ai_bi_language_natural",
    [
        header(
            "9", "4", "Genie (AI/BI): análise em linguagem natural",
            "Usar o Genie para responder perguntas de negócio em linguagem natural sobre "
            "o Ouro — e entender o Genie Code.",
            "DAA (Genie 2026), GenAI", "Genie space respondendo perguntas do projeto",
            "✅ Free Edition",
        ),
        teoria(
            "O que é o Genie",
            "O **Genie** é o assistente conversacional de BI do Databricks: você pergunta "
            "em linguagem natural ('qual o país com mais receita em novembro?') e ele "
            "gera/executa SQL sobre as tabelas que você autorizou.\n\n"
            "- **Genie spaces**: coleções de tabelas + instruções para o assistente\n"
            "- **Genie Code**: modo que mostra o SQL gerado (transparência e correção)\n"
            "- **Ontologia** (DAIS 2026, 🔑): define métricas e cálculos padrão — o Genie "
            "não erra conta porque conhece a definição oficial",
        ),
        pratica("Criando um Genie space",
            "1. **AI/BI → Genie → New space**.\n"
            "2. Adicione as tabelas: `workspace.ouro.vendas_por_dia`, `workspace.ouro.receita_por_pais`, "
            "`workspace.ouro.top_produtos`.\n"
            "3. Escreva instruções (prompt do space): 'Sempre use receita como "
            "Quantity*UnitPrice; responda em português'.\n"
            "4. Pergunte: 'Qual o top 5 de países por receita?'",
        ),
        pratica("Genie Code",
            "No Genie, ative o **Code mode** para ver o SQL gerado — aprenda com ele e "
            "valide a resposta."),
        code('# O que o Genie gera (exemplo do SQL por trás da resposta)\n'
             'sql_exemplo = """\n'
             'SELECT Country, SUM(Quantity * UnitPrice) AS receita\n'
             'FROM workspace.bronze.vendas_bronze\n'
             'GROUP BY Country\n'
             'ORDER BY receita DESC\n'
             'LIMIT 5\n'
             '"""\n'
             'print(sql_exemplo)\n'
             'print("Valide: rode este SQL você mesmo e compare com a resposta do Genie.")'),
        pratica("Perguntas de negócio",
            "Teste o Genie com perguntas cada vez mais complexas."),
        code('# Perguntas para testar no Genie\n'
             'perguntas = """\n'
             '1. Qual o ticket médio por país?\n'
             '2. Compare a receita de novembro vs outubro.\n'
             '3. Quais os 3 produtos mais vendidos no Reino Unido?\n'
             '4. Qual a receita acumulada por mês em 2024?\n'
             '5. (Ontologia, 🔑) Qual o ARPU por cliente?\n'
             '"""\n'
             'print(perguntas)'),
        dica_prova("DAA 2026 inclui **Genie**. Pergunta típica: 'qual ferramenta responde "
                   "perguntas em linguagem natural sobre dados?' → Genie; 'como garantir "
                   "que a métrica está correta?' → Genie Ontology (definição canônica)."),
        exercicios([
            "Crie um Genie space com 3 tabelas e faça 5 perguntas.",
            "Qual a vantagem do Genie Code mode?",
            "O que a Ontologia resolve?",
        ]),
        gabarito([
            ("Space",
             "AI/BI → Genie → New space → tabelas → instruções → perguntar."),
            ("Code mode",
             "Mostra o SQL gerado: transparência, aprendizado e correção manual quando a "
             "resposta não fizer sentido."),
            ("Ontologia",
             "Define métricas e cálculos oficiais — o Genie usa a definição canônica e "
             "para de 'inventar' fórmulas (a causa nº 1 de erro em BI conversacional)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana9_dia5_dashboards_avancados_alerts",
    [
        header(
            "9", "5", "Dashboards avançados, alertas e result caching",
            "Levar o BI do projeto a nível profissional: dashboards interativos, alertas "
            "e a estratégia de result caching do SQL Warehouse.",
            "DAA, DEP", "Dashboard + alertas configurados",
            "✅ Free Edition",
        ),
        teoria(
            "BI profissional no Databricks SQL",
            "- **Dashboards**: múltiplas visualizações com filtros (parâmetros) linkados\n"
            "- **Alerts**: condições com notificação (e-mail/Slack)\n"
            "- **Result caching**: o SQL Warehouse guarda resultados por até 24h — "
            "consultas iguais retornam instantaneamente (e sem DBU!)\n"
            "- **Schedules**: queries agendadas (ex.: 8h diária)",
        ),
        pratica("Dashboard com filtros",
            "Crie um dashboard com parâmetro de país que filtra todas as visualizações."),
        sql('-- Query com parâmetro {{pais}}\n'
            'SELECT Country, DATE_TRUNC("month", InvoiceDate) AS mes,\n'
            '       SUM(Quantity * UnitPrice) AS receita\n'
            'FROM workspace.bronze.vendas_bronze\n'
            'WHERE Country = {{pais}}\n'
            'GROUP BY 1, 2\n'
            'ORDER BY mes'),
        pratica("Alertas e agendamento",
            "1. Salve a query `alerta_receita_diaria` (receita de hoje vs ontem).\n"
            "2. Crie o **alert**: se variação < -20% → notificar.\n"
            "3. Agende a query para rodar 07:50 (antes do expediente).",
        ),
        code('# Query de alerta (receita do dia vs dia anterior)\n'
             'sql_alerta = """\n'
             'WITH rec AS (\n'
             '  SELECT DATE_TRUNC(\'day\', InvoiceDate) dia, SUM(Quantity*UnitPrice) receita\n'
             '  FROM workspace.bronze.vendas_bronze GROUP BY 1)\n'
             'SELECT (receita - LAG(receita) OVER (ORDER BY dia)) / LAG(receita) OVER (ORDER BY dia) * 100 AS var_pct\n'
             'FROM rec ORDER BY dia DESC LIMIT 1\n'
             '"""\n'
             'print(sql_alerta)'),
        dica_prova("Result caching: consultas repetidas retornam do cache (rápido, sem "
                   "compute). O cache é invalidado quando a tabela muda. Pergunta típica "
                   "de DEP: 'por que a 2a execução é mais rápida?' → result caching."),
        exercicios([
            "Crie um dashboard com 3 visualizações e um filtro de país.",
            "Configure um alerta de queda de receita > 20%.",
            "Explique o result caching em 2 frases.",
        ]),
        gabarito([
            ("Dashboard",
             "Queries com parâmetro {{pais}} + dashboard → Add filter → ligar às "
             "visualizações."),
            ("Alerta",
             "Nova query (variação) → Save → Create Alert → condição < -20 → notificação "
             "por e-mail."),
            ("Result caching",
             "O warehouse guarda o resultado de queries por até 24h; consultas idênticas "
             "voltam do cache sem reprocessar — mais rápido e sem custo de DBU."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana9_dia6_simulado_dea_completo",
    [
        header(
            "9", "6", "📜 Simulado completo DEA (40 questões) + guia da prova",
            "Validar tudo o que você aprendeu nas Semanas 1–9 com um simulado no formato "
            "oficial e planejar o agendamento da prova real.",
            "DEA (simulado completo)", "Simulado DEA ≥ 70% + prova agendada",
            "✅ Free Edition",
        ),
        teoria(
            "Formato oficial da prova DEA (2026)",
            "- 45 questões, 120 minutos, Pearson VUE (online ou centro)\n"
            "- Domínios (pesos 2026): ELT com Spark SQL/Python · Unity Catalog (~30%) · "
            "Delta Lake · Lakeflow · qualidade de dados · medallion\n"
            "- Validade: 2 anos. Custo: ~$200 (verifique descontos)\n"
            "- Nota de corte: ~70% (não oficial; mire ≥ 80%)",
        ),
        pratica("Simulado — Parte 1: Plataforma, SQL, UC (20 questões)",
            "Marque antes do gabarito (40 questões totais — 20 aqui + 20 na parte 2)."),
        md("""### Parte 1 — Plataforma, SQL, Unity Catalog

**1.** Qual compute é usado para consultas SQL/BI?
- A) notebook serverless  B) SQL Warehouse  C) MLflow  D) DABs

**2.** Nome do namespace do UC:
- A) metastore.table  B) catalog.schema.object  C) schema.table.column  D) workspace.catalog

**3.** Para criar volume:
- A) CREATE VOLUME  B) CREATE BUCKET  C) MOUNT  D) dbfs

**4.** `%fs ls` lista:
- A) tabelas  B) arquivos do sistema de arquivos  C) jobs  D) volumes

**5.** RDD na DEA 2026:
- A) cobrado a fundo  B) fora do escopo  C) obrigatório  D) só em Scala

**6.** View temporária é criada com:
- A) saveAsTable  B) createOrReplaceTempView  C) createView  D) register

**7.** `GROUP BY` + `HAVING`: HAVING filtra:
- A) antes do group  B) depois da agregação  C) linhas  D) colunas

**8.** Window `ROW_NUMBER() OVER (PARTITION BY p ORDER BY v DESC)`:
- A) numera por partição  B) agrega  C) ordena tudo  D) remove duplicatas

**9.** Managed table com DROP:
- A) preserva arquivos  B) apaga dados  C) exige LOCATION  D) nada

**10.** External table requer:
- A) external location  B) volume  C) delta sharing  D) nada

**11.** Constraint CHECK violada:
- A) descarta linha  B) falha transação  C) remove constraint  D) loga e segue

**12.** Para RLS por linha:
- A) column masking  B) dynamic view + current_user  C) tag  D) GRANT de tabela

**13.** Para mascarar CPF:
- A) RLS  B) column masking  C) volume  D) view simples

**14.** system.access.audit guarda:
- A) linhagem  B) auditoria de acesso  C) custo  D) schema

**15.** Delta Time Travel consulta:
- A) versionAsOf  B) OPTIMIZE  C) VACUUM  D) MERGE

**16.** VACUUM (7 dias) remove:
- A) tudo  B) arquivos fora da retenção  C) log  D) nada

**17.** Liquid Clustering é definido com:
- A) ZORDER BY  B) CLUSTER BY  C) PARTITION BY  D) SORT BY

**18.** Z-ORDER (2026):
- A) recomendado  B) deprecado (usar CLUSTER BY)  C) obrigatório  D) removido

**19.** Para compartilhar tabela com parceiro:
- A) Federation  B) Delta Sharing  C) merge  D) volume

**20.** Para consultar dados externos (Postgres):
- A) Sharing  B) Lakehouse Federation  C) cache  D) external table
"""),
        pratica("Simulado — Parte 2: Spark, Delta, Lakeflow, qualidade (20 questões)",
            "Marque antes do gabarito."),
        md("""### Parte 2 — Spark, Delta, Lakeflow, qualidade

**21.** Lazy evaluation: transformações...
- A) executam na hora  B) constroem o DAG; ações executam  C) falham  D) nada

**22.** Onde rodam as tasks?
- A) driver  B) executores sobre partições  C) metastore  D) warehouse

**23.** Shuffle é:
- A) rápido  B) o operador mais caro  C) opcional em join  D) cache

**24.** Broadcast join é automático quando:
- A) sempre  B) tabela pequena  C) nunca  D) com índice

**25.** AQE faz:
- A) coalesce partições + broadcast dinâmico + skew  B) backup  C) schema  D) nada

**26.** cache() materializa:
- A) na chamada  B) na 1ª ação  C) nunca  D) no collect

**27.** MERGE é usado para:
- A) upsert  B) select  C) drop  D) describe

**28.** Schema evolution automática:
- A) autoMerge=true  B) mergeSchema  C) ALTER TABLE  D) todas válidas conforme contexto

**29.** Auto Loader:
- A) lê arquivos novos incrementalmente  B) escreve parquet  C) cria jobs  D) versiona

**30.** checkpointLocation garante:
- A) retomada sem reprocessar  B) schema  C) cache  D) backup

**31.** DLT @dlt.expect_or_drop:
- A) mantém e conta  B) descarta violadas  C) falha  D) nada

**32.** DLT materialized vs streaming:
- A) iguais  B) MT recalcula; ST incremental  C) MT só SQL  D) ST só Python

**33.** Lakeflow Jobs é:
- A) orquestrador  B) query engine  C) cofre  D) repo

**34.** 6 dimensões de qualidade NÃO inclui:
- A) completude  B) unicidade  C) velocidade  D) validade

**35.** Dimensão de um star schema:
- A) fato  B) dim_cliente  C) medida  D) agregação

**36.** Ouro contém:
- A) dados crus  B) agregados de negócio  C) logs  D) nada

**37.** Para SCD2 com histórico:
- A) UPDATE  B) APPLY CHANGES (type 2)  C) INSERT  D) DELETE

**38.** CDF (change data feed) permite:
- A) ler mudanças incrementais  B) cache  C) tuning  D) share

**39.** TTL nativo (DAIS 2026):
- A) expira dados automaticamente  B) cache  C) índice  D) share

**40.** Serverless:
- A) exige cluster próprio  B) plataforma gerencia o compute  C) mais config  D) RDD
"""),
        teoria(
            "Gabarito completo",
            "1-B · 2-B · 3-A · 4-B · 5-B · 6-B · 7-B · 8-A · 9-B · 10-A · 11-B · "
            "12-B · 13-B · 14-B · 15-A · 16-B · 17-B · 18-B · 19-B · 20-B · "
            "21-B · 22-B · 23-B · 24-B · 25-A · 26-B · 27-A · 28-D · 29-A · "
            "30-A · 31-B · 32-B · 33-A · 34-C · 35-B · 36-B · 37-B · 38-A · "
            "39-A · 40-B.\n\n"
            "≥ 32/40 (80%) = agende a prova. 28–31 = revise os temas errados. < 28 = "
            "refaça as semanas 1–9 focando nos erros.",
        ),
        pratica("Guia de agendamento",
            "1. Crie a conta no **Pearson VUE** (ou Databricks Academy → Exams).\n"
            "2. Escolha **DEA** → agende **OnVUE** (online) ou centro.\n"
            "3. Prepare: documento oficial, webcam, ambiente silencioso.\n"
            "4. Verifique descontos (estudante, promoções da Academy).\n"
            "5. Validade 2 anos — planeje a recertificação.",
        ),
        dica_prova("No dia da prova: leia 2x cada questão, cuidado com 'select all that "
                   "apply', e responda pelo que a DOCUMENTAÇÃO diz (não pelo que você faria "
                   "na prática)."),
        exercicios([
            "Marque sua nota: ____ /40. Liste os 5 temas que errou.",
            "Agende a prova real (ou anote a data alvo).",
            "Crie um plano de revisão de 3 dias antes da prova.",
        ]),
        gabarito([
            ("Nota",
             "≥ 32/40 para agendar; revise os erros por semana correspondente."),
            ("Agendamento",
             "Pearson VUE → DEA → OnVUE → data. Validade 2 anos."),
            ("Revisão",
             "3 dias: dia 1 UC + SQL; dia 2 Delta + Spark; dia 3 Lakeflow + qualidade + "
             "simulado branco."),
        ]),
        footer([
            "Fiz o simulado DEA completo e revisei todos os erros.",
            "Entendo custos, serverless, Genie e observabilidade.",
            "Tenho a data da prova real agendada (ou plano claro).",
            "Semanas 1–9 concluídas — base de engenharia sólida.",
        ]),
    ],
))
