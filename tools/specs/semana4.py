"""Semana 4 — Delta Lake + Medallion completa (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana4_dia1_delta_lake_acid_time_travel",
    [
        header(
            "4", "1", "Delta Lake: ACID, Time Travel e o _delta_log",
            "Dominar o coração do Lakehouse: transações ACID, versionamento (Time Travel), "
            "VACUUM e o log de transações.",
            "DEA (Delta Lake)", "Time Travel exercitado com versões da tabela",
            "✅ Free Edition",
        ),
        teoria(
            "O que o Delta Lake resolve",
            "Parquet puro é um data lake sem transações: escrita interrompida corrompe, leitores "
            "veem estado inconsistente, updates são 'reescrever tudo'.\n\n"
            "O **Delta Lake** adiciona ao Parquet:\n"
            "- **ACID**: transações atômicas, consistentes, isoladas e duráveis\n"
            "- **Time Travel**: consultar qualquer versão histórica\n"
            "- **Schema enforcement e evolution**\n"
            "- **MERGE/UPSERT** e **Change Data Feed**\n\n"
            "Tecnicamente: um diretório com Parquet (dados) + `_delta_log/` (log JSON de "
            "transações). O log é a 'fonte da verdade'.",
        ),
        teoria(
            "O _delta_log",
            "Cada escrita (commit) adiciona um arquivo JSON `00000N.json` no `_delta_log`, "
            "descrevendo o que mudou (novos Parquet, arquivos removidos, metadados, "
            "constraints). Isso permite: leitura consistente, Time Travel e rollback.",
        ),
        pratica("Time Travel",
            "Faça commits na tabela e viaje no tempo."),
        code('# Garantir a tabela Bronze e um histórico de versões\n'
             'df = spark.table("workspace.bronze.vendas_bronze")\n'
             'print("Versões desta tabela:")\n'
             'display(spark.sql("DESCRIBE HISTORY workspace.bronze.vendas_bronze").select("version", "timestamp", "operation").limit(5))'),
        code('# Criar alterações para ter várias versões\n'
             'spark.sql("UPDATE workspace.bronze.vendas_bronze SET Country = \'BRASIL\' WHERE Country = \'Brazil\'")\n'
             'spark.sql("UPDATE workspace.bronze.vendas_bronze SET Country = \'Brazil\' WHERE Country = \'BRASIL\'")\n'
             'print("Foram criadas 2 novas versões (update).")'),
        code('# Time Travel: consultar uma versão antiga\n'
             '# 1) Por versão\n'
             'df_v0 = spark.read.format("delta").option("versionAsOf", 0).table("workspace.bronze.vendas_bronze")\n'
             '# 2) Por timestamp\n'
             'df_ts = spark.read.format("delta")\\\n'
             '    .option("timestampAsOf", "2024-01-01")\\\n'
             '    .table("workspace.bronze.vendas_bronze")\n'
             'print("Versão 0:", df_v0.count(), "| Antes de 2024:", df_ts.count())'),
        pratica("Restore e VACUUM",
            "`RESTORE` volta a tabela para uma versão; `VACUUM` apaga arquivos antigos "
            "(destrói Time Travel antigo)."),
        sql('-- Restore para a versão 0 (desfaz updates)\n'
            'RESTORE TABLE workspace.bronze.vendas_bronze TO VERSION AS OF 0;\n'
            'SELECT COUNT(*) FROM workspace.bronze.vendas_bronze;'),
        code('# VACUUM com retenção padrão (7 dias) — em tabelas grandes, libera espaço\n'
             '# ATENÇÃO: torna irreversível o Time Travel para além da retenção\n'
             'spark.sql("VACUUM workspace.bronze.vendas_bronze")  # opcional; pode demorar\n'
             'print("VACUUM remove arquivos órfãos/antigos além da retenção.")'),
        dica_prova("Time Travel: `DESCRIBE HISTORY`, `versionAsOf`, `timestampAsOf`, "
                   "`RESTORE TABLE ... TO VERSION`. VACUUM destrói Time Travel antigo — "
                   "pergunta clássica de prova."),
        exercicios([
            "Quantas versões sua tabela tem agora? Use DESCRIBE HISTORY.",
            "O que acontece com leitores ativos durante um VACUUM?",
            "Crie uma tabela Delta nova e faça: insert, update, delete, e restaure para antes do delete.",
        ]),
        gabarito([
            ("Versões",
             "`DESCRIBE HISTORY workspace.bronze.vendas_bronze` mostra a lista; a versão atual é a "
             "última linha."),
            ("VACUUM com leitores",
             "VACUUM respeita a retenção (7 dias por padrão) e as transações ativas: arquivos "
             "ainda necessários não são removidos. Leitores ativos usam a versão que começaram "
             "a ler."),
            ("Tabela e restore",
             "```sql\nCREATE TABLE workspace.bronze.t_teste (id INT, v STRING) USING DELTA;\nINSERT ...; UPDATE ...; DELETE ...;\nRESTORE TABLE workspace.bronze.t_teste TO VERSION AS OF 1;\n```"),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana4_dia2_delta_merge_schema_evolution",
    [
        header(
            "4", "2", "Delta: MERGE, schema evolution e constraints",
            "Dominar o upsert com MERGE, a evolução de schema e as constraints — o coração "
            "de pipelines incrementais.",
            "DEA (Delta)", "MERGE com schema evolution rodando",
            "✅ Free Edition",
        ),
        teoria(
            "O MERGE (upsert)",
            "**MERGE** insere, atualiza ou apaga linhas em uma única operação atômica: \n\n"
            "```sql\nMERGE INTO alvo t\nUSING origem s ON t.id = s.id\nWHEN MATCHED THEN UPDATE SET ...\nWHEN NOT MATCHED THEN INSERT ...\n```\n\n"
            "É o padrão para: deduplicar, SCD, cargas incrementais idempotentes. Sem MERGE, "
            "você precisaria de delete+insert não atômicos.",
        ),
        teoria(
            "Schema evolution",
            "Por padrão, uma escrita com colunas novas **falha** (enforcement). Com "
            "`mergeSchema = True` (ou `ALTER TABLE ADD COLUMN`), o schema evolui "
            "adicionando colunas. Use com cuidado: evolução automática pode quebrar "
            "consumidores.",
        ),
        pratica("MERGE na prática",
            "Monte uma tabela alvo e uma fonte com updates/inserts, e aplique MERGE."),
        code('# Alvo: dimensão de clientes (simulada)\n'
             'spark.sql("CREATE OR REPLACE TABLE workspace.prata.dim_cliente_teste (\n'
             '  CustomerID STRING, nome STRING, cidade STRING, is_current BOOLEAN) USING DELTA")\n'
             'spark.sql("INSERT INTO workspace.prata.dim_cliente_teste VALUES\n'
             '  (\'12345\', \'Ana\', \'SP\', true),\n'
             '  (\'67890\', \'João\', \'RJ\', true)")\n'
             'print("Alvo inicial criado")'),
        code('# Fonte: clientes novos + Ana mudou de cidade\n'
             'fonte = spark.createDataFrame([\n'
             '    ("12345", "Ana", "CAMPINAS"),\n'
             '    ("99999", "Maria", "BH"),\n'
             '], ["CustomerID", "nome", "cidade"])\n'
             'fonte.createOrReplaceTempView("fonte_cli")\n'
             'print("Fonte com 1 update + 1 insert")'),
        sql('-- MERGE: atualiza Ana, insere Maria\n'
            'MERGE INTO workspace.prata.dim_cliente_teste t\n'
            'USING fonte_cli s ON t.CustomerID = s.CustomerID\n'
            'WHEN MATCHED THEN UPDATE SET t.cidade = s.cidade\n'
            'WHEN NOT MATCHED THEN INSERT (CustomerID, nome, cidade, is_current)\n'
            '  VALUES (s.CustomerID, s.nome, s.cidade, true);\n'
            'SELECT * FROM workspace.prata.dim_cliente_teste ORDER BY CustomerID;'),
        pratica("Schema evolution",
            "Adicione uma coluna nova na fonte e evolua o schema do alvo."),
        code('# Fonte com coluna nova (email)\n'
             'fonte2 = spark.createDataFrame([("12345", "Ana", "CAMPINAS", "ana@x.com")],\n'
             '                               ["CustomerID", "nome", "cidade", "email"])\n'
             'fonte2.createOrReplaceTempView("fonte2")\n'
             'print("Fonte agora tem coluna email")'),
        sql('-- MERGE com schema evolution (novo campo email)\n'
            'MERGE INTO workspace.prata.dim_cliente_teste t\n'
            'USING fonte2 s ON t.CustomerID = s.CustomerID\n'
            'WHEN MATCHED THEN UPDATE SET t.cidade = s.cidade\n'
            'WHEN NOT MATCHED THEN INSERT (CustomerID, nome, cidade, is_current)\n'
            '  VALUES (s.CustomerID, s.nome, s.cidade, true);\n'
            '-- Falha por padrão (enforcement)!\n'
            '-- Para permitir evolução, use spark.conf ou ALTER TABLE:'),
        code('# Habilitar evolução automática e refazer\n'
             'spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")\n'
             'spark.sql("""\n'
             'MERGE INTO workspace.prata.dim_cliente_teste t\n'
             'USING fonte2 s ON t.CustomerID = s.CustomerID\n'
             'WHEN MATCHED THEN UPDATE SET t.cidade = s.cidade, t.email = s.email\n'
             'WHEN NOT MATCHED THEN INSERT *\n'
             '""")\n'
             'display(spark.sql("SELECT * FROM workspace.prata.dim_cliente_teste"))'),
        dica_prova("MERGE com `WHEN NOT MATCHED THEN INSERT *` + `autoMerge` evolui schema "
                   "automaticamente. Pergunta típica: o que acontece sem schema evolution? "
                   "→ falha de análise."),
        exercicios([
            "Escreva um MERGE que faça UPDATE apenas quando a cidade mudou (evita escrita desnecessária).",
            "O que `INSERT *` faz no MERGE?",
            "Crie um SCD1 simples com MERGE (update de cidade sem histórico).",
        ]),
        gabarito([
            ("MERGE condicional",
             "```sql\nWHEN MATCHED AND t.cidade <> s.cidade THEN UPDATE SET t.cidade = s.cidade\n```"),
            ("INSERT *",
             "Insere todas as colunas da fonte que não estão na condição de match — com "
             "autoMerge, cria as colunas novas automaticamente."),
            ("SCD1",
             "O MERGE acima (update direto) É o SCD1: sobrescreve o valor antigo, sem histórico."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana4_dia3_otimizacao_liquid_clustering",
    [
        header(
            "4", "3", "Otimização: OPTIMIZE, Liquid Clustering e VACUUM",
            "Entender por que tabelas Delta degeneram com o tempo e como manter performance "
            "com Liquid Clustering (padrão 2026) e OPTIMIZE.",
            "DEA, DEP (performance)", "Tabela clusterizada + OPTIMIZE aplicado",
            "✅ Free Edition",
        ),
        teoria(
            "Por que otimizar?",
            "A cada escrita, o Delta cria novos Parquet pequenos. Com o tempo: **muitos "
            "arquivos pequenos** → leituras lentas (muito overhead). O `OPTIMIZE` compacta "
            "arquivos pequenos em maiores (bin-packing).",
        ),
        teoria(
            "Particionamento vs Liquid Clustering",
            "**Particionamento** (`PARTITIONED BY (ano)`) divide em pastas fixas por coluna de "
            "baixa cardinalidade. Bom para data/hora; ruim para colunas de alta cardinalidade "
            "(muitas partições = muitos arquivos minúsculos).\n\n"
            "**Liquid Clustering** (padrão 2026) usa `CLUSTER BY` e re-organiza dados de forma "
            "adaptativa (Z-ORDER foi deprecado — use CLUSTER BY):\n\n"
            "```sql\nCREATE TABLE t (col1 STRING, col2 INT) USING DELTA CLUSTER BY (col1, col2);\n```\n\n"
            "Vantagem: mantém o clustering automático em cada escrita e funciona com alta "
            "cardinalidade. **Regra**: mais de 1 TB → cluster por 1–4 colunas; abaixo disso, "
            "o OPTIMIZE ocasional é suficiente.",
        ),
        teoria(
            "OPTIMIZE e VACUUM",
            "`OPTIMIZE` reescreve e reordena arquivos; `OPTIMIZE ... ZORDER BY` ordenava "
            "por coluna (legado; com Liquid Clustering use `CLUSTER BY`). "
            "`VACUUM` remove arquivos órfãos e versões antigas (liberando espaço).",
        ),
        pratica("Criando tabela com Liquid Clustering",
            "Crie a tabela de fatos já clusterizada — o padrão de produção."),
        sql('CREATE OR REPLACE TABLE workspace.prata.fato_vendas_teste (\n'
            '  InvoiceNo STRING, StockCode STRING, CustomerID STRING, Country STRING,\n'
            '  data_venda DATE, quantidade INT, valor DOUBLE)\n'
            'USING DELTA\n'
            'CLUSTER BY (Country, data_venda);\n'
            'SELECT COUNT(*) FROM workspace.prata.fato_vendas_teste;'),
        code('# Popular a tabela clusterizada (a partir do Bronze)\n'
             'from pyspark.sql.functions import to_date\n'
             'df = (spark.table("workspace.bronze.vendas_bronze")\n'
             '    .select("InvoiceNo", "StockCode", "CustomerID", "Country",\n'
             '            to_date("InvoiceDate", "M/d/yyyy H:mm").alias("data_venda"),\n'
             '            "Quantity", "UnitPrice")\n'
             '    .filter("CustomerID IS NOT NULL"))\n'
             'df.write.mode("overwrite").saveAsTable("workspace.prata.fato_vendas_teste")\n'
             'print("Populado:", spark.table("workspace.prata.fato_vendas_teste").count())'),
        code('# OPTIMIZE: compactar arquivos pequenos\n'
             'spark.sql("OPTIMIZE workspace.prata.fato_vendas_teste")\n'
             'print("Arquivos antes/depois (veja o Spark UI e o diretório da tabela).")'),
        pratica("Analisando o efeito",
            "Compare o número de arquivos antes e depois do OPTIMIZE."),
        code('# Ver os arquivos físicos da tabela\n'
             'display(spark.sql("DESCRIBE DETAIL workspace.prata.fato_vendas_teste").select("location"))\n'
             'tabela = spark.table("workspace.prata.fato_vendas_teste")\n'
             'print("NumFiles (do delta log):", spark.sql("DESCRIBE DETAIL workspace.prata.fato_vendas_teste").select("numFiles").collect()[0][0])'),
        dica_prova("DEA 2026 usa **Liquid Clustering** (CLUSTER BY) como recomendação; "
                   "Z-ORDER é legado. Pergunta típica: particionamento vs clustering para "
                   "coluna de alta cardinalidade → clustering."),
        exercicios([
            "Quando usar particionamento vs Liquid Clustering?",
            "O que OPTIMIZE faz internamente?",
            "Crie uma tabela com CLUSTER BY em 2 colunas e rode OPTIMIZE.",
        ]),
        gabarito([
            ("Particionar vs cluster",
             "Particionar: colunas de baixa cardinalidade e consultas por filtro exato (ex.: "
             "ano). Cluster: alta cardinalidade, múltiplas colunas de filtro, atualizações "
             "frequentes."),
            ("OPTIMIZE",
             "Compacta arquivos pequenos (bin-packing) e, com clustering, reordena dados — "
             "reduz overhead de leitura e acelera consultas por filtro."),
            ("Prática",
             "`CREATE TABLE ... USING DELTA CLUSTER BY (col1, col2)` + `OPTIMIZE t`."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana4_dia4_camada_prata_dimensoes_fato",
    [
        header(
            "4", "4", "Camada Prata: dimensões e tabela fato (Star Schema)",
            "Construir a camada Prata do projeto — dimensões (cliente, produto, tempo) e "
            "fato (vendas) — com deduplicação, tipagem e chaves surrogate.",
            "DEA (medallion)", "Prata completa: dim_cliente, dim_produto, dim_tempo, fato_vendas",
            "✅ Free Edition",
        ),
        teoria(
            "O papel da Prata",
            "A camada Prata transforma o Bronze cru em um modelo limpo e reutilizável: "
            "deduplicado, tipado, validado e modelado (dimensões + fatos). Regras:\n"
            "- **Idempotente**: rodar N vezes = mesmo resultado.\n"
            "- **Sem dados brutos**: só o que é necessário.\n"
            "- **Chaves surrogate** (`sk_*`) para cada dimensão.",
        ),
        pratica("Criando as dimensões",
            "Comece pelas dimensões — elas são as 'tabelas de contexto'."),
        code('# dim_cliente: deduplicado e tipado\n'
             'from pyspark.sql.functions import col, row_number, min, max, count, sum as s\n'
             'from pyspark.sql.window import Window\n'
             'df = spark.table("workspace.bronze.vendas_bronze")\n'
             'clientes = (df\n'
             '    .filter(col("CustomerID").isNotNull())\n'
             '    .groupBy("CustomerID", "Country")\n'
             '    .agg(count("*").alias("n_vendas"),\n'
             '         min("InvoiceDate").alias("primeira_compra"),\n'
             '         max("InvoiceDate").alias("ultima_compra"))\n'
             '    .withColumn("sk_cliente", row_number().over(Window.orderBy("CustomerID"))))\n'
             'clientes.createOrReplaceTempView("dim_cliente_vw")\n'
             'clientes.show(5, truncate=False)\n'
             'print("Total de clientes:", clientes.count())'),
        code('# dim_produto\n'
             'produtos = (df\n'
             '    .select("StockCode", "Description")\n'
             '    .dropDuplicates(["StockCode"])\n'
             '    .filter(col("StockCode").isNotNull())\n'
             '    .withColumn("sk_produto", row_number().over(Window.orderBy("StockCode"))))\n'
             'produtos.createOrReplaceTempView("dim_produto_vw")\n'
             'produtos.show(5, truncate=False)'),
        code('# dim_tempo (a partir das datas das vendas)\n'
             'from pyspark.sql.functions import to_date, year, month, dayofmonth, quarter\n'
             'datas = (df\n'
             '    .select(to_date("InvoiceDate", "M/d/yyyy H:mm").alias("data_venda"))\n'
             '    .dropDuplicates()\n'
             '    .filter(col("data_venda").isNotNull())\n'
             '    .withColumn("ano", year("data_venda"))\n'
             '    .withColumn("mes", month("data_venda"))\n'
             '    .withColumn("dia", dayofmonth("data_venda"))\n'
             '    .withColumn("trimestre", quarter("data_venda"))\n'
             '    .withColumn("sk_tempo", row_number().over(Window.orderBy("data_venda"))))\n'
             'datas.createOrReplaceTempView("dim_tempo_vw")\n'
             'datas.show(5)'),
        pratica("Criando o fato",
            "O fato conecta as dimensões por chave e carrega as medidas."),
        code('# fato_vendas: junta as chaves das dimensões\n'
             'from pyspark.sql.functions import to_date, col as c\n'
             'fato = (df\n'
             '    .filter(c("CustomerID").isNotNull())\n'
             '    .withColumn("data_venda", to_date("InvoiceDate", "M/d/yyyy H:mm"))\n'
             '    .join(clientes.select("CustomerID", "sk_cliente"), "CustomerID", "left")\n'
             '    .join(produtos.select("StockCode", "sk_produto"), "StockCode", "left")\n'
             '    .join(datas.select("data_venda", "sk_tempo"), "data_venda", "left")\n'
             '    .select("InvoiceNo", "sk_cliente", "sk_produto", "sk_tempo",\n'
             '            "Quantity", "UnitPrice", "Country")\n'
             '    .withColumn("receita", c("Quantity") * c("UnitPrice")))\n'
             'fato.createOrReplaceTempView("fato_vendas_vw")\n'
             'fato.show(5, truncate=False)'),
        code('# Gravar a Prata (idempotente)\n'
             'spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.prata")\n'
             'clientes.write.mode("overwrite").saveAsTable("workspace.prata.dim_cliente")\n'
             'produtos.write.mode("overwrite").saveAsTable("workspace.prata.dim_produto")\n'
             'datas.write.mode("overwrite").saveAsTable("workspace.prata.dim_tempo")\n'
             'fato.write.mode("overwrite").saveAsTable("workspace.prata.fato_vendas")\n'
             'print("Prata completa!")'),
        sql('-- Conferência: fato + dimensões via join (o star schema funcionando)\n'
            'SELECT c.sk_cliente, p.sk_produto, t.ano, f.receita\n'
            'FROM workspace.prata.fato_vendas f\n'
            'JOIN workspace.prata.dim_cliente c ON f.sk_cliente = c.sk_cliente\n'
            'JOIN workspace.prata.dim_produto p ON f.sk_produto = p.sk_produto\n'
            'JOIN workspace.prata.dim_tempo t ON f.sk_tempo = t.sk_tempo\n'
            'LIMIT 10'),
        dica_prova("A DEA cobra a ordem das camadas e as regras: Bronze append-only, "
                   "Prata idempotente/limpa, Ouro denormalizado/agregado. Memorize as "
                   "**regras da Medallion**."),
        exercicios([
            "Por que a Prata deve ser idempotente?",
            "Qual a diferença entre sk_ (surrogate) e chave natural?",
            "Refaça a dim_cliente adicionando a cidade do cliente como atributo.",
        ]),
        gabarito([
            ("Idempotente",
             "Para permitir reprocessamento sem duplicar dados: rodar 2x produz o mesmo "
             "resultado (overwrite/merge). Sem isso, pipelines falham e duplicam."),
            ("Surrogate vs natural",
             "Surrogate (sk_) é artificial, estável e não depende da fonte (sobrevive a "
             "mudanças de chave natural). Natural é o ID do sistema de origem."),
            ("Cidade",
             "Derive de `Country`/endereço na fonte ou de um lookup; na dim_cliente o ideal é "
             "a cidade do cadastro — para nosso dataset, podemos usar o país como proxy."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana4_dia5_camada_ouro_agregados_negocio",
    [
        header(
            "4", "5", "Camada Ouro: agregados de negócio",
            "Construir a camada Ouro — agregações denormalizadas prontas para BI e IA "
            "(vendas por dia, receita por país, top produtos).",
            "DEA (medallion, BI)", "Tabelas Ouro criadas + dashboard conectado",
            "✅ Free Edition",
        ),
        teoria(
            "O papel do Ouro",
            "O **Ouro** é o que analistas, BI e modelos consomem: denormalizado, agregado e "
            "estável. 'Denormalizado' = joins já resolvidos, KPI direto.\n\n"
            "Regras: poucas tabelas, colunas claras, sem lixo, sempre atualizado pelo pipeline.",
        ),
        pratica("Criando os agregados",
            "Crie as 3 tabelas Ouro do projeto a partir da Prata."),
        code('# vendas_por_dia (série temporal para BI e previsão)\n'
             'vendas_por_dia = (spark.table("workspace.prata.fato_vendas")\n'
             '    .groupBy("sk_tempo")\n'
             '    .agg(s("receita").alias("receita_total"),\n'
             '         count("*").alias("n_vendas"),\n'
             '         countDistinct("InvoiceNo").alias("n_notas"))\n'
             '    .join(spark.table("workspace.prata.dim_tempo").select("sk_tempo", "data_venda"), "sk_tempo")\n'
             '    .select("data_venda", "receita_total", "n_vendas", "n_notas")\n'
             '    .orderBy("data_venda"))\n'
             'vendas_por_dia.show(5)'),
        code('# receita_por_pais\n'
             'receita_por_pais = (spark.table("workspace.prata.fato_vendas")\n'
             '    .groupBy("Country")\n'
             '    .agg(s("receita").alias("receita_total"), count("*").alias("n_vendas"))\n'
             '    .orderBy(col("receita_total").desc()))\n'
             'receita_por_pais.show(5)'),
        code('# top_produtos\n'
             'top_produtos = (spark.table("workspace.prata.fato_vendas")\n'
             '    .groupBy("sk_produto")\n'
             '    .agg(s("receita").alias("receita_total"), count("*").alias("n_vendas"))\n'
             '    .join(spark.table("workspace.prata.dim_produto").select("sk_produto", "StockCode", "Description"), "sk_produto")\n'
             '    .orderBy(col("receita_total").desc())\n'
             '    .limit(20))\n'
             'top_produtos.show(5, truncate=False)'),
        code('# Gravar o Ouro\n'
             'spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.ouro")\n'
             'vendas_por_dia.write.mode("overwrite").saveAsTable("workspace.ouro.vendas_por_dia")\n'
             'receita_por_pais.write.mode("overwrite").saveAsTable("workspace.ouro.receita_por_pais")\n'
             'top_produtos.write.mode("overwrite").saveAsTable("workspace.ouro.top_produtos")\n'
             'print("Camada Ouro criada!")'),
        pratica("Dashboard conectado ao Ouro",
            "Crie visualizações no Databricks SQL sobre o Ouro."),
        sql('-- Query para o dashboard\n'
            'SELECT data_venda, receita_total\n'
            'FROM workspace.ouro.vendas_por_dia\n'
            'ORDER BY data_venda'),
        dica_prova("A Ouro é **denormalizada e agregada** para BI/IA — nunca dados brutos. "
                   "Pergunta típica: 'onde coloco uma view de KPI?' → Ouro."),
        exercicios([
            "Crie uma tabela Ouro `vendas_por_dia_pais` (data × país × receita).",
            "Qual camada um modelo de ML deve consumir? Por quê?",
        ]),
        gabarito([
            ("vendas_por_dia_pais",
             "```python\n(spark.table('workspace.prata.fato_vendas').groupBy('sk_tempo','Country').agg(sum('receita').alias('receita')).join(spark.table('workspace.prata.dim_tempo'),'sk_tempo').select('data_venda','Country','receita').write.mode('overwrite').saveAsTable('workspace.ouro.vendas_por_dia_pais'))\n```"),
            ("ML no Ouro",
             "Ouro: agregados limpos e estáveis → treinar previsão de receita. (Para features "
             "granulares, usa-se Feature Engineering sobre Prata/Ouro — Semana 10.)"),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana4_dia6_revisao_exercicios_delta_medallion",
    [
        header(
            "4", "6", "Revisão Delta + Medallion e exercícios de prova",
            "Consolidar a semana com exercícios no formato da prova e garantir que a "
            "arquitetura Medallion está sólida.",
            "DEA (Delta + medallion)", "Exercícios resolvidos + checklist",
            "✅ Free Edition",
        ),
        teoria(
            "O mapa mental da Semana 4",
            "```\nDelta Lake\n ├─ ACID + _delta_log\n ├─ Time Travel (versionAsOf/timestampAsOf/RESTORE)\n ├─ MERGE (upsert) + schema evolution\n ├─ OPTIMIZE + Liquid Clustering + VACUUM\n └─ constraints (CHECK/NOT NULL)\n\nMedallion\n ├─ Bronze: cru, append-only, _ingested_at\n ├─ Prata: limpo, dedup, star schema (dim_*, fato_*)\n └─ Ouro: agregados denormalizados (KPIs)\n```",
        ),
        pratica("Exercícios rápidos",
            "Rode e confira com o gabarito."),
        sql('-- 1. Quantas versões a fato_vendas tem?\n'
            'DESCRIBE HISTORY workspace.prata.fato_vendas'),
        sql('-- 2. Constraint de quantidade positiva na fato\n'
            'ALTER TABLE workspace.prata.fato_vendas ADD CONSTRAINT ck_fato_qtd CHECK (Quantity > 0);\n'
            'SHOW TBLPROPERTIES workspace.prata.fato_vendas ("delta.constraints.*")'),
        code('# 3. MERGE de atualização na dim_cliente (SCD1)\n'
             'fonte = spark.createDataFrame([("12345", "CAMPINAS")], ["CustomerID", "cidade_nova"])\n'
             'fonte.createOrReplaceTempView("f")\n'
             'spark.sql("""\n'
             'MERGE INTO workspace.prata.dim_cliente t USING f ON t.CustomerID = f.CustomerID\n'
             'WHEN MATCHED THEN UPDATE SET t.Country = f.cidade_nova\n'
             '""")\n'
             'print("MERGE executado (SCD1 simples).")'),
        md("""### Perguntas estilo prova (marque antes do gabarito)

**1.** Uma escrita com coluna nova sem `mergeSchema`:
- A) evolui automaticamente  B) falha  C) ignora a coluna  D) duplica

**2.** `VACUUM` com retenção de 7 dias:
- A) apaga todos os arquivos  B) apaga arquivos órfãos/antigos fora da retenção
- C) nada  D) apaga o _delta_log

**3.** Para histórico completo de endereço de cliente (SCD2), qual ferramenta:
- A) MERGE simples  B) `APPLY CHANGES INTO` (SCD2)  C) UPDATE  D) DELETE

**4.** Onde colocar `vendas_por_dia`?
- A) Bronze  B) Prata  C) Ouro  D) FileStore

**5.** `OPTIMIZE` resolve qual problema?
- A) dados duplicados  B) muitos arquivos pequenos  C) schema errado  D) dados nulos
"""),
        teoria(
            "Gabarito",
            "**1-B** (enforcement falha; autoMerge evolui) · **2-B** · **3-B** (`APPLY CHANGES "
            "INTO` é o padrão SCD2 — Semana 8) · **4-C** · **5-B**.",
        ),
        dica_prova("Revisão final: as 4 perguntas que caem em toda prova Delta: Time Travel, "
                   "MERGE, constraints, OPTIMIZE/Liquid Clustering. Você domina todas."),
        exercicios([
            "Explique a Medallion para um colega em 2 minutos (teste de ensino).",
            "Crie um diagrama no seu caderno com as tabelas Bronze/Prata/Ouro atuais.",
        ]),
        gabarito([
            ("Ensino",
             "Se você consegue ensinar, você sabe. Compare com o mapa mental da teoria."),
            ("Diagrama",
             "Bronze: vendas/voos/clientes · Prata: dim_cliente, dim_produto, dim_tempo, "
             "fato_vendas · Ouro: vendas_por_dia, receita_por_pais, top_produtos."),
        ]),
        footer([
            "Rodei os 6 notebooks da Semana 4.",
            "Criei Prata (4 tabelas) e Ouro (3 tabelas) no meu workspace.",
            "Domino MERGE, Time Travel e Liquid Clustering.",
            "Refiz os exercícios de prova com gabarito.",
        ]),
    ],
))
