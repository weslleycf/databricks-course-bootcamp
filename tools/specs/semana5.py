"""Semana 5 — Ingestão, Streaming e Lakeflow (DLT + Jobs) (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana5_dia1_auto_loader_ingestao_incremental",
    [
        header(
            "5", "1", "Auto Loader: ingestão incremental",
            "Dominar o Auto Loader — o padrão para ingerir arquivos novos em pastas com "
            "exactly-once e schema inference/evolution.",
            "DEA, DEP (ingestão)", "Pipeline Auto Loader rodando com arquivos novos",
            "✅ Free Edition",
        ),
        teoria(
            "O problema da ingestão",
            "Arquivos novos chegam o tempo todo (vendas diárias, logs). Reler tudo a cada vez é "
            "caro; perder arquivos é inaceitável.\n\n"
            "**Auto Loader** (padrão Databricks para ingestão) monitora uma pasta e processa "
            "**somente arquivos novos**, com garantia **exactly-once** (checkpoint guarda o "
            "que já foi processado).",
        ),
        teoria(
            "Como funciona",
            "1. Você aponta para um diretório (`/Volumes/.../landing`).\n"
            "2. O Auto Loader registra cada arquivo novo (via listagem ou notificação de "
            "arquivo — na Free, listagem).\n"
            "3. Opções: `cloudFiles.format`, `cloudFiles.schemaLocation` (checkpoint de "
            "schema), `cloudFiles.inferColumnTypes`.\n\n"
            "```python\n(spark.readStream\n"
            "    .format('cloudFiles')\n"
            "    .option('cloudFiles.format', 'csv')\n"
            "    .option('cloudFiles.schemaLocation', '/Volumes/.../checkpoints')\n"
            "    .load('/Volumes/.../landing'))\n```",
        ),
        pratica("Preparando a área de landing",
            "Crie a pasta de arquivos e um volume de trabalho."),
        code('# Área de staging\n'
             'spark.sql("CREATE VOLUME IF NOT EXISTS workspace.bronze.vol_landing")\n'
             'spark.sql("CREATE VOLUME IF NOT EXISTS workspace.bronze.vol_checkpoints")\n'
             'print("Volumes de landing e checkpoints prontos")'),
        code('# Copiar uma amostra do dataset para o landing\n'
             'import shutil\n'
             'amostra = spark.table("workspace.bronze.vendas_bronze").limit(2000)\n'
             'amostra.write.mode("overwrite").option("header", True).csv("/Volumes/workspace/bronze/vol_landing/vendas")\n'
             'print("2.000 linhas gravadas como CSV no landing")'),
        pratica("Auto Loader na prática",
            "Leia incrementalmente os arquivos novos do landing."),
        code('# Leitura incremental com Auto Loader\n'
             'df_stream = (spark.readStream\n'
             '    .format("cloudFiles")\n'
             '    .option("cloudFiles.format", "csv")\n'
             '    .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/vol_checkpoints/schema_landing")\n'
             '    .option("header", True)\n'
             '    .option("inferColumnTypes", True)\n'
             '    .load("/Volumes/workspace/bronze/vol_landing"))\n'
             'print("Stream configurado (lazy). Tipo:", type(df_stream).__name__)'),
        code('# Gravar incrementalmente (append) com checkpoint\n'
             'query = (df_stream.writeStream\n'
             '    .format("delta")\n'
             '    .option("checkpointLocation", "/Volumes/workspace/bronze/vol_checkpoints/ckpt_landing")\n'
             '    .outputMode("append")\n'
             '    .trigger(once=True)   # roda uma vez, processa o que há\n'
             '    .table("workspace.bronze.vendas_landing"))\n'
             'query.awaitTermination()\n'
             'print("Ingestão concluída:", spark.table("workspace.bronze.vendas_landing").count(), "linhas")'),
        pratica("Novos arquivos",
            "Adicione mais dados e rode de novo — só o que é novo entra (exactly-once)."),
        code('# Adicionar mais 1000 linhas novas ao landing\n'
             'extra = spark.table("workspace.bronze.vendas_bronze").limit(1000)\n'
             'extra.write.mode("append").option("header", True).csv("/Volumes/workspace/bronze/vol_landing/vendas_extra")\n'
             'print("Mais 1.000 linhas no landing")'),
        code('# Rodar a ingestão de novo — só processa o que é novo\n'
             'q2 = (spark.readStream\n'
             '    .format("cloudFiles")\n'
             '    .option("cloudFiles.format", "csv")\n'
             '    .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/vol_checkpoints/schema_landing")\n'
             '    .option("header", True)\n'
             '    .load("/Volumes/workspace/bronze/vol_landing")\n'
             '    .writeStream\n'
             '    .format("delta")\n'
             '    .option("checkpointLocation", "/Volumes/workspace/bronze/vol_checkpoints/ckpt_landing")\n'
             '    .outputMode("append")\n'
             '    .trigger(once=True)\n'
             '    .table("workspace.bronze.vendas_landing"))\n'
             'q2.awaitTermination()\n'
             'print("Agora total:", spark.table("workspace.bronze.vendas_landing").count(), "linhas (2000 + 1000 novas)")'),
        dica_prova("Auto Loader cai na DEA e DEP: `cloudFiles.format`, `schemaLocation`, "
                   "exactly-once via checkpoint. Pergunta típica: 'qual opção para processar "
                   "somente arquivos novos?' → Auto Loader."),
        exercicios([
            "Por que o Auto Loader é melhor que reler a pasta inteira?",
            "O que `cloudFiles.schemaLocation` guarda?",
            "Adicione um terceiro arquivo e verifique se o total continua correto.",
        ]),
        gabarito([
            ("Incremental",
             "Processa só o delta (arquivos novos), com checkpoint — economiza custo e tempo, "
             "com garantia exactly-once."),
            ("schemaLocation",
             "O checkpoint de schema: onde o Auto Loader persiste o schema inferido e a "
             "evolução — necessário para idempotência."),
            ("Terceiro arquivo",
             "Total = 2000 + 1000 + novos; rode o stream mais uma vez e confira o count."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana5_dia2_structured_streaming_batch_vs_stream",
    [
        header(
            "5", "2", "Structured Streaming: batch vs streaming",
            "Entender o modelo de streaming estruturado do Spark: readStream/writeStream, "
            "triggers, watermarks e checkpointing.",
            "DEA, DEP (streaming)", "Streaming simples rodando com watermark",
            "✅ Free Edition",
        ),
        teoria(
            "Batch vs Streaming",
            "**Batch**: processa um lote de dados já completo (ex.: diário).\n"
            "**Streaming**: processa dados que chegam continuamente (ex.: eventos em tempo "
            "real), em micro-batches.\n\n"
            "O **Structured Streaming** do Spark usa a **mesma API de DataFrame** — a diferença "
            "é `readStream`/`writeStream` + checkpoint.",
        ),
        teoria(
            "Conceitos-chave",
            "- **trigger**: quando o micro-batch roda (`once`, `processingTime`, `continuous`)\n"
            "- **watermark**: tolerância para dados atrasados (ex.: `watermark('ts', '1 hour')`)\n"
            "- **checkpointLocation**: onde o estado é persistido — sem isso, o stream não "
            "recupera após falha\n"
            "- **outputMode**: `append` (novas linhas), `update` (linhas atualizadas), "
            "`complete` (agregações totais)",
        ),
        pratica("Streaming simples",
            "Leia o landing como stream e escreva em Delta com checkpoint."),
        code('# Ler o CSV como stream\n'
             'stream = (spark.readStream\n'
             '    .format("cloudFiles")\n'
             '    .option("cloudFiles.format", "csv")\n'
             '    .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/vol_checkpoints/schema_stream")\n'
             '    .option("header", True)\n'
             '    .load("/Volumes/workspace/bronze/vol_landing"))\n'
             'print("Stream criado (lazy).")'),
        code('# Escrever com trigger once (para estudo)\n'
             '(stream.writeStream\n'
             '    .format("delta")\n'
             '    .option("checkpointLocation", "/Volumes/workspace/bronze/vol_checkpoints/ckpt_stream")\n'
             '    .outputMode("append")\n'
             '    .trigger(once=True)\n'
             '    .table("workspace.bronze.vendas_stream"))\n'
             'print("Streaming batch-único executado.")'),
        pratica("Watermark e agregações em stream",
            "Streaming com agregação por janela de tempo."),
        code('# Agregação com janela temporal + watermark\n'
             'from pyspark.sql.functions import window, sum as s, to_timestamp\n'
             'df = (spark.readStream\n'
             '    .format("cloudFiles")\n'
             '    .option("cloudFiles.format", "csv")\n'
             '    .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/vol_checkpoints/schema_win")\n'
             '    .option("header", True)\n'
             '    .load("/Volumes/workspace/bronze/vol_landing")\n'
             '    .withColumn("ts", to_timestamp("InvoiceDate", "M/d/yyyy H:mm"))\n'
             '    .withWatermark("ts", "1 hour")\n'
             '    .groupBy(window("ts", "1 day"), "Country")\n'
             '    .agg(s("Quantity").alias("qtd")))\n'
             'print("Stream com janela diária e watermark de 1h configurado.")'),
        code('# Escrever o resultado (append)\n'
             'q = (df.writeStream\n'
             '    .format("delta")\n'
             '    .option("checkpointLocation", "/Volumes/workspace/bronze/vol_checkpoints/ckpt_win")\n'
             '    .outputMode("append")\n'
             '    .trigger(once=True)\n'
             '    .table("workspace.bronze.vendas_janela"))\n'
             'q.awaitTermination()\n'
             'print("Agregação em stream concluída.")'),
        dica_prova("Watermark + janela é pergunta clássica de streaming (DEP). Memorize: "
                   "watermark define o atraso tolerado; janela agrupa por tempo."),
        exercicios([
            "Explique a diferença entre trigger(once=True) e processingTime.",
            "O que acontece sem checkpointLocation?",
            "Qual outputMode usar para agregação com atualizações?",
        ]),
        gabarito([
            ("Triggers",
             "once: processa tudo que chegou e para (batch incremental). processingTime: roda "
             "a cada N segundos continuamente (stream de verdade)."),
            ("Sem checkpoint",
             "O stream não consegue recuperar estado após falha — pode reprocessar (perde "
             "exactly-once) ou falhar ao reiniciar."),
            ("OutputMode",
             "`update` — emite somente linhas que mudaram; ideal para agregações com "
             "atualização contínua. `append` não permite atualização."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana5_dia3_dlt_lakeflow_pipelines",
    [
        header(
            "5", "3", "Lakeflow pipelines (Delta Live Tables)",
            "Sair de notebooks manuais para pipelines declarativos com Delta Live Tables "
            "(DLT) — o padrão oficial de produção do Databricks.",
            "DEA, DEP (Lakeflow)", "Pipeline DLT Bronze→Prata rodando",
            "✅ Free Edition",
        ),
        teoria(
            "O que é o Lakeflow (DLT)",
            "**Delta Live Tables (DLT)** é o framework declarativo do Databricks para "
            "pipelines: você declara **o que** cada tabela deve ser, e o DLT gerencia "
            "dependências, ordenação, qualidade e retry.\n\n"
            "Na Free Edition: **1 pipeline ativo por tipo** (crie e rode; pare antes de criar "
            "outro).\n\n"
            "Sintaxe: decorators `@dlt.table`, `@dlt.view`, `@dlt.expect` (e `@dlt.streaming_table`).",
        ),
        teoria(
            "Materialized vs Streaming tables",
            "**Materialized table (MT)**: calculada como batch, recalculada sob demanda — "
            "refrescada de acordo com as dependências.\n"
            "**Streaming table (ST)**: alimentada por stream contínuo (Auto Loader) com "
            "incrementos.\n\n"
            "Em produção, usa-se ST para ingestão (Bronze) e MT para transformações "
            "(Prata/Ouro) — o DLT orquestra tudo.",
        ),
        pratica("Pipeline DLT em arquivo",
            "Crie o arquivo de pipeline como *workspace file* e rode via UI. Células abaixo "
            "são o conteúdo do arquivo — cole num arquivo `.py` no Workspace."),
        code('# ===== workspace_file: pipeline_vendas.py =====\n'
             'import dlt\n'
             'from pyspark.sql.functions import col, to_date, sum as s\n'
             '\n'
             '@dlt.table(comment="Bronze: vendas via Auto Loader")\n'
             'def vendas_bronze():\n'
             '    return (spark.readStream\n'
             '        .format("cloudFiles")\n'
             '        .option("cloudFiles.format", "csv")\n'
             '        .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/vol_checkpoints/schema_pipeline")\n'
             '        .option("header", True)\n'
             '        .load("/Volumes/workspace/bronze/vol_landing"))\n'
             '\n'
             '@dlt.table(comment="Prata: limpo e tipado")\n'
             'def vendas_prata():\n'
             '    return (dlt.read_stream("vendas_bronze")\n'
             '        .filter(col("Quantity") > 0)\n'
             '        .withColumn("data_venda", to_date("InvoiceDate", "M/d/yyyy H:mm")))\n'
             '\n'
             '@dlt.table(comment="Ouro: receita por dia")\n'
             'def receita_diaria():\n'
             '    return (dlt.read("vendas_prata")\n'
             '        .groupBy("data_venda")\n'
             '        .agg(s(col("Quantity") * col("UnitPrice")).alias("receita")))'),
        pratica("Rodando o pipeline",
            "1. Em **Workflows → Pipelines → Create Pipeline**.\n"
            "2. Nome: `pipeline_vendas`. Selecione o arquivo acima como código-fonte.\n"
            "3. Target schema: `workspace.bronze` (ou um schema próprio).\n"
            "4. **Start**. O DLT cria as tabelas e mostra o DAG de dependências.\n"
            "5. Na Free Edition, pare o pipeline ao terminar (limite de 1 ativo).",
        ),
        code('# Conferir o resultado após rodar o pipeline\n'
             'spark.sql("SHOW TABLES IN workspace.bronze")\n'
             'display(spark.sql("SELECT * FROM workspace.bronze.receita_diaria LIMIT 10"))'),
        dica_prova("DLT cai forte na DEA/DEP 2026 (nomenclatura: **Lakeflow pipelines**). "
                   "Decore: `@dlt.table`, `@dlt.view`, `@dlt.expect`, `dlt.read` vs "
                   "`dlt.read_stream`, e os 3 níveis de expectations (próximo dia)."),
        exercicios([
            "Qual a diferença entre dlt.read e dlt.read_stream?",
            "Por que o DLT é declarativo e o notebook é imperativo?",
            "Crie uma tabela DLT extra que compute top 10 produtos por dia.",
        ]),
        gabarito([
            ("read vs read_stream",
             "`dlt.read` lê a versão materializada (batch) de outra tabela; `dlt.read_stream` "
             "lê como stream contínuo — usado em streaming tables."),
            ("Declarativo vs imperativo",
             "No DLT você declara o RESULTADO (o que é a tabela); o DLT decide ordem, "
             "incrementos, retry e qualidade. No notebook você dita o COMO passo a passo."),
            ("Top 10",
             "```python\n@dlt.table\ndef top10_dia():\n    return (dlt.read('vendas_prata')\n        .groupBy('data_venda','StockCode')\n        .agg(s(col('Quantity')).alias('qtd'))\n        .orderBy('data_venda', col('qtd').desc()))\n```"),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana5_dia4_dlt_expectations_qualidade",
    [
        header(
            "5", "4", "DLT Expectations: qualidade contínua",
            "Aplicar os 3 níveis de expectations do DLT (expect, expect_or_drop, "
            "expect_or_fail) para garantir qualidade dentro do pipeline.",
            "DEA (qualidade de dados)", "Expectations aplicadas no pipeline",
            "✅ Free Edition",
        ),
        teoria(
            "Expectations — qualidade como código",
            "No DLT, qualidade é **declarada** junto com a tabela, com 3 níveis de severidade:\n\n"
            "| Nível | Comportamento | Uso |\n|---|---|---|\n"
            "| `@dlt.expect` | conta violações e **mantém** as linhas ruins | monitorar sem bloquear |\n"
            "| `@dlt.expect_or_drop` | **descarta** as linhas violadas | limpeza silenciosa |\n"
            "| `@dlt.expect_or_fail` | **falha o pipeline** se violar | regra de negócio crítica |\n\n"
            "As violações viram **métricas de qualidade** na UI do pipeline (dashboard de "
            "expectations) — auditoria automática.",
        ),
        pratica("Expectations na prática",
            "Adicione expectations ao pipeline da tabela Prata."),
        code('# ===== workspace_file: pipeline_vendas_qualidade.py =====\n'
             'import dlt\n'
             'from pyspark.sql.functions import col\n'
             '\n'
             '@dlt.table(comment="Prata com qualidade")\n'
             '@dlt.expect("quantidade_positiva", "Quantity > 0")\n'
             '@dlt.expect_or_drop("preco_positivo", "UnitPrice > 0")\n'
             '@dlt.expect_or_fail("cliente_obrigatorio", "CustomerID IS NOT NULL")\n'
             'def vendas_prata():\n'
             '    return (dlt.read_stream("vendas_bronze")\n'
             '        .filter(col("Quantity") > 0))\n'
             '\n'
             '@dlt.table(comment="Métricas de qualidade")\n'
             'def qualidade_vendas():\n'
             '    return (dlt.read("vendas_prata")\n'
             '        .groupBy("Country")\n'
             '        .count())'),
        pratica("Rodando e observando",
            "1. Atualize o pipeline `pipeline_vendas` para apontar para o novo arquivo.\n"
            "2. **Start** e aguarde.\n"
            "3. Na aba **Quality**, veja as métricas: linhas violadas por expectation "
            "(contadas, dropadas, falhas).",
        ),
        code('# Conferir as tabelas geradas\n'
             'spark.sql("SHOW TABLES IN workspace.bronze")\n'
             'display(spark.sql("SELECT COUNT(*) AS total, COUNT(DISTINCT InvoiceNo) AS notas FROM workspace.bronze.vendas_prata"))'),
        dica_prova("Os 3 níveis de expectations são pergunta garantida (DEA). Memorize: "
                   "expect (conta+mantém), expect_or_drop (descarta), expect_or_fail "
                   "(falha o pipeline)."),
        exercicios([
            "Qual expectation usar para: (a) bloquear pipeline se preço negativo? (b) monitorar "
            "sem bloquear? (c) descartar linhas com e-mail inválido?",
            "Onde as métricas de qualidade aparecem na UI?",
        ]),
        gabarito([
            ("Níveis",
             "(a) expect_or_fail; (b) expect; (c) expect_or_drop."),
            ("UI",
             "Na aba **Quality** do pipeline (e nas métricas de dados do Unity Catalog)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana5_dia5_lakeflow_jobs_orquestracao",
    [
        header(
            "5", "5", "Lakeflow Jobs: orquestração e agendamento",
            "Orquestrar notebooks, pipelines DLT e tarefas com dependências, retries e "
            "alertas usando o Lakeflow Jobs (sucessor do Workflows).",
            "DEA, DEP (orquestração)", "Job agendado com 2 tarefas + dependência",
            "✅ Free Edition",
        ),
        teoria(
            "Lakeflow Jobs (2026)",
            "O **Lakeflow Jobs** é o orquestrador do Databricks: roda notebooks, pipelines "
            "DLT, queries SQL e código arbitrário em sequência ou paralelo, com "
            "**dependências**, **retries**, **alertas** e **agendamento**.\n\n"
            "Na Free Edition: **máx. 5 tarefas/jobs concorrentes** por conta.\n\n"
            "Terminologia 2026: *Workflows* → **Lakeflow Jobs** (mesma API/UI, nome novo).",
        ),
        teoria(
            "Componentes de um Job",
            "- **Task**: uma unidade (notebook, pipeline, SQL query, Python wheel, ...)\n"
            "- **Dependência**: task B roda após task A (via parâmetros de entrada/saída)\n"
            "- **Trigger**: agendamento (cron) ou manual\n"
            "- **Retry**: tentativas em falha\n"
            "- **Alert**: notificação por e-mail/Slack\n"
            "- **Run**: uma execução (com log, status, duração)",
        ),
        pratica("Criando o Job",
            "1. Em **Workflows → Jobs → Create Job**.\n"
            "2. Task 1: notebook `Semana 5 · Auto Loader` (ou o notebook deste curso).\n"
            "3. Task 2: **Delta Live Tables pipeline** `pipeline_vendas`.\n"
            "4. Task 3: query SQL que valida contagem (ex.: `SELECT COUNT(*) FROM workspace.bronze.vendas_prata`).\n"
            "5. Configure dependência: Task 2 depende de Task 1; Task 3 depende de Task 2.\n"
            "6. Schedule: diário às 06:00. Alert: e-mail em falha.",
        ),
        code('# Jobs via API (visão geral — a execução real é na UI)\n'
             'import json\n'
             'job_def = {\n'
             '  "name": "job_pipeline_vendas",\n'
             '  "tasks": [\n'
             '    {"task_key": "t1_ingestao", "notebook_task": {"notebook_path": "/Workspace/.../semana5_dia1"}, "existing_cluster_id": ""},\n'
             '    {"task_key": "t2_pipeline", "depends_on": [{"task_key": "t1_ingestao"}],\n'
             '     "pipeline_task": {"pipeline_id": "REPLACE_COM_ID_DO_PIPELINE"}},\n'
             '    {"task_key": "t3_validacao", "depends_on": [{"task_key": "t2_pipeline"}],\n'
             '     "sql_task": {"query": {"query_text": "SELECT COUNT(*) FROM workspace.bronze.vendas_prata"}}}\n'
             '  ]\n'
             '}\n'
             'print(json.dumps(job_def, indent=2, ensure_ascii=False))'),
        code('# Como consultar os jobs via API (na UI ou CLI)\n'
             '# !databricks jobs list  (CLI)\n'
             'print("Na UI: Jobs > veja o job, runs, logs e retries.")'),
        dica_prova("Terminologia 2026: **Lakeflow Jobs**. A prova pergunta sobre "
                   "dependências entre tasks, retry e triggers. Lembre: dependências são "
                   "declaradas com depends_on."),
        exercicios([
            "Crie um job com 3 tasks e dependência encadeada.",
            "Qual a diferença entre trigger por agendamento e trigger manual?",
            "Onde você vê o log e o status de uma execução (run)?",
        ]),
        gabarito([
            ("Job 3 tasks",
             "UI: Create Job → adicionar tasks → em cada task, 'Depends on' a anterior. "
             "Alternativa: API com depends_on."),
            ("Triggers",
             "Agendamento: roda em horário (cron) automaticamente. Manual: dispara quando "
             "você clica 'Run now'. Também há trigger contínuo para streams."),
            ("Runs",
             "Na aba **Runs** do job: status (PENDING/RUNNING/SUCCESS/FAILED), duração, log "
             "de cada task (Link to logs)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana5_dia6_pipeline_completo_dlt_job",
    [
        header(
            "5", "6", "Entregável da semana: pipeline DLT + Job completo",
            "Unir Auto Loader + DLT + Jobs em um pipeline de ponta a ponta e validar "
            "o ciclo completo de ingestão → transformação → validação.",
            "DEA, DEP", "Pipeline completo rodando de ponta a ponta",
            "✅ Free Edition",
        ),
        teoria(
            "A arquitetura final da Semana 5",
            "```\nlanding (CSV) --AutoLoader--> Bronze --DLT--> Prata --DLT--> Ouro\n                       (stream)      (streaming)   (materialized)\n                                  |\n                           Lakeflow Job (diário)\n                                  |\n                           validação (query SQL)\n```\n"
            "Tudo orquestrado por um Job com dependências — reproduzível e auditável.",
        ),
        pratica("Pipeline de ponta a ponta",
            "1. Garanta que o `pipeline_vendas` (arquivo `pipeline_vendas_qualidade.py`) está "
            "correto e rode-o.\n"
            "2. Confira as tabelas criadas.\n"
            "3. Crie o Job com as 3 tasks (ingestão → pipeline → validação) e rode manualmente.\n"
            "4. Verifique os runs e as métricas de qualidade.",
        ),
        code('# 1) Confirmar tabelas do pipeline\n'
             'spark.sql("SHOW TABLES IN workspace.bronze")\n'
             'print("Pipeline: bronze/prata/ouro devem aparecer")'),
        code('# 2) Validar as camadas\n'
             'print("Bronze:", spark.table("workspace.bronze.vendas_bronze").count())\n'
             'print("Prata:", spark.table("workspace.bronze.vendas_prata").count())\n'
             'print("Ouro (receita_diaria):", spark.table("workspace.bronze.receita_diaria").count())'),
        code('# 3) Rodar a validação de negócio\n'
             'display(spark.sql("""\n'
             'SELECT SUM(receita) AS receita_total, COUNT(*) AS dias\n'
             'FROM workspace.bronze.receita_diaria\n'
             '"""))'),
        pratica("Ciclo completo no Job",
            "Na UI do Job, execute 'Run now' e observe: Task 1 (ingestão) → Task 2 (DLT) → "
            "Task 3 (validação). Cada falha deve disparar retry/alerta.",
        ),
        dica_prova("Revisão rápida: Auto Loader (cloudFiles), streaming (watermark, "
                   "checkpoint), DLT (3 níveis de expectation, materialized vs streaming), "
                   "Jobs (dependências, retry, agendamento). Tudo cai na DEA/DEP."),
        exercicios([
            "Documente o diagrama do pipeline no seu README do GitHub.",
            "Rode o Job 2x e confirme que os totais não duplicam (idempotência).",
        ]),
        gabarito([
            ("Diagrama",
             "Descreva: landing → AutoLoader → Bronze (ST) → Prata (ST/MT) → Ouro (MT) → "
             "Job diário com validação."),
            ("Idempotência",
             "DLT usa checkpoint + tabela incremental: rodar 2x processa apenas o delta — "
             "totais estáveis, sem duplicação."),
        ]),
        footer([
            "Rodei o pipeline DLT com expectations.",
            "Criei o Job com dependências e rodei com sucesso.",
            "Entendo materialized vs streaming table.",
            "Sei explicar Auto Loader + checkpoint em 2 frases.",
        ]),
    ],
))
