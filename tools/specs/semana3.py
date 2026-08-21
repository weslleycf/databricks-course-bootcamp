"""Semana 3 — Spark: DataFrame API, Spark SQL e internals (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana3_dia1_spark_arquitetura_lazy_dag",
    [
        header(
            "3", "1", "Spark: arquitetura, lazy evaluation e DAG",
            "Entender como o Spark executa por baixo dos panos: driver/executors, lazy "
            "evaluation, Catalyst e DAG — a base para performance na Semana 8.",
            "DEA (Spark), DEP (performance)", "Diagrama mental do pipeline Spark",
            "✅ Free Edition",
        ),
        teoria(
            "A arquitetura do Spark",
            "Um cluster Spark tem:\n"
            "- **Driver**: 'o maestro'. Recebe seu código, monta o plano de execução e coordena "
            "os executores.\n"
            "- **Executors**: 'os músicos'. Rodam as tarefas (tasks) em paralelo, cada um numa "
            "partição dos dados.\n"
            "- **Partições**: fatias dos dados distribuídas entre os executores — o paralelismo "
            "vem daqui.\n\n"
            "```\n         Driver (plano)\n        /      |       \\\n  Executor   Executor   Executor\n  [part 0]   [part 1]   [part 2]\n```\n\n"
            "Na **Free Edition**, o compute é **serverless**: o Databricks provisiona driver + "
            "executores para você, sem configurar máquinas.",
        ),
        teoria(
            "Lazy evaluation e o DAG",
            "O Spark é **preguiçoso (lazy)**: chamar `.filter()`, `.select()`, `.join()` NÃO "
            "executa nada — só **constrói um grafo** de transformações, o **DAG (Directed "
            "Acyclic Graph)**.\n\n"
            "A execução só dispara numa **ação**: `.count()`, `.show()`, `.collect()`, "
            "`.write()`, `.saveAsTable()`.\n\n"
            "**Consequência prática**: você pode encadear 20 transformações sem custo; o custo "
            "vem quando o resultado é materializado. E o Spark **reordena/otimiza** o DAG "
            "antes de rodar (otimizador Catalyst + AQE).",
        ),
        teoria(
            "DataFrame vs RDD",
            "O **DataFrame** é a API moderna: colunas tipadas, otimizada pelo Catalyst, com "
            "schema. O **RDD** é a API antiga de baixo nível (linhas sem schema).\n\n"
            "> 🎯 **Dica de prova (DEA 2026)**: a prova **removeu RDDs** do escopo ('ELT with "
            "Spark SQL and Python'). Você NÃO precisa programar RDD — mas entender que por "
            "baixo tudo vira tarefas em partições ajuda em entrevistas.",
        ),
        pratica("Primeiro DAG",
            "Crie um DataFrame e observe a preguiça do Spark: as transformações retornam "
            "instantaneamente; a ação dispara o trabalho."),
        code('# Transformações (lazy) — retornam na hora\n'
             'df = spark.range(10_000_000)\n'
             'transformado = (df\n'
             '    .withColumn("dobro", df["id"] * 2)\n'
             '    .filter("dobro % 3 == 0"))\n'
             'print("Transformação criada (lazy) — nada foi executado ainda.")\n'
             'print("Tipo:", type(transformado).__name__)'),
        code('# Ação (eager) — dispara o trabalho\n'
             'print("Executando ação count()...")\n'
             'n = transformado.count()\n'
             'print("Linhas resultantes:", n)'),
        code('# Spark UI: veja o DAG da última ação\n'
             '# Na UI do notebook, clique no ícone de gráfico (Spark UI) da célula acima.\n'
             '# Procure a aba SQL/Job: é o DAG (estágios de tasks).\n'
             'print("O Spark UI mostra o DAG de cada job. Explore depois da execução!")'),
        dica_prova("Pergunta clássica: 'o que dispara a execução no Spark?' → uma **ação**. "
                   "Transformações são lazy. Outra: 'onde roda a task?' → em um executor, sobre "
                   "uma partição."),
        exercicios([
            "Liste 4 ações e 4 transformações.",
            "Por que `df.filter(...)` não executa nada?",
            "Qual a diferença entre driver e executor?",
            "Por que RDDs saíram do escopo da DEA 2026?",
        ]),
        gabarito([
            ("Ações e transformações",
             "Ações: count, show, collect, write, saveAsTable, take. Transformações: select, "
             "filter, join, groupBy, withColumn, orderBy."),
            ("Lazy",
             "Porque o Spark constrói o DAG (plano) primeiro e só executa quando precisa de um "
             "resultado materializado (ação). Isso permite otimizar o plano inteiro."),
            ("Driver vs executor",
             "Driver coordena (planeja, distribui tasks, agrega resultados); executor executa as "
             "tasks sobre partições em paralelo."),
            ("RDD fora",
             "A DEA 2026 focou o escopo em ELT com Spark SQL e Python (DataFrame API); RDD é "
             "legado, usado raramente em produção."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana3_dia2_leitura_escrita_formatos_schema",
    [
        header(
            "3", "2", "Leitura e escrita: formatos, opções e schema",
            "Dominar a leitura/escrita de CSV, JSON, Parquet e Delta com schema enforcement, "
            "paths via Volumes/DBFS e opções importantes.",
            "DEA (ELT)", "Leitura correta dos 4 formatos com schema explícito",
            "✅ Free Edition",
        ),
        teoria(
            "Schema enforcement vs inferência",
            "Quando você lê um CSV sem schema, o Spark **infere** os tipos — mas isso pode errar "
            "(ex.: `000123` vira INT perdendo zeros à esquerda).\n\n"
            "Em produção, defina o **schema explícito**: mais rápido, determinístico e seguro. "
            "No Delta, o schema fica gravado na tabela — sempre enforcement.",
        ),
        teoria(
            "Paths: DBFS vs Volumes",
            "**DBFS**: `dbfs:/FileStore/...` — legado, mas prático para arquivos de estudo.\n"
            "**Volumes**: `/Volumes/workspace/bronze/vol_dados_curso/...` — o padrão 2026, governado "
            "pelo UC.\n\n"
            "> 🎯 **Dica de prova**: a DEA 2026 cobre a recomendação de usar **Volumes** para "
            "arquivos e a diferença entre paths de Volume e DBFS.",
        ),
        pratica("Schema explícito",
            "Defina o schema do CSV do projeto com `StructType` e leia com ele."),
        code('# Schema explícito do CSV de vendas\n'
             'from pyspark.sql.types import (StructType, StructField, StringType, IntegerType,\n'
             '                               DoubleType, TimestampType)\n'
             'schema_vendas = StructType([\n'
             '    StructField("InvoiceNo", StringType(), True),\n'
             '    StructField("StockCode", StringType(), True),\n'
             '    StructField("Description", StringType(), True),\n'
             '    StructField("Quantity", IntegerType(), True),\n'
             '    StructField("InvoiceDate", StringType(), True),\n'
             '    StructField("UnitPrice", DoubleType(), True),\n'
             '    StructField("CustomerID", StringType(), True),\n'
             '    StructField("Country", StringType(), True),\n'
             '])\n'
             'df = (spark.read\n'
             '    .format("csv")\n'
             '    .option("header", True)\n'
             '    .option("multiLine", True)\n'
             '    .schema(schema_vendas)\n'
             '    .load("/Volumes/workspace/bronze/vol_dados_curso/vendas.csv"))\n'
             'df.printSchema()\n'
             'print("Linhas:", df.count())'),
        pratica("Escrita com modo",
            "O parâmetro `mode` decide o que fazer quando o destino existe: `overwrite`, "
            "`append`, `error`, `ignore`."),
        code('# Escrita nos modos comuns (no Volume do curso)\n'
             'df.limit(1000).write.mode("overwrite").format("parquet").save("/Volumes/workspace/bronze/vol_dados_curso/vendas_amostra")\n'
             'df.limit(100).write.mode("append").format("parquet").save("/Volumes/workspace/bronze/vol_dados_curso/vendas_amostra")\n'
             'print("Amostra gravada e estendida (overwrite + append).")'),
        code('# Volumes: o caminho moderno\n'
             'spark.sql("CREATE VOLUME IF NOT EXISTS workspace.bronze.vol_dados_curso")\n'
             'path_volume = "/Volumes/workspace/bronze/vol_dados_curso/vendas.parquet"\n'
             'df.limit(1000).write.mode("overwrite").format("parquet").save(path_volume)\n'
             'print("Gravado no Volume:", path_volume)'),
        dica_prova("`mode('overwrite')` em tabela managed pode apagar dados se o schema mudar — "
                   "na prova, prefira `overwrite` explícito com schema compatível, e lembre: "
                   "em pipelines de Bronze use **append** (append-only)."),
        exercicios([
            "Leia o JSON do projeto (`/Volumes/workspace/bronze/vol_dados_curso/vendas.json`) com schema explícito.",
            "Qual opção usa `header` e `multiLine` para CSV?",
            "Escreva 1000 linhas em Parquet num Volume e leia de volta contando.",
        ]),
        gabarito([
            ("JSON com schema",
             "`spark.read.schema(schema_vendas).json('/Volumes/workspace/bronze/vol_dados_curso/vendas.json')` — para JSON o caminho "
             "de um arquivo único, sem header."),
            ("Opções CSV",
             "`.option('header', True)` (primeira linha é cabeçalho) e `.option('multiLine', True)` "
             "(quebra de linha dentro de campos entre aspas)."),
            ("Volume",
             "`df.write.mode('overwrite').format('parquet').save('/Volumes/workspace/bronze/vol_dados_curso/vendas.parquet')` "
             "e depois `spark.read.parquet(...)` contando linhas."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana3_dia3_transformacoes_joins_agregacoes",
    [
        header(
            "3", "3", "Transformações: select, withColumn, joins e agregações",
            "Dominar as transformações ELT mais usadas em produção com a DataFrame API.",
            "DEA (ELT with Spark)", "Pipeline de transformação limpo rodando",
            "✅ Free Edition",
        ),
        teoria(
            "As transformações do dia a dia",
            "| Operação | Uso |\n|---|---|\n"
            "| `select` | escolher colunas |\n"
            "| `withColumn` | criar/alterar coluna (com expressão) |\n"
            "| `filter` / `where` | filtrar linhas |\n"
            "| `groupBy().agg()` | agregações |\n"
            "| `join` | combinar tabelas |\n"
            "| `union` / `unionByName` | empilhar tabelas |\n"
            "| `dropDuplicates` | deduplicar |\n"
            "| `orderBy` | ordenar |\n\n"
            "**Regra de ouro**: prefira expressões de coluna (Spark SQL) a UDFs Python — "
            "expressões são otimizadas pelo Catalyst e executadas em JVM; UDFs Python são "
            "centenas de vezes mais lentas.",
        ),
        teoria(
            "Tipos de join",
            "| Join | Devolve | Uso típico |\n|---|---|---|\n"
            "| inner | só correspondências | padrão |\n"
            "| left | tudo da esquerda + match à direita | enriquecer |\n"
            "| right | tudo da direita + match à esquerda | raro |\n"
            "| full | tudo de ambos | auditoria |\n"
            "| left semi | linhas da esquerda com match | filtro eficiente |\n"
            "| left anti | linhas da esquerda SEM match | exclusão/validação |\n\n"
            "> 🎯 **Dica de prova**: `left semi` = filtro (sem colunas da direita); `left anti` = "
            "exclusão. São perguntas garantidas na DEA.",
        ),
        pratica("Pipeline de transformação",
            "Construa um pipeline ELT sobre o Bronze: limpeza, enriquecimento e agregação."),
        code('# Ler o Bronze\n'
             'from pyspark.sql.functions import col, when, upper, round as r, sum as s, to_date\n'
             'df = spark.table("workspace.bronze.vendas_bronze")\n'
             'print("Linhas:", df.count())'),
        code('# Limpeza e enriquecimento\n'
             'df_enriquecido = (df\n'
             '    .filter(col("CustomerID").isNotNull())\n'
             '    .withColumn("pais_upper", upper(col("Country")))\n'
             '    .withColumn("receita_linha", r(col("Quantity") * col("UnitPrice"), 2))\n'
             '    .withColumn("categoria_preco",\n'
             '        when(col("UnitPrice") < 2, "barato")\n'
             '        .when(col("UnitPrice") < 20, "medio")\n'
             '        .otherwise("caro")))\n'
             'df_enriquecido.select("InvoiceNo", "Country", "pais_upper", "receita_linha", "categoria_preco").show(5, truncate=False)'),
        code('# Agregação + join\n'
             'receita_por_pais = (df_enriquecido\n'
             '    .groupBy("pais_upper")\n'
             '    .agg(s("receita_linha").alias("receita_total"))\n'
             '    .orderBy(col("receita_total").desc()))\n'
             'receita_por_pais.show(5)'),
        pratica("Joins na prática",
            "Crie uma dimensão pequena de categoria e faça os joins."),
        code('# Dimensão de exemplo (categoria por StockCode)\n'
             'categorias = spark.createDataFrame([\n'
             '    ("85123A", "Decoração"), ("71053", "Cozinha"), ("84406B", "Papelaria"),\n'
             '    ("22423", "Iluminação"), ("47566", "Vestuário"),\n'
             '], ["StockCode", "categoria"])\n'
             '# inner: só produtos com categoria conhecida\n'
             'df_inner = df_enriquecido.join(categorias, "StockCode", "inner")\n'
             'print("inner:", df_inner.count())\n'
             '# left anti: produtos sem categoria cadastrada\n'
             'df_sem_cat = df_enriquecido.join(categorias, "StockCode", "left_anti")\n'
             'print("left_anti (sem categoria):", df_sem_cat.select("StockCode").distinct().count())'),
        dica_prova("UDF Python vs expressão: a prova pergunta por que expressões são preferíveis "
                   "(performance; Catalyst otimiza; execução JVM). Evite UDFs quando houver "
                   "função nativa."),
        exercicios([
            "Use `dropDuplicates(['CustomerID'])` e explique o que acontece.",
            "Faça um join left e diga quantas linhas ficam com categoria nula.",
            "Crie coluna `faixa` com when: receita < 50 → 'baixa', < 200 → 'media', senão 'alta'.",
        ]),
        gabarito([
            ("dropDuplicates",
             "Remove linhas duplicadas **na combinação das colunas indicadas** (aqui, um registro "
             "por cliente, mantendo o primeiro). Para dedup por chave é padrão em camada Prata."),
            ("Left join com nulos",
             "`df.join(cat, 'StockCode', 'left')` — linhas da esquerda sem match ficam com "
             "`categoria` nula. Conte com `filter(col('categoria').isNull()).count()`."),
            ("Faixa",
             "```python\n.withColumn('faixa', when(col('receita_linha') < 50, 'baixa').when(col('receita_linha') < 200, 'media').otherwise('alta'))\n```"),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana3_dia4_window_udf_pandas_spark_connect",
    [
        header(
            "3", "4", "Window functions no Spark, UDFs (quando evitar) e pandas API",
            "Aplicar window functions na DataFrame API, entender o custo de UDFs Python e "
            "conhecer a pandas API on Spark + Spark Connect (Spark Dev 2026).",
            "DEA (Spark SQL), Spark Dev Assoc", "Exercícios de window + pandas API",
            "✅ Free Edition",
        ),
        teoria(
            "Window no Spark",
            "Na DataFrame API, use `Window.partitionBy(...).orderBy(...)`:\n\n"
            "```python\nfrom pyspark.sql.window import Window\nw = Window.partitionBy('pais').orderBy(col('receita').desc())\ndf.withColumn('rn', row_number().over(w))\n```\n\n"
            "Mesmos conceitos do SQL: PARTITION BY fatia, ORDER BY ordena dentro da fatia.",
        ),
        teoria(
            "UDFs Python: quando (não) usar",
            "UDF Python roda a função **linha a linha** fora do motor (serialização + Python) — "
            "10–100x mais lento que expressões nativas.\n\n"
            "**Regra de decisão**:\n"
            "1. Existe função nativa (built-in) ou SQL? → use.\n"
            "2. Precisa de lógica complexa não nativa? → tente `when/otherwise`, depois UDF.\n"
            "3. Só use UDF se não houver alternativa; marque com `@udf(returnType=...)`.\n"
            "4. Para pandas: use **pandas UDF (Vectorized UDF)** — roda por lote, muito mais rápido.",
        ),
        teoria(
            "pandas API on Spark e Spark Connect",
            "A **pandas API on Spark** (`pyspark.pandas`) permite escrever código estilo pandas "
            "rodando distribuído — excelente para quem vem do pandas.\n\n"
            "**Spark Connect** (2024+) separa cliente do servidor: seu código Python fala com "
            "o cluster via gRPC. É o futuro da API e cai na prova **Spark Developer Associate "
            "2026** (peso aumentado).",
        ),
        pratica("Window na prática",
            "Ranking de produtos por país e delta mês a mês."),
        code('# Window: top produtos por país\n'
             'from pyspark.sql.functions import row_number, rank, lag, sum as s\n'
             'from pyspark.sql.window import Window\n'
             'vendas_prod = (spark.table("workspace.bronze.vendas_bronze")\n'
             '    .groupBy("Country", "StockCode")\n'
             '    .agg(s("Quantity").alias("qtd")))\n'
             'w = Window.partitionBy("Country").orderBy(col("qtd").desc())\n'
             'top = vendas_prod.withColumn("rn", row_number().over(w)).filter("rn <= 3")\n'
             'top.show(9)'),
        code('# Running total por país\n'
             'rec_mes = (spark.table("workspace.bronze.vendas_bronze")\n'
             '    .withColumn("mes", to_date("InvoiceDate", "M/d/yyyy H:mm"))\n'
             '    .groupBy("Country", "mes").agg(s("Quantity*UnitPrice").alias("receita")))\n'
             'w2 = Window.partitionBy("Country").orderBy("mes").rowsBetween(Window.unboundedPreceding, Window.currentRow)\n'
             'rec_mes.withColumn("acumulado", s("receita").over(w2)).show(8)'),
        pratica("UDF vs nativa — o teste",
            "Compare o tempo de uma expressão nativa vs uma UDF Python."),
        code('# Expressão nativa (rápida)\n'
             'import time\n'
             'df = spark.table("workspace.bronze.vendas_bronze")\n'
             't0 = time.time()\n'
             'nativo = df.withColumn("receita_linha", col("Quantity") * col("UnitPrice")).count()\n'
             't1 = time.time()\n'
             'print(f"Nativo: {nativo} linhas em {t1-t0:.2f}s")'),
        code('# UDF Python (lenta) — para comparar\n'
             'from pyspark.sql.functions import udf\n'
             'from pyspark.sql.types import DoubleType\n'
             'import time\n'
             '@udf(returnType=DoubleType())\n'
             'def receita_udf(q, p):\n'
             '    return q * p\n'
             't0 = time.time()\n'
             'u = df.withColumn("receita_linha", receita_udf(col("Quantity"), col("UnitPrice"))).count()\n'
             't1 = time.time()\n'
             'print(f"UDF: {u} linhas em {t1-t0:.2f}s (geralmente 5-50x mais lento)")'),
        pratica("pandas API on Spark",
            "Use a API pandas distribuída para operações familiares."),
        code('# pandas API on Spark (exemplo)\n'
             'import pyspark.pandas as ps\n'
             'dfp = df[["Country", "Quantity", "UnitPrice"]]\\\n'
             '    .to_pandas_on_spark()\n'
             'print(dfp.groupby("Country")["Quantity"].sum().sort_values(ascending=False).head(5))'),
        dica_prova("Spark Connect e pandas API on Spark ganharam peso na **Spark Developer "
                   "Associate** (2026). No DEA, saber que UDFs são mais lentas e que "
                   "vectorized UDF existe é suficiente."),
        exercicios([
            "Use `rank()` e `dense_rank()` e mostre a diferença com empate.",
            "Reescreva a UDF `receita_udf` sem UDF (só com col).",
            "Conte quantos produtos são top-1 em mais de um país (com window).",
        ]),
        gabarito([
            ("rank vs dense_rank",
             "Com qtd (10,10,9): rank → 1,1,3; dense_rank → 1,1,2. Mesma lógica do SQL."),
            ("Sem UDF",
             "`df.withColumn('receita_linha', col('Quantity') * col('UnitPrice'))` — nativa, "
             "otimizada pelo Catalyst."),
            ("Top-1 em vários países",
             "```python\nw = Window.partitionBy('Country').orderBy(col('qtd').desc())\ntop1 = vendas_prod.withColumn('rn', row_number().over(w)).filter('rn = 1')\ntop1.groupBy('StockCode').count().filter('count > 1')\n```"),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana3_dia5_internals_shuffle_cache_plano_fisico",
    [
        header(
            "3", "5", "Internals: partições, shuffle, cache e o Spark UI",
            "Entender partições, shuffle, broadcast vs sort-merge join, cache/persist e ler o "
            "plano físico — a base do tuning (Semana 8).",
            "DEP (performance)", "Análise do Spark UI de um job real",
            "✅ Free Edition",
        ),
        teoria(
            "Partições e paralelismo",
            "Cada arquivo/tabela é lido em **partições**. O paralelismo = número de tasks "
            "simultâneas ≈ número de partições ativas × cores. Poucas partições = subutilização; "
            "muitas = overhead.\n\n"
            "`spark.sql.shuffle.partitions` (padrão 200) define o nº de partições após um "
            "shuffle (groupBy/join). Ajuste com bom senso — a Semana 8 aprofunda.",
        ),
        teoria(
            "Shuffle — o custo do movimento",
            "Quando um `groupBy` ou `join` precisa juntar linhas que estão em partições "
            "diferentes, o Spark **embaralha** os dados pela rede (shuffle): grava em disco, "
            "move, reordena. **Shuffle é o operador mais caro do Spark.**\n\n"
            "**Broadcast join**: se uma tabela é pequena (< 10 MB por padrão), o Spark a copia "
            "para cada executor e faz join sem shuffle — muito mais rápido.\n\n"
            "> 🎯 **Dica de prova (DEP)**: escolher entre broadcast join (tabela pequena) e "
            "sort-merge join (tabelas grandes, shuffle) é pergunta clássica. O broadcast é "
            "automático até o limite, mas pode ser forçado com hint.",
        ),
        teoria(
            "cache() vs persist()",
            "Ambos guardam o DataFrame em memória para **reutilização** (evita recalcular).\n"
            "- `cache()` = `persist(MEMORY_AND_DISK)`.\n"
            "- `persist(level)` permite escolher: DISK_ONLY, MEMORY_ONLY, etc.\n"
            "- São **lazy**: só materializam na primeira ação.\n"
            "- Use em dados **reutilizados várias vezes**; em dados de 1 uso, cache é desperdício.\n"
            "- Para desfazer: `df.unpersist()`.",
        ),
        pratica("Plano físico e Spark UI",
            "Gere um job e observe o plano físico."),
        code('# Forçar um broadcast join para ver no plano físico\n'
             'categorias = spark.createDataFrame([("85123A","Decoração"), ("71053","Cozinha")], ["StockCode", "cat"])\n'
             'df = spark.table("workspace.bronze.vendas_bronze").limit(50_000)\n'
             'j = df.join(categorias, "StockCode", "left")\n'
             'print(j.explain("formatted"))  # veja o BroadcastExchange no plano\n'
             'print("Se vir BroadcastExchange, o Spark fez broadcast (sem shuffle).")'),
        code('# Shuffle real: groupBy\n'
             'g = spark.table("workspace.bronze.vendas_bronze").groupBy("Country").count()\n'
             'print(g.explain("formatted"))  # veja Exchange (shuffle) no plano\n'
             'g.collect()'),
        code('# cache: reutilizar sem recalcular\n'
             'import time\n'
             'df_ouro = spark.table("workspace.bronze.vendas_bronze").filter("Quantity > 5")\n'
             'df_ouro.cache()\n'
             't0 = time.time(); df_ouro.count(); t1 = time.time()\n'
             'print(f"1a contagem (carrega cache): {t1-t0:.2f}s")\n'
             't0 = time.time(); df_ouro.count(); t1 = time.time()\n'
             'print(f"2a contagem (do cache): {t1-t0:.2f}s")\n'
             'df_ouro.unpersist()'),
        dica_prova("O Spark UI (abas Query/Jobs) mostra: DAG, estágios, tasks, tempos e "
                   "skew. Saber ler 'shuffle read/write' e 'task time vs duration' diferencia "
                   "sênior de júnior em entrevistas."),
        exercicios([
            "Explique em 2 frases o que é shuffle e por que é caro.",
            "Quando o Spark usa broadcast join automaticamente? Como forçar?",
            "Diferencie cache() de persist(DISK_ONLY).",
            "Rode um join e veja no explain se foi broadcast ou sort-merge.",
        ]),
        gabarito([
            ("Shuffle",
             "Movimentação de linhas entre partições para satisfazer groupBy/join; envolve disco "
             "+ rede, sendo o operador mais caro. Evitar shuffle é a 1ª regra de tuning."),
            ("Broadcast",
             "Quando uma das tabelas é pequena (< spark.sql.autoBroadcastJoinThreshold, 10MB). "
             "Forçar: `df.join(cat.hint('broadcast'), 'key')`."),
            ("cache vs persist",
             "cache() = MEMORY_AND_DISK. persist() aceita outros níveis (DISK_ONLY, MEMORY_ONLY...). "
             "Ambos são lazy e liberados com unpersist()."),
            ("Explain",
             "Procure `BroadcastExchange` (broadcast) vs `Exchange` + `SortMergeJoin` (shuffle)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana3_dia6_pipeline_limpeza_simulado_spark",
    [
        header(
            "3", "6", "Pipeline de limpeza + simulado parcial DEA (Spark)",
            "Entregar um pipeline Python de limpeza completo e validar com um simulado parcial "
            "do domínio Spark da DEA.",
            "DEA (Spark)", "Pipeline de limpeza rodando + simulado ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "O entregável: pipeline de limpeza (Bronze → pré-Prata)",
            "Vamos consolidar a semana em um pipeline idempotente de limpeza — ele será a base "
            "da camada Prata na Semana 4.\n\n"
            "**Idempotente** = rodar 2x dá o mesmo resultado. Regra de ouro da Prata.",
        ),
        pratica("Pipeline completo",
            "Rode de ponta a ponta: leitura → limpeza → enriquecimento → escrita."),
        code('# 1) Ler Bronze\n'
             'from pyspark.sql.functions import col, when, to_timestamp, upper, round as r, trim\n'
             'df = spark.table("workspace.bronze.vendas_bronze")\n'
             'print("Bronze:", df.count())'),
        code('# 2) Limpeza: nulos, duplicatas, tipos, regras de negócio\n'
             'df_limpo = (df\n'
             '    .filter(col("CustomerID").isNotNull())\n'
             '    .withColumn("Description", trim(col("Description")))\n'
             '    .withColumn("Country", upper(trim(col("Country"))))\n'
             '    .dropDuplicates(["InvoiceNo", "StockCode", "InvoiceDate"])\n'
             '    .filter("Quantity > 0 AND UnitPrice > 0")\n'
             '    .withColumn("receita_linha", r(col("Quantity") * col("UnitPrice"), 2))\n'
             '    .withColumn("faixa",\n'
             '        when(col("receita_linha") < 20, "baixa")\n'
             '        .when(col("receita_linha") < 100, "media")\n'
             '        .otherwise("alta")))\n'
             'print("Após limpeza:", df_limpo.count())'),
        code('# 3) Auditoria rápida (as 6 dimensões)\n'
             'print("Nulos restantes por coluna:")\n'
             'df_limpo.select([count(isnull(c)).alias(c) for c in ["CustomerID", "Description"]]).show()\n'
             'print("Receita total:", df_limpo.agg(s("receita_linha")).collect()[0][0])'),
        code('# 4) Gravar como tabela pré-Prata (idempotente)\n'
             'spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.prata")\n'
             'df_limpo.write.mode("overwrite").saveAsTable("workspace.prata.vendas_preprata")\n'
             'print("Pré-Prata gravada:", spark.table("workspace.prata.vendas_preprata").count())'),
        pratica("Simulado parcial — domínio Spark (10 questões)",
            "Responda antes de ver o gabarito."),
        md("""### Questões Spark

**1.** Qual é a diferença entre transformação e ação?
- A) transformação roda imediato; ação é lazy
- B) transformação é lazy; ação dispara execução
- C) iguais
- D) ação só funciona em RDD

**2.** Onde as tasks rodam?
- A) no driver  B) nos executores, sobre partições  C) no metastore  D) no SQL Warehouse

**3.** Qual operador é o mais caro?
- A) select  B) filter  C) shuffle  D) withColumn

**4.** Quando o broadcast join é aplicado automaticamente?
- A) sempre  B) quando a tabela é pequena (< threshold)  C) quando há índices  D) nunca

**5.** `df.cache()` materializa quando?
- A) na chamada  B) na primeira ação  C) no collect  D) nunca

**6.** Qual é a forma correta de criar coluna condicional?
- A) `df['col'] = ...`  B) `withColumn` + `when`  C) UDF obrigatório  D) `addColumn`

**7.** Qual comando lê um JSON com schema?
- A) `spark.read.schema(s).json(path)`  B) `spark.read.json(s)`  C) `spark.json(s)`  D) `LOAD`

**8.** O que `left anti` retorna?
- A) linhas da esquerda com match  B) linhas da esquerda SEM match  C) todas  D) nulas

**9.** Qual API é recomendada para lógica pandas distribuída?
- A) RDD  B) pandas API on Spark  C) UDF Python  D) SQL puro

**10.** O que o Spark UI mostra?
- A) DAG, estágios, tasks e tempos  B) apenas o schema  C) apenas custos  D) nada em serverless
"""),
        teoria(
            "Gabarito — Simulado Spark",
            "**1-B** · **2-B** · **3-C** · **4-B** · **5-B** · **6-B** · **7-A** · "
            "**8-B** · **9-B** · **10-A**.\n\n"
            "≥ 7 acertos = pronto para a Semana 4. Se errou shuffle/broadcast, revise o Dia 5.",
        ),
        dica_prova("Lazy evaluation + ações + shuffle + broadcast é o 'quarteto' de performance "
                   "que aparece em toda prova Spark/DEA. Decore o quarteto."),
        exercicios([
            "Explique por que o pipeline acima é idempotente.",
            "O que aconteceria se rodássemos sem `mode('overwrite')` a segunda vez?",
        ]),
        gabarito([
            ("Idempotente",
             "Porque recria a tabela do zero (overwrite) a partir da mesma fonte — o resultado "
             "final é sempre o mesmo, independente de quantas vezes rodar."),
            ("Sem overwrite",
             "Falha por 'table already exists' (ou acumularia duplicatas com append). "
             "Idempotência exige overwrite ou merge."),
        ]),
        footer([
            "Rodei todos os 6 notebooks da Semana 3.",
            "Expliquei lazy evaluation e DAG em 2 frases.",
            "Sei quando usar broadcast join e o que é shuffle.",
            "Fiz o simulado Spark e revisei os erros.",
        ]),
    ],
))
