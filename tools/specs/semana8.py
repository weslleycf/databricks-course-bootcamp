"""Semana 8 — Performance, CDC, SCD2 e DLT avançado (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana8_dia1_tuning_spark_aqe_broadcast_cache",
    [
        header(
            "8", "1", "Tuning Spark: AQE, broadcast join e cache estratégico",
            "Aplicar as técnicas que reduzem tempo de execução em até 10x: AQE, hints de "
            "join, shuffles e estratégia de cache.",
            "DEP (performance)", "Benchmark antes/depois documentado",
            "✅ Free Edition",
        ),
        teoria(
            "O caminho do tuning (na ordem certa)",
            "1. **Plano físico** (explain) — ver onde está o custo\n"
            "2. **Evitar shuffle** — broadcast join, boas chaves\n"
            "3. **AQE (Adaptive Query Execution)** — otimiza em runtime\n"
            "4. **Cache** — só para reuso real\n"
            "5. **Storage** — Liquid Clustering, OPTIMIZE\n\n"
            "> 🎯 **Dica de prova (DEP)**: tuning NÃO começa com `spark.conf`. Começa com o "
            "plano físico e a eliminação de shuffle.",
        ),
        teoria(
            "AQE — Adaptive Query Execution",
            "O AQE ajusta o plano **durante a execução**: reduz partições de shuffle quando "
            "há poucos dados, converte sort-merge em broadcast quando a tabela ficou pequena, "
            "e corrige skew (partições desbalanceadas).\n\n"
            "Configurações (raro mexer; entender é o que cai na prova):\n"
            "```\nspark.sql.adaptive.enabled=true\nspark.sql.adaptive.coalescePartitions.enabled=true\nspark.sql.adaptive.skewJoin.enabled=true\n```",
        ),
        pratica("Encontrando o custo no explain",
            "Compare o plano de um join e veja onde está o shuffle."),
        code('# Dataset de teste\n'
             'df = spark.table("workspace.prata.fato_vendas")\n'
             'dim = spark.table("workspace.prata.dim_produto")\n'
             'print("Fato:", df.count(), "| Dim:", dim.count())'),
        code('# Plano físico do join (identifique Exchange/Shuffle)\n'
             'plano = df.join(dim, "sk_produto", "left")\n'
             'print(plano.explain("formatted"))\n'
             'print("Procure: Exchange (shuffle) e SortMergeJoin vs BroadcastHashJoin")'),
        pratica("Forçando broadcast",
            "Uma dimensão pequena deve ser broadcast — economiza shuffle."),
        code('# Sem hint (pode shuffle)\n'
             't_sem = df.join(dim, "sk_produto", "left").count()\n'
             '# Com hint broadcast\n'
             't_com = df.join(dim.hint("broadcast"), "sk_produto", "left").count()\n'
             'print("Resultado igual:", t_sem == t_com)\n'
             'print("Veja no explain: BroadcastExchange eliminou o shuffle.")'),
        pratica("Cache estratégico",
            "Meça o efeito de cache em reuso real."),
        code('# Sem cache: recalcula a cada uso\n'
             'import time\n'
             'base = spark.table("workspace.prata.fato_vendas").filter("Country = \'United Kingdom\'")\n'
             't0 = time.time(); base.groupBy("sk_produto").count().count(); t1 = time.time()\n'
             't2 = time.time(); base.groupBy("Country").count().count(); t3 = time.time()\n'
             'print(f"Sem cache: {t1-t0:.2f}s + {t3-t2:.2f}s (recalcula 2x)")'),
        code('# Com cache (uma vez em memória)\n'
             'base_cached = base.cache()\n'
             'base_cached.count()  # materializa\n'
             't0 = time.time(); base_cached.groupBy("sk_produto").count().count(); t1 = time.time()\n'
             't2 = time.time(); base_cached.groupBy("Country").count().count(); t3 = time.time()\n'
             'print(f"Com cache: {t1-t0:.2f}s + {t3-t2:.2f}s (mais rápido no reuso)")\n'
             'base_cached.unpersist()'),
        dica_prova("Pergunta DEP típica: 'o que o AQE faz?' → coalesce de partições, "
                   "conversão para broadcast, correção de skew. 'Como eliminar shuffle?' → "
                   "broadcast join em tabela pequena."),
        exercicios([
            "Explique por que broadcast join elimina o shuffle.",
            "Quais 3 otimizações o AQE faz em runtime?",
            "Quando cache NÃO ajuda?",
        ]),
        gabarito([
            ("Broadcast",
             "A tabela pequena é copiada para cada executor — o join roda localmente, sem "
             "mover linhas entre partições (sem Exchange)."),
            ("AQE",
             "1) coalesce partições de shuffle (une partições pequenas); 2) converte "
             "sort-merge em broadcast se o tamanho permitir; 3) corrige skew de join "
             "(divide partição quente)."),
            ("Cache sem reuso",
             "Se o DataFrame é usado 1x, cache só ocupa memória e adiciona trabalho (o "
             "primeiro count materializa na mesma velocidade). Cache paga quando o mesmo "
             "resultado é consumido várias vezes."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana8_dia2_particionamento_liquid_clustering_zorder",
    [
        header(
            "8", "2", "Particionamento vs Liquid Clustering vs Z-ORDER",
            "Escolher a estratégia de organização física certa e aplicar OPTIMIZE/VACUUM "
            "por tamanho de tabela.",
            "DEP (performance)", "Estratégia de clustering aplicada + documentada",
            "✅ Free Edition",
        ),
        teoria(
            "As 3 estratégias",
            "| Estratégia | Como | Quando |\n|---|---|---|\n"
            "| **Particionamento** | pastas fixas por coluna | colunas de baixa cardinalidade; filtro exato (ano) |\n"
            "| **Liquid Clustering** (`CLUSTER BY`) | reordenamento adaptativo automático | padrão 2026; alta cardinalidade; múltiplos filtros |\n"
            "| **Z-ORDER** (legado) | índice de ordenação multi-coluna | ⚠️ deprecado — use CLUSTER BY |\n\n"
            "**Regra prática** (documentação Databricks):\n"
            "- < 1 TB: geralmente não precisa de particionamento/clustering — só OPTIMIZE.\n"
            "- > 1 TB com filtros frequentes: Liquid Clustering por 1–4 colunas.\n"
            "- Particionar SÓ por data (baixa cardinalidade e pruning efetivo).",
        ),
        pratica("Liquid Clustering na prática",
            "Crie uma tabela clusterizada e otimize."),
        sql('CREATE OR REPLACE TABLE workspace.prata.fato_vendas_cluster (\n'
            '  InvoiceNo STRING, StockCode STRING, sk_cliente LONG, sk_produto LONG,\n'
            '  data_venda DATE, Country STRING, Quantity INT, UnitPrice DOUBLE, receita DOUBLE)\n'
            'USING DELTA\n'
            'CLUSTER BY (Country, data_venda);'),
        code('# Popular a partir do Bronze\n'
             'from pyspark.sql.functions import to_date\n'
             'df = (spark.table("workspace.bronze.vendas_bronze")\n'
             '    .select("InvoiceNo", "StockCode", "Quantity", "UnitPrice", "Country",\n'
             '            to_date("InvoiceDate", "M/d/yyyy H:mm").alias("data_venda"))\n'
             '    .withColumn("receita", col("Quantity") * col("UnitPrice")))\n'
             'df.write.mode("overwrite").saveAsTable("workspace.prata.fato_vendas_cluster")\n'
             'print("Populado:", spark.table("workspace.prata.fato_vendas_cluster").count())'),
        code('# OPTIMIZE + histograma de clustering\n'
             'spark.sql("OPTIMIZE workspace.prata.fato_vendas_cluster")\n'
             'spark.sql("ANALYZE TABLE workspace.prata.fato_vendas_cluster COMPUTE STATISTICS")\n'
             'display(spark.sql("DESCRIBE DETAIL workspace.prata.fato_vendas_cluster"))'),
        pratica("Benchmark de leitura",
            "Compare leitura com e sem filtro na coluna de clustering."),
        code('# Filtro na coluna cluster (Country) — pruning eficiente\n'
             't0 = time.time()\n'
             'n1 = spark.sql("SELECT COUNT(*) FROM workspace.prata.fato_vendas_cluster WHERE Country = \'United Kingdom\'").collect()[0][0]\n'
             't1 = time.time()\n'
             'print(f"UK: {n1} linhas em {t1-t0:.2f}s (com clustering, lê menos arquivos)")'),
        dica_prova("Liquid Clustering (CLUSTER BY) é o padrão 2026; Z-ORDER está "
                   "deprecado. Pergunta típica: coluna de alta cardinalidade → clustering, "
                   "não particionamento."),
        exercicios([
            "Quando particionar vs clusterizar?",
            "Rode OPTIMIZE na sua fato_vendas_cluster e compare o tempo de uma query antes/depois.",
            "O que o histograma de clustering mostra?",
        ]),
        gabarito([
            ("Particionar vs cluster",
             "Particionar: baixa cardinalidade + filtro exato (ex.: ano). Cluster: alta "
             "cardinalidade, múltiplas colunas de filtro, escrita frequente."),
            ("Benchmark",
             "Anote o tempo antes (muitos arquivos) e depois (arquivos compactados e "
             "ordenados) — a melhora vem do pruning + menos arquivos."),
            ("Histograma",
             "Mostra o quanto os dados estão clusterizados por coluna (0-1): próximo de 1 = "
             "bem organizado para pruning."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana8_dia3_cdc_change_data_feed",
    [
        header(
            "8", "3", "CDC com Change Data Feed (CDF)",
            "Habilitar e consumir o Change Data Feed do Delta: captura de mudanças "
            "incrementais (insert/update/delete) para pipelines e streaming.",
            "DEP (CDC)", "CDF habilitado + leitura de mudanças",
            "✅ Free Edition",
        ),
        teoria(
            "O que é CDC e CDF",
            "**CDC (Change Data Capture)**: capturar mudanças nos dados (insert/update/"
            "delete) para propagar a outras camadas/sistemas.\n\n"
            "O **Change Data Feed (CDF)** do Delta registra **cada mudança** com metadados "
            "de operação e versão:\n\n"
            "| Coluna | Significado |\n|---|---|\n"
            "| `_change_type` | insert / update_preimage / update_postimage / delete |\n"
            "| `_commit_version` | versão do commit |\n"
            "| `_commit_timestamp` | quando |\n\n"
            "Uso: alimentar o Ouro incrementalmente, espelhar para outro sistema, "
            "auditoria, SCD.",
        ),
        pratica("Habilitando o CDF",
            "Habilite na criação da tabela (recomendado) ou por ALTER."),
        sql('CREATE OR REPLACE TABLE workspace.prata.dim_cliente_cdf (\n'
            '  CustomerID STRING, nome STRING, cidade STRING)\n'
            'USING DELTA\n'
            'TBLPROPERTIES (delta.enableChangeDataFeed = true);\n'
            'INSERT INTO workspace.prata.dim_cliente_cdf VALUES\n'
            '  (\'12345\', \'Ana\', \'SP\'),\n'
            '  (\'67890\', \'João\', \'RJ\');\n'
            'SHOW TBLPROPERTIES workspace.prata.dim_cliente_cdf;'),
        code('# Mudanças: update + delete\n'
             'spark.sql("UPDATE workspace.prata.dim_cliente_cdf SET cidade = \'CAMPINAS\' WHERE CustomerID = \'12345\'")\n'
             'spark.sql("DELETE FROM workspace.prata.dim_cliente_cdf WHERE CustomerID = \'67890\'")\n'
             'print("Update + delete executados.")'),
        pratica("Lendo o CDF",
            "Leia as mudanças geradas (versão mínima e/ou por timestamp)."),
        code('# Ler TODAS as mudanças\n'
             'mudancas = spark.read.format("delta")\\\n'
             '    .option("readChangeFeed", "true")\\\n'
             '    .table("workspace.prata.dim_cliente_cdf")\n'
             'mudancas.orderBy("_commit_version").show(truncate=False)'),
        code('# Ler mudanças a partir da versão 0 (incremental)\n'
             'spark.read.format("delta")\\\n'
             '    .option("readChangeFeed", "true")\\\n'
             '    .option("startingVersion", "0")\\\n'
             '    .table("workspace.prata.dim_cliente_cdf")\n'
             '    .show(truncate=False)'),
        pratica("Consumindo em streaming",
            "Streaming consome o CDF como se fosse uma fonte contínua."),
        code('# Streaming de mudanças (conceito — roda com trigger once no estudo)\n'
             'stream_mudancas = (spark.readStream\n'
             '    .format("delta")\n'
             '    .option("readChangeFeed", "true")\n'
             '    .table("workspace.prata.dim_cliente_cdf")\n'
             '    .writeStream\n'
             '    .format("delta")\n'
             '    .option("checkpointLocation", "/Volumes/workspace/bronze/vol_checkpoints/ckpt_cdf")\n'
             '    .outputMode("append")\n'
             '    .trigger(once=True)\n'
             '    .table("workspace.prata.dim_cliente_cdf_historico"))\n'
             'print("Streaming de CDF configurado (rode e veja as mudanças propagadas).")'),
        dica_prova("DEP: CDF = `readChangeFeed=true` + colunas `_change_type`, "
                   "`_commit_version`, `_commit_timestamp`. Pergunta: 'como propagar "
                   "mudanças do Delta para outro sistema?' → CDF."),
        exercicios([
            "O que `_change_type = update_postimage` significa?",
            "Habilite CDF em uma tabela existente via ALTER.",
            "Para que `startingVersion` serve no readChangeFeed?",
        ]),
        gabarito([
            ("update_postimage",
             "A linha APÓS o update — o estado novo. A versão anterior é "
             "update_preimage."),
            ("ALTER",
             "```sql\nALTER TABLE t SET TBLPROPERTIES (delta.enableChangeDataFeed = true)\n```"),
            ("startingVersion",
             "Define a partir de qual versão ler as mudanças — o checkpoint do streaming "
             "usa isso para continuar de onde parou."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana8_dia4_scd1_scd2_apply_changes",
    [
        header(
            "8", "4", "SCD1 e SCD2 com APPLY CHANGES INTO",
            "Implementar Slowly Changing Dimensions de verdade: SCD1 (correção) e SCD2 "
            "(histórico) usando o padrão `APPLY CHANGES INTO` do DLT.",
            "DEP (SCD)", "dim_cliente SCD2 rodando com histórico",
            "✅ Free Edition (via notebook com dlt em modo batch)",
        ),
        teoria(
            "SCD2 na prática",
            "SCD2 mantém o histórico: a dimensão ganha colunas `valid_from`, `valid_to`, "
            "`is_current`. Cada mudança de atributo gera uma nova versão da linha.\n\n"
            "O Databricks padroniza com **`APPLY CHANGES INTO`** (dentro do DLT):\n\n"
            "```python\n@dlt.table\ndef dim_cliente_scd2():\n"
            "    return (\n"
            "        dlt.apply_changes(\n"
            "            target='dim_cliente_scd2',\n"
            "            source='stg_clientes',\n"
            "            keys=['CustomerID'],\n"
            "            sequence_by='updated_at',\n"
            "            apply_as_append=False,\n"
            "            except_column_list=['CustomerID'],\n"
            "            stored_as_scd_type=2))\n"
            "```",
        ),
        teoria(
            "SCD1 vs SCD2 no APPLY CHANGES",
            "| Parâmetro | SCD1 | SCD2 |\n|---|---|---|\n"
            "| `stored_as_scd_type` | `1` | `2` |\n"
            "| `apply_as_append` | `True` (sobrescreve) | `False` (gera versões) |\n"
            "| Resultado | valor atual | histórico completo |",
        ),
        pratica("Simulando SCD2 fora do DLT",
            "Como o DLT roda em pipeline, vamos demonstrar o mesmo padrão com PySpark "
            "(mudança de cidade) para ver o mecanismo."),
        code('# Staging: cliente 12345 mudou de cidade\n'
             'stg = spark.createDataFrame([\n'
             '    ("12345", "Ana", "CAMPINAS", "2024-06-01"),\n'
             '    ("99999", "Maria", "BH", "2024-06-01"),\n'
             '], ["CustomerID", "nome", "cidade", "updated_at"])\n'
             'stg.createOrReplaceTempView("stg_clientes")\n'
             'print("Staging com 1 update + 1 insert")'),
        code('# Dimensão SCD2 inicial (na vida real, criada por APPLY CHANGES)\n'
             'spark.sql("""\n'
             'CREATE OR REPLACE TABLE workspace.prata.dim_cliente_scd2_demo (\n'
             '  CustomerID STRING, nome STRING, cidade STRING,\n'
             '  valid_from DATE, valid_to DATE, is_current BOOLEAN) USING DELTA\n'
             '""")\n'
             'spark.sql("""INSERT INTO workspace.prata.dim_cliente_scd2_demo VALUES\n'
             '  (\'12345\', \'Ana\', \'SP\', \'2024-01-01\', NULL, true),\n'
             '  (\'67890\', \'João\', \'RJ\', \'2024-01-01\', NULL, true)\n'
             '""")\n'
             'print("Dimensão inicial criada.")'),
        code('# Aplicar a mudança (SCD2 manual — o mesmo efeito do APPLY CHANGES)\n'
             'from pyspark.sql.functions import current_date, lit, to_date\n'
             'atuais = spark.table("workspace.prata.dim_cliente_scd2_demo")\n'
             '# Fechar a linha atual e abrir a nova versão\n'
             'spark.sql("UPDATE workspace.prata.dim_cliente_scd2_demo SET valid_to = \'2024-06-01\', is_current = false WHERE CustomerID = \'12345\'")\n'
             'stg.select("CustomerID", "nome", "cidade",\n'
             '           to_date("updated_at").alias("valid_from"))\\\n'
             '    .withColumn("valid_to", lit(None).cast("date"))\\\n'
             '    .withColumn("is_current", lit(True))\\\n'
             '    .write.mode("append").saveAsTable("workspace.prata.dim_cliente_scd2_demo")\n'
             'display(spark.sql("SELECT * FROM workspace.prata.dim_cliente_scd2_demo ORDER BY CustomerID, valid_from"))'),
        pratica("APPLY CHANGES no DLT (o padrão oficial)",
            "Dentro de um pipeline DLT (arquivo `.py`), cole o exemplo da teoria e rode — "
            "em produção é assim que SCD2 é mantido."),
        code('# ===== workspace_file: pipeline_scd.py =====\n'
             'import dlt\n'
             'from pyspark.sql.functions import col, to_date\n'
             '\n'
             '@dlt.table\n'
             'def stg_clientes():\n'
             '    return (spark.readStream\n'
             '        .format("cloudFiles")\n'
             '        .option("cloudFiles.format", "csv")\n'
             '        .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/vol_checkpoints/schema_scd")\n'
             '        .load("/Volumes/workspace/bronze/vol_landing"))\n'
             '\n'
             '@dlt.table\n'
             '@dlt.expect_all_or_drop({"cliente_chave": "CustomerID IS NOT NULL"})\n'
             'def dim_cliente_scd2():\n'
             '    return (dlt.apply_changes(\n'
             '        target="dim_cliente_scd2",\n'
             '        source="stg_clientes",\n'
             '        keys=["CustomerID"],\n'
             '        sequence_by="updated_at",\n'
             '        apply_as_append=False,\n'
             '        except_column_list=["CustomerID"],\n'
             '        stored_as_scd_type=2))\n'
             'print("Arquivo de pipeline SCD2 (cole no Workspace e rode no DLT).")'),
        dica_prova("DEP: `APPLY CHANGES INTO` com `stored_as_scd_type=2` e "
                   "`sequence_by` é o padrão para SCD2. Pergunta típica: qual função DLT "
                   "para SCD2? → apply_changes. SCD1 = stored_as_scd_type 1."),
        exercicios([
            "Explique o papel de sequence_by no apply_changes.",
            "O que muda em apply_as_append entre SCD1 e SCD2?",
            "Crie o SCD1 para a dim_produto (correção de descrição).",
        ]),
        gabarito([
            ("sequence_by",
             "Define a ordem temporal dos eventos (ex.: updated_at) — o DLT usa para "
             "decidir qual mudança é a mais recente e fechar versões na ordem certa."),
            ("apply_as_append",
             "SCD1: True (a mudança sobrescreve o valor atual, sem novas linhas). SCD2: "
             "False (gera novas linhas de versão, mantendo histórico)."),
            ("SCD1 dim_produto",
             "`apply_changes(target='dim_produto', source='stg_produtos', keys=['StockCode'], "
             "sequence_by='updated_at', apply_as_append=True, stored_as_scd_type=1)` — "
             "a descrição é sobrescrita."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana8_dia5_dlt_avancado_triggered_continuous",
    [
        header(
            "8", "5", "DLT avançado: triggered vs continuous e expectations profundas",
            "Aprofundar o Lakeflow: modos de execução (triggered/continuous), streaming "
            "tables em produção e expectations avançadas.",
            "DEP (DLT)", "Pipeline avançado com expectations profundas",
            "✅ Free Edition (triggered) + 🔑 contínuo (trial)",
        ),
        teoria(
            "Triggered vs Continuous no DLT",
            "| Modo | Comportamento | Uso |\n|---|---|---|\n"
            "| **Triggered** | processa o delta disponível e para | padrão; custo controlado |\n"
            "| **Continuous** | processa em streaming contínuo (latência baixa) | dados em tempo real; mais custo |\n\n"
            "Na Free Edition, o pipeline é **triggered** (1 ativo por tipo). O modo "
            "continuous é recurso de conta completa (trial para validar).",
        ),
        teoria(
            "Expectations avançadas",
            "Além dos 3 níveis, o DLT permite:\n"
            "- `@dlt.expect_all({...})` — várias expectations, mantém tudo\n"
            "- `@dlt.expect_all_or_drop({...})` — descarta violadas\n"
            "- `@dlt.expect_all_or_fail({...})` — falha em qualquer violação\n"
            "- Combinar com funções: `col('receita') > 0`, `isin(...)`, `regexp`",
        ),
        pratica("Expectations combinadas",
            "Aplique expect_all_or_drop com várias regras numa tabela."),
        code('# ===== workspace_file: pipeline_vendas_avancado.py =====\n'
             'import dlt\n'
             'from pyspark.sql.functions import col\n'
             '\n'
             '@dlt.table(comment="Prata com expectations combinadas")\n'
             '@dlt.expect_all_or_drop({\n'
             '    "qtd_positiva": "Quantity > 0",\n'
             '    "preco_positivo": "UnitPrice > 0",\n'
             '    "cliente_existe": "CustomerID IS NOT NULL",\n'
             '    "pais_valido": "UPPER(Country) IN (\'UNITED KINGDOM\', \'BRAZIL\', \'GERMANY\', \'FRANCE\')"})\n'
             'def vendas_prata():\n'
             '    return (dlt.read_stream("vendas_bronze"))\n'
             '\n'
             '@dlt.table(comment="Ouro: receita diária com expect_or_fail (KPI crítico)")\n'
             '@dlt.expect_or_fail("receita_nao_negativa", "receita >= 0")\n'
             'def receita_diaria():\n'
             '    return (dlt.read("vendas_prata")\n'
             '        .withColumn("receita", col("Quantity") * col("UnitPrice"))\n'
             '        .groupBy("data_venda")\n'
             '        .sum("receita"))'),
        pratica("Modo triggered na Free",
            "Na UI do pipeline: **Triggered** (processa o que há e para). Rode e veja as "
            "métricas de qualidade. Para validar **continuous**, use o trial pago."),
        code('# Rodando no modo triggered (UI) — observação das métricas\n'
             'print("""\n'
             '1. Pipeline > Settings > Triggered\n'
             '2. Start\n'
             '3. Aba Quality: veja violações por expectation\n'
             '4. Tabelas: vendas_prata (drop de violadas), receita_diaria (fail em receita < 0)\n'
             '""")\n'
             'print("Na Free, 1 pipeline ativo por tipo — pare ao terminar.")'),
        dica_prova("DEP: triggered (delta + para) vs continuous (streaming contínuo) e as "
                   "funções expect_all*. Pergunta típica: 'qual expectation mantém linhas "
                   "e só monitora?' → expect_all."),
        exercicios([
            "Quando usar continuous em vez de triggered?",
            "Escreva expect_all_or_fail com 3 regras de negócio do seu projeto.",
            "Por que o Ouro usa expect_or_fail para KPI crítico?",
        ]),
        gabarito([
            ("Continuous",
             "Quando a latência importa (decisões em tempo real) e o custo é aceitável. "
             "Para lotes diários, triggered é suficiente e mais barato."),
            ("Expect_all_or_fail",
             '```python\n@dlt.expect_all_or_fail({"qtd>0": "Quantity > 0", "preco>0": "UnitPrice > 0", "cliente": "CustomerID IS NOT NULL"})\n```'),
            ("Fail no KPI",
             "Um KPI errado propaga erro para BI e modelos — melhor parar o pipeline e "
             "alertar do que publicar número errado."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana8_dia6_entregavel_scd2_cdc_tuning_simulado",
    [
        header(
            "8", "6", "Entregável: SCD2 + CDC + tuning + simulado DEP",
            "Fechar a Semana 8: pipeline com SCD2, CDC e tuning aplicados, e um simulado "
            "parcial DEP.",
            "DEP (simulado)", "SCD2 + CDC + benchmark + simulado ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "O que você agora sabe fazer",
            "- Tuning: plano físico, broadcast, AQE, cache (10x)\n"
            "- Organização física: Liquid Clustering vs particionamento\n"
            "- CDC: Change Data Feed (ler mudanças)\n"
            "- SCD1/SCD2: APPLY CHANGES INTO\n"
            "- DLT avançado: triggered/continuous + expectations combinadas\n\n"
            "Esse é o núcleo da **Data Engineer Professional**.",
        ),
        pratica("Entregável integrado",
            "Monte o pipeline completo: Bronze (CDF on) → Prata SCD2 → Ouro com tuning."),
        code('# Passo 1: garantir CDF no Bronze (para CDC)\n'
             'spark.sql("ALTER TABLE workspace.bronze.vendas_bronze SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")\n'
             'print("CDF habilitado no Bronze.")'),
        code('# Passo 2: benchmark antes do tuning\n'
             'import time\n'
             't0 = time.time()\n'
             'r = spark.sql("""\n'
             '  SELECT Country, DATE_TRUNC(\'month\', InvoiceDate) mes, SUM(Quantity*UnitPrice) receita\n'
             '  FROM workspace.bronze.vendas_bronze GROUP BY 1, 2\n'
             '""").count()\n'
             't1 = time.time()\n'
             'print(f"Antes do tuning: {t1-t0:.2f}s ({r} linhas)")'),
        code('# Passo 3: aplicar tuning (broadcast em dimensão pequena)\n'
             'dim = spark.table("workspace.prata.dim_produto").limit(5)\n'
             't0 = time.time()\n'
             'r2 = (spark.table("workspace.prata.fato_vendas")\n'
             '    .join(dim.hint("broadcast"), "sk_produto", "left")\n'
             '    .groupBy("Country").count().count())\n'
             't1 = time.time()\n'
             'print(f"Com broadcast: {t1-t0:.2f}s")'),
        pratica("Simulado DEP parcial (10 questões)",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** O AQE pode:
- A) transformar sort-merge em broadcast em runtime  B) apagar dados
- C) criar tabelas  D) nada

**2.** Para leitura eficiente por país+data em tabela de 5 TB:
- A) particionar por país  B) Liquid Clustering (Country, data)  C) Z-ORDER só  D) nada

**3.** `_change_type='delete'` aparece ao ler com:
- A) readChangeFeed=true  B) readStream normal  C) select simples  D) count

**4.** SCD2 com histórico é feito com:
- A) MERGE simples  B) apply_changes (stored_as_scd_type=2)  C) UPDATE  D) INSERT OVERWRITE

**5.** `sequence_by` no apply_changes define:
- A) ordem das colunas  B) ordem temporal dos eventos  C) tamanho da tabela  D) nada

**6.** Continuous vs Triggered: Continuous é:
- A) mais barato  B) streaming contínuo (baixa latência)  C) batch único  D) igual

**7.** `expect_all_or_drop`:
- A) mantém e conta  B) descarta violadas  C) falha pipeline  D) remove a tabela

**8.** Para propagar mudanças do Delta a outro sistema:
- A) CDF  B) cache  C) broadcast  D) VACUUM

**9.** VACUUM com retenção padrão (7d):
- A) apaga tudo  B) remove arquivos fora da retenção  C) nunca roda  D) destrói o log

**10.** Spark UI mostra:
- A) DAG, estágios, tasks  B) apenas erros  C) nada  D) somente SQL
"""),
        teoria(
            "Gabarito",
            "**1-A** · **2-B** · **3-A** · **4-B** · **5-B** · **6-B** · **7-B** · "
            "**8-A** · **9-B** · **10-A**. ≥ 7/10 = pronto para a Semana 9.",
        ),
        dica_prova("DEP é a prova de 'para que serve X'. Ao responder, pergunte-se: o que "
                   "essa ferramenta RESOLVE? (CDF=propagar mudança, AQE=otimizar runtime, "
                   "CLUSTER BY=pruning em cardinalidade alta)."),
        exercicios([
            "Documente o benchmark antes/depois do seu tuning no README.",
            "Explique o fluxo Bronze(CDF) → Prata(SCD2) → Ouro em 4 frases.",
        ]),
        gabarito([
            ("Benchmark",
             "Anote tempo, nº de arquivos e a técnica (broadcast/cache/cluster). É a prova "
             "de impacto para entrevistas."),
            ("Fluxo",
             "Bronze captura mudanças (CDF); Prata mantém dimensões SCD2 (histórico); Ouro "
             "agrega para BI; o DLT orquestra tudo com expectations e triggered."),
        ]),
        footer([
            "Apliquei broadcast/AQE/cache e documentei o benchmark.",
            "Habilitei CDF e li mudanças.",
            "Implementei SCD2 (demo + APPLY CHANGES).",
            "Fiz o simulado DEP parcial e revisei erros.",
        ]),
    ],
))
