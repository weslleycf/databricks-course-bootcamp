"""Semana 1 — Plataforma, Lakehouse e primeiros dados (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana1_dia1_conta_free_edition_tour_ui",
    [
        header(
            "1", "1", "Conta Free Edition, Tour da Interface e Primeiro Notebook",
            "Criar a conta Databricks Free Edition (sucessora da Community Edition), entender o "
            "ambiente serverless e rodar o primeiro código com os comandos mágicos.",
            "DEA (fundações da plataforma)", "Conta criada + notebook `00_bem_vindo` rodando",
            "✅ Free Edition",
            dais="AI Assistant integrado na UI para escrever e corrigir código.",
        ),
        teoria(
            "A nova Databricks Free Edition",
            "Até meados de 2025, a Databricks oferecia a *Community Edition* para quem queria "
            "estudar sem pagar. Ela foi aposentada em junho de 2025 e substituída pela "
            "**Free Edition**: um workspace real na nuvem, com **compute serverless** "
            "(você não configura máquinas — a plataforma provisiona e escala sozinha) e acesso "
            "à maioria dos produtos: Unity Catalog, Delta Lake, SQL, Lakeflow, Apps e Mosaic AI.\n\n"
            "**Limitações importantes da Free Edition** (que vamos respeitar o curso todo):\n"
            "- Uso **não comercial**, sem SLA e sem suporte dedicado.\n"
            "- 1 SQL Warehouse (tamanho 2X-Small).\n"
            "- Máx. 5 jobs/tarefas concorrentes e **1 pipeline Lakeflow ativo por tipo**.\n"
            "- Até 3 Databricks Apps (com auto-stop após 24h) e **1 projeto Lakebase**.\n"
            "- Model Serving limitado: sem GPU, sem throughput provisionado, alguns modelos indisponíveis.\n"
            "- Internet de saída restrita a domínios confiáveis (verificação via LinkedIn libera GPU "
            "limitada e acesso a mais domínios).\n"
            "- Sem R/Scala, sem external locations, sem account console, sem SSO/SCIM.\n"
            "- Contas inativas por muito tempo podem ser excluídas — **use o workspace toda semana**.\n\n"
            "> 💡 **Analogia**: a Free Edition é como um carro de luxo de demonstração: você "
            "dirige tudo de verdade, mas com um tanque pequeno e sem sair do estacionamento do "
            "concessionário. Para o estudo é perfeita — e 85% do que um especialista faz cabe nela.",
        ),
        pratica(
            "Criando a conta",
            "1. Acesse https://www.databricks.com/try-databricks e clique em **Get Started** com "
            "**Free Edition**.\n"
            "2. Cadastre-se com e-mail (OTP), Google ou Microsoft (não há SSO/SCIM na Free).\n"
            "3. Confirme o e-mail. O workspace é criado em poucos minutos.\n"
            "4. **Anote o URL do workspace** (formato `dbc-xxxx.cloud.databricks.com`) e a senha.\n\n"
            "> ⚠️ A Free Edition pode pedir verificação de identidade via **LinkedIn** para liberar "
            "limites extras (GPU, internet). É opcional, mas recomendado.",
        ),
        teoria(
            "O tour da interface",
            "**Sidebar esquerda** (navegação principal):\n"
            "- **Home**: atalhos para notebooks, queries e dashboards recentes.\n"
            "- **Workspace**: onde ficam notebooks e pastas (equivalentes a arquivos).\n"
            "- **Data**: Unity Catalog — catálogos, schemas, tabelas, volumes, funções e modelos.\n"
            "- **Compute**: SQL Warehouses e computação (na Free, serverless).\n"
            "- **Jobs**: orquestração de pipelines (Lakeflow Jobs).\n"
            "- **Experiments / Models**: MLflow.\n"
            "- **Apps / Lakebase**: publicar aplicações e criar projetos transacionais.\n"
            "- **AI**: Playground, Mosaic AI, Vector Search, agentes.\n"
            "- **Search**: busca global (Ctrl+K).",
        ),
        teoria(
            "Notebooks e comandos mágicos",
            "O notebook é dividido em **células**. Cada célula roda em uma linguagem definida por um "
            "**comando mágico** no topo da célula:\n\n"
            "| Comando | Linguagem / efeito |\n|---|---|\n"
            "| `%python` | Python (padrão) |\n"
            "| `%sql` | Spark SQL |\n"
            "| `%md` | Markdown (documentação) |\n"
            "| `%sh` | Shell no nó do driver |\n"
            "| `%fs` | Comandos de arquivos (ex.: `%fs ls`) |\n"
            "| `%scala` / `%r` | Scala / R (⚠️ não disponíveis na Free Edition) |\n\n"
            "> 🎯 **Dica de prova (DEA)**: a prova cobra a diferença entre `%sql`, `%python` e `%md`, "
            "e o fato de que células SQL compartilham o mesmo catálogo do notebook. O comando `%fs` "
            "acessa o sistema de arquivos, não o catálogo.",
        ),
        pratica("Primeiro código",
            "Rode a célula abaixo com **Shift+Enter**. Em notebooks Databricks, `spark` já existe "
            "como uma variável global — você não precisa criá-la."),
        code('# Célula Python — primeiro contato com o ambiente\n'
             'print("Bem-vindo(a) ao curso Especialista Databricks!")\n'
             'print("Versão do Spark:", spark.version)\n'
             'print("Versão do Databricks Runtime:", spark.conf.get("spark.databricks.clusterUsageTags.sparkVersion"))'),
        pratica("SQL no notebook",
            "Células SQL rodam no mesmo catálogo do notebook. Experimente:"),
        sql('SELECT 1 + 1 AS soma, current_date() AS hoje'),
        pratica("Markdown e documentação",
            "Use `%md` para documentar — anotações, diagramas ASCII, checklists. Um notebook bem "
            "documentado vale ouro em equipes (e em entrevistas, mostrando comunicação)."),
        md('%md\n'
           '### 📝 Anotações do Dia 1\n\n'
           '- [x] Conta Free Edition criada\n'
           '- [x] Tour pela interface concluído\n'
           '- [ ] Primeiro notebook rodando (falta validar)\n'),
        dica_prova("Na Free Edition, notebooks rodam em **compute serverless** — você não cria "
                   "clusters como na versão clássica. A prova DEA 2026 cobra serverless como conceito "
                   "e as diferenças para clusters clássicos."),
        exercicios([
            "Qual a diferença entre a antiga Community Edition e a nova Free Edition?",
            "Quais são 3 limitações da Free Edition que afetam o plano de estudo?",
            "Cite 3 comandos mágicos e o que cada um faz.",
            "O que a verificação via LinkedIn libera na Free Edition?",
        ]),
        gabarito([
            ("Community Edition x Free Edition",
             "A CE foi aposentada em junho/2025. A FE é serverless-only, com quotas (1 SQL "
             "warehouse 2X-Small, 5 jobs concorrentes, 1 pipeline Lakeflow ativo por tipo, 3 Apps, "
             "1 Lakebase, model serving sem GPU) e sem R/Scala, sem external locations, sem account "
             "console e sem SSO/SCIM."),
            ("3 limitações",
             "Ex.: 1 pipeline Lakeflow ativo por tipo; máx. 5 jobs concorrentes; model serving sem "
             "GPU/provisioned throughput; até 3 Apps com auto-stop 24h; internet de saída restrita."),
            ("Comandos mágicos",
             "`%sql` roda Spark SQL; `%python` roda Python; `%md` insere Markdown; `%fs` acessa o "
             "sistema de arquivos; `%sh` roda shell. `%scala`/`%r` não existem na Free Edition."),
            ("LinkedIn verification",
             "Libera acesso a GPU serverless limitada e internet de saída mais ampla — útil nas "
             "semanas de fine-tuning e integrações."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana1_dia2_lakehouse_unity_catalog_volumes",
    [
        header(
            "1", "2", "Arquitetura Lakehouse, Unity Catalog e Volumes",
            "Entender por que o Lakehouse existe, a governança em 3 níveis do Unity Catalog e "
            "a diferença entre DBFS e Volumes.",
            "DEA (arquitetura + UC)", "Diagrama mental da arquitetura + notas no caderno",
            "✅ Free Edition",
        ),
        teoria(
            "Por que Lakehouse?",
            "**Data Warehouse** (anos 90): excelente para SQL e BI, mas caro, proprietário e péssimo "
            "para IA/ML.\n"
            "**Data Lake** (anos 2010): barato, escala, lê qualquer formato — mas vira um *pântano de "
            "dados* (data swamp): sem transações, sem consistência, sem governança.\n\n"
            "**Lakehouse** (Databricks, 2020) = a união dos dois: dados abertos (Parquet/Delta) em "
            "armazenamento barato, com **transações ACID**, versionamento e governança de warehouse, "
            "e motores para SQL, Python, R e IA no mesmo dado.\n\n"
            "**As 7 características do Lakehouse**:\n"
            "1. Transações ACID (Atomicidade, Consistência, Isolamento, Durabilidade)\n"
            "2. Schema enforcement e evolução\n"
            "3. Dados abertos e acessíveis (Parquet/Delta, sem lock-in)\n"
            "4. Suporte a BI direto na fonte\n"
            "5. Storage separado do compute (S3/ADLS/GCS + clusters)\n"
            "6. Versionamento de dados (Time Travel)\n"
            "7. Governança unificada (Unity Catalog)",
        ),
        teoria(
            "Unity Catalog — governança em 3 níveis",
            "O **Unity Catalog (UC)** é a camada de governança que organiza TUDO o que existe no "
            "workspace em um **namespace de 3 níveis**:\n\n"
            "```\ncatálogo.schema.objeto\n\nworkspace.bronze.vendas_bronze\n```\n\n"
            "| Nível | Exemplo | O que guarda |\n|---|---|---|\n"
            "| Catálogo | `workspace` | Agrupamento máximo (metastore); `workspace` é o padrão da Free Edition |\n"
            "| Schema | `bronze`, `prata`, `ouro` | Agrupamento lógico de objetos relacionados |\n"
            "| Objeto | `vendas_bronze` | Tabela, view, volume, função, modelo, ... |\n\n"
            "> 🎯 **Dica de prova (DEA)**: em 2026 o Unity Catalog vale **~30% da prova**. A "
            "nomenclatura de 3 níveis (`catalog.schema.table`), permissões (GRANT/REVOKE), "
            "external locations e dynamic views são os tópicos mais cobrados. DBFS é legado — o "
            "recomendado é **Volumes**.",
        ),
        teoria(
            "DBFS vs Volumes",
            "**DBFS (Databricks File System)**: sistema de arquivos montado no cluster. Fácil para "
            "começar, mas é **legado** — difícil de governar e não escala para equipes.\n\n"
            "**Volumes (Unity Catalog)**: diretórios governados dentro do UC, com permissões, "
            "linhagem e controle de acesso. É o **padrão 2026** para armazenar arquivos "
            "(deltas, parquets, modelos, dados brutos).\n\n"
            "```\n/Volumes/catalogo/schema/volume/caminho/arquivo.csv\n```",
        ),
        pratica("Criando schemas do projeto (Medallion)",
            "Vamos criar a estrutura de pastas lógica do projeto — os 3 schemas da arquitetura "
            "Medallion (Bronze → Prata → Ouro). Isso prepara o terreno para os próximos dias."),
        sql('-- Criação dos schemas da arquitetura Medallion\n'
            'CREATE SCHEMA IF NOT EXISTS workspace.bronze;\n'
            'CREATE SCHEMA IF NOT EXISTS workspace.prata;\n'
            'CREATE SCHEMA IF NOT EXISTS workspace.ouro;\n'
            'SHOW SCHEMAS IN workspace'),
        pratica("Volumes na prática",
            "Crie um volume gerenciado para guardar arquivos brutos do curso (dados do projeto)."),
        sql('CREATE VOLUME IF NOT EXISTS workspace.bronze.vol_dados_curso;\n'
            'SHOW VOLUMES IN workspace.bronze'),
        code('# O caminho de um volume montado é acessível do Python assim:\n'
             'print("/Volumes/workspace/bronze/vol_dados_curso")\n'
             'display(spark.sql("SHOW VOLUMES IN workspace.bronze"))'),
        dica_prova("A prova DEA distingue **managed tables** (gerenciadas pelo UC, criadas com "
                   "`CREATE TABLE`) de **external tables** (apontam para storage fora do UC, exigem "
                   "external location — que não existe na Free Edition). Memorize essa diferença."),
        exercicios([
            "Explique em 3 frases por que o Lakehouse supera warehouse e data lake.",
            "Escreva o namespace de 3 níveis da tabela que criaremos: vendas no schema bronze do catálogo workspace.",
            "Qual a diferença entre managed e external table?",
            "Por que Volumes são o padrão 2026 e não DBFS?",
        ]),
        gabarito([
            ("Lakehouse",
             "Une a abertura e o custo baixo do data lake com ACID, versionamento e governança do "
             "warehouse, num único motor para SQL, Python e IA."),
            ("Namespace",
             "`workspace.bronze.vendas_bronze` (catálogo.schema.objeto)."),
            ("Managed vs external",
             "Managed: o UC gerencia o armazenamento e o ciclo de vida (DROP apaga dados). External: "
             "aponta para storage próprio (S3/ADLS/GCS) via external location; DROP não apaga os "
             "arquivos. Na Free Edition só temos managed."),
            ("Volumes vs DBFS",
             "Volumes são governados pelo UC (permissões, linhagem, auditoria) e acessíveis em "
             "qualquer compute; DBFS é legado, sem governança fina e com acesso dependente do cluster."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana1_dia3_datasets_formatos_arquivos",
    [
        header(
            "1", "3", "Datasets do projeto e os 4 formatos de arquivo",
            "Carregar os dados do projeto (vendas de varejo) e dominar leitura/escrita de "
            "CSV, JSON, Parquet e Delta com inspeção de schema.",
            "DEA (formatos de dados)", "Dados do projeto lidos em 4 formatos + inspeção",
            "✅ Free Edition",
        ),
        teoria(
            "O projeto do curso: vendas de varejo",
            "Você é engenheiro(a) de dados de uma rede de varejo com múltiplas lojas. Os dados "
            "chegam em **CSV** (vendas), **JSON** (clientes) e feeds de catálogo. Nas próximas "
            "semanas você vai construir a plataforma completa: Bronze → Prata → Ouro, dashboards, "
            "um modelo de previsão, um RAG e um agente que responde perguntas sobre as vendas.\n\n"
            "Usaremos o dataset oficial de exemplo do Databricks — **Online Retail** "
            "(~540 mil linhas de vendas de uma loja online do Reino Unido, dez/2010–dez/2011) — "
            "que já vem disponível no workspace (`samples.databricks.datasets` / "
            "`/databricks-datasets`), com espelho no GitHub oficial e na UCI "
            "(archive.ics.uci.edu/dataset/352/online+retail). Também geramos dados "
            "sintéticos de voos para enriquecimento.",
        ),
        teoria(
            "Os 4 formatos que você precisa dominar",
            "| Formato | Uso típico | Quando usar |\n|---|---|---|\n"
            "| **CSV** | Exportações, sistemas legados | Leitura rápida; sem schema |\n"
            "| **JSON** | APIs, logs, eventos | Semianinhado, flexível |\n"
            "| **Parquet** | Analítico, colunar, comprimido | Grande volume, schema forte |\n"
            "| **Delta** | Tabelas transacionais (ACID) | **Sempre para produção** — base do Lakehouse |\n\n"
            "**Parquet vs CSV**: Parquet é **colunar** (lê só as colunas necessárias), comprime "
            "75–90% e guarda o **schema** no arquivo. CSV é linha a linha e sem schema.",
        ),
        pratica("Carregando o dataset",
            "O Databricks já fornece o dataset **Online Retail** no workspace. Vamos usar, "
            "em ordem: (1) o dataset local do Databricks (sem internet, recomendado na "
            "Free Edition), (2) o raw do GitHub oficial do Databricks, (3) upload manual.\n\n"
            "> 💾 **Destino dos arquivos**: usaremos o **Volume `vol_dados_curso`** "
            "(criado no Dia 2) — `/Volumes/workspace/bronze/vol_dados_curso/` — como área de "
            "trabalho do curso. Ele é governado pelo Unity Catalog e acessível em qualquer "
            "compute. Na Free Edition, o filesystem local (`/tmp`) é restrito, então "
            "**não** usamos `/tmp`."),
        code('# 1) Dataset local do Databricks (funciona onde há sample datasets)\n'
             'destino = "/Volumes/workspace/bronze/vol_dados_curso/vendas.csv"\n'
             'caminhos = [\n'
             '    "/databricks-datasets/online-retail-dataset/data-original/online-retail-dataset.csv",\n'
             '    "/Volumes/samples/databricks/datasets/online_retail/online_retail.csv",\n'
             ']\n'
             'encontrado = None\n'
             'for p in caminhos:\n'
             '    try:\n'
             '        dbutils.fs.head(p)  # só funciona se o ARQUIVO existir\n'
             '        encontrado = p\n'
             '        break\n'
             '    except Exception:\n'
             '        continue\n'
             'if encontrado:\n'
             '    dbutils.fs.cp(encontrado, destino)\n'
             '    print("Usado dataset local do Databricks:", encontrado)\n'
             'else:\n'
             '    print("Dataset local não encontrado nesta conta — tente o GitHub (próxima célula).")'),
        code('# 2) Fallback: raw do GitHub oficial do Databricks (se internet liberada)\n'
             'import urllib.request\n'
             'url = "https://raw.githubusercontent.com/databricks/Spark-The-Definitive-Guide/master/data/retail-data/all/online-retail-dataset.csv"\n'
             'try:\n'
             '    with urllib.request.urlopen(url, timeout=60) as r:\n'
             '        conteudo = r.read()\n'
             '    # dbutils.fs.put grava direto no Volume a partir da memória —\n'
             '    # sem usar o filesystem local (que é restrito na Free Edition)\n'
             '    dbutils.fs.put(destino, conteudo.decode("utf-8"), overwrite=True)\n'
             '    print("Download OK (GitHub oficial)! Tamanho:", len(conteudo), "bytes")\n'
             'except Exception as e:\n'
             '    print("Fallback GitHub falhou:", str(e)[:120])\n'
             '    print("Siga o upload manual na próxima célula.")'),
        code('# 3) Verificação: o arquivo está no Volume?\n'
             'try:\n'
             '    dbutils.fs.head(destino)\n'
             '    print("OK — vendas.csv pronto no Volume:", destino)\n'
             'except Exception:\n'
             '    print("ARQUIVO AINDA NÃO ESTÁ NO VOLUME. Faça o upload manual:")\n'
             '    print("1. Baixe o CSV: https://raw.githubusercontent.com/databricks/Spark-The-Definitive-Guide/master/data/retail-data/all/online-retail-dataset.csv")\n'
             '    print("2. No Databricks: Data > Add Data > Upload File")\n'
             '    print("3. Destino: Volumes > workspace > bronze > vol_dados_curso")\n'
             '    print("4. Rode esta célula de novo para confirmar.")'),
        code('# Conferir o arquivo no Volume\n'
             'display(dbutils.fs.ls("/Volumes/workspace/bronze/vol_dados_curso/"))'),
        pratica("Leitura com Spark",
            "O Spark infere o schema automaticamente. Sempre **confira o schema** antes de usar "
            "os dados — é a fonte de 80% dos bugs em pipelines."),
        code('# Ler CSV com inferência de schema\n'
             'df_vendas = (spark.read\n'
             '    .format("csv")\n'
             '    .option("header", True)\n'
             '    .option("inferSchema", True)\n'
             '    .option("multiLine", True)\n'
             '    .load(destino))\n'
             'df_vendas.printSchema()\n'
             'df_vendas.show(5, truncate=False)\n'
             'print("Total de linhas:", df_vendas.count())'),
        pratica("Inspeção e estatísticas",
            "`describe` dá estatísticas básicas (min/max/avg). Cuidado: strings viram stats estranhas; "
            "aplique em colunas numéricas."),
        code('# Estatísticas descritivas\n'
             'df_vendas.describe("Quantity", "UnitPrice").show()\n'
             '# Contagem de nulos por coluna (base da qualidade de dados)\n'
             'from pyspark.sql.functions import col, isnan, isnull, count\n'
             'df_vendas.select([count(isnull(c)).alias(f"nulos_{c}") for c in df_vendas.columns]).show()'),
        pratica("Gravando nos 4 formatos",
            "Vamos gravar a mesma base em CSV (cópia), JSON, Parquet e Delta e comparar. "
            "Usamos o **Volume** como destino (área governada e persistente)."),
        code('# Gravar nos 4 formatos (no Volume do curso)\n'
             'df_vendas.write.mode("overwrite").parquet("/Volumes/workspace/bronze/vol_dados_curso/vendas.parquet")\n'
             'df_vendas.write.mode("overwrite").json("/Volumes/workspace/bronze/vol_dados_curso/vendas.json")\n'
             'df_vendas.write.mode("overwrite").format("delta").save("/Volumes/workspace/bronze/vol_dados_curso/vendas_delta")\n'
             'print("Parquet, JSON e Delta gravados no Volume vol_dados_curso")'),
        code('# Comparar leitura de volta e tamanho\n'
             'df_p = spark.read.parquet("/Volumes/workspace/bronze/vol_dados_curso/vendas.parquet")\n'
             'df_j = spark.read.json("/Volumes/workspace/bronze/vol_dados_curso/vendas.json")\n'
             'df_d = spark.read.format("delta").load("/Volumes/workspace/bronze/vol_dados_curso/vendas_delta")\n'
             'print("Parquet:", df_p.count(), "| JSON:", df_j.count(), "| Delta:", df_d.count())\n'
             'display(spark.sql("SELECT COUNT(*) AS linhas FROM delta.`/Volumes/workspace/bronze/vol_dados_curso/vendas_delta`"))'),
        dica_prova("A prova DEA pergunta **quando usar cada formato** e o motivo de Parquet/Delta "
                   "serem superiores ao CSV (colunar, compressão, schema embutido, ACID). "
                   "Decore a tabela dos formatos."),
        exercicios([
            "Leia o JSON e mostre as 3 primeiras linhas.",
            "Quantas linhas tem o JSON vs o Parquet? Por quê?",
            "Crie uma view temporária `vendas_vw` a partir do DataFrame lido.",
            "Qual formato escolheria para uma tabela de produção que recebe updates frequentes? Por quê?",
        ]),
        gabarito([
            ("Ler JSON",
             "`spark.read.json('/Volumes/workspace/bronze/vol_dados_curso/vendas.json').show(3, truncate=False)`."),
            ("JSON vs Parquet",
             "O JSON gravado aqui contém o mesmo conjunto de linhas (a menos que o parquet tenha "
             "partições extras); a diferença real é o tamanho em disco e a velocidade: Parquet "
             "comprime por coluna e guarda schema. Em pipelines reais o JSON é bem maior e mais lento."),
            ("View temporária",
             "`df_vendas.createOrReplaceTempView('vendas_vw')` — a partir dela pode-se consultar com "
             "`%sql SELECT * FROM vendas_vw LIMIT 5`."),
            ("Delta",
             "Delta: ACID, Time Travel, MERGE, schema evolution — necessário para updates frequentes "
             "e consistência. CSV/JSON não têm transações."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana1_dia4_sql_warehouse_queries_views",
    [
        header(
            "1", "4", "SQL Warehouse, queries analíticas e views",
            "Usar o SQL Warehouse (2X-Small) para rodar queries analíticas, entender o papel das "
            "views temporárias e conectar Python ↔ SQL.",
            "DEA (SQL analítico)", "10 queries analíticas respondidas + ponte Python↔SQL",
            "✅ Free Edition",
        ),
        teoria(
            "SQL Warehouse (e por que a Free Edition tem 1)",
            "O **SQL Warehouse** é o compute especializado em SQL (otimizado para BI, dashboards e "
            "queries ad hoc). Na Free Edition você tem **1 warehouse de tamanho 2X-Small** — "
            "suficiente para o curso. Ele pode ser iniciado/parado manualmente; na Free, ele "
            "desliga sozinho após inatividade.\n\n"
            "**Diferença**: notebooks rodam no compute serverless de notebooks; queries SQL e "
            "dashboards rodam no SQL Warehouse. Ambos acessam o **mesmo Unity Catalog**.",
        ),
        pratica("Conectando no SQL Warehouse",
            "1. Em **Compute → SQL Warehouses**, crie um warehouse (2X-Small, auto-stop ~10 min).\n"
            "2. Abra **Queries** (ícone de banco de dados) para escrever SQL puro.\n"
            "3. Alternativamente, use células `%sql` no notebook — elas também rodam via Spark, "
            "mas para testar o warehouse de verdade, use o editor de Queries.",
        ),
        teoria(
            "Views temporárias — a ponte Python ↔ SQL",
            "Uma **view temporária** registra um DataFrame para ser consultado em SQL na mesma "
            "sessão. É a peça que conecta seu código Python com a consulta SQL — muito usado em "
            "pipelines e em perguntas de prova.\n\n"
            "```\ndf.createOrReplaceTempView('nome')\nspark.sql('SELECT ... FROM nome')\n```",
        ),
        code('# Ponte Python → SQL: registrar view e consultar\n'
             'df_vendas = spark.read.format("csv") \\\n'
             '    .option("header", True) \\\n'
             '    .option("inferSchema", True) \\\n'
             '    .load("/Volumes/workspace/bronze/vol_dados_curso/vendas.csv")\n'
             'df_vendas.createOrReplaceTempView("vendas_vw")\n'
             'print("View vendas_vw registrada. Total de linhas:", spark.sql("SELECT COUNT(*) FROM vendas_vw").collect()[0][0])'),
        sql('-- 1. Vendas por país (análise clássica)\n'
            'SELECT Country, COUNT(*) AS vendas\n'
            'FROM vendas_vw\n'
            'GROUP BY Country\n'
            'ORDER BY vendas DESC\n'
            'LIMIT 10'),
        code('# SQL → Python: trazer o resultado de volta\n'
             'resultado = spark.sql("""\n'
             '    SELECT SUM(Quantity * UnitPrice) AS receita_total\n'
             '    FROM vendas_vw\n'
             '""").collect()[0]["receita_total"]\n'
             'print(f"Receita total do dataset: {resultado:,.2f}")'),
        pratica("Queries analíticas essenciais",
            "Rode e analise cada uma. Esse padrão (GROUP BY + agregação + ORDER BY + LIMIT) é o "
            "coração de 90% dos dashboards."),
        sql('-- 2. Ticket médio por país\n'
            'SELECT Country, ROUND(AVG(Quantity * UnitPrice), 2) AS ticket_medio\n'
            'FROM vendas_vw\n'
            'GROUP BY Country\n'
            'ORDER BY ticket_medio DESC\n'
            'LIMIT 10'),
        sql('-- 3. Receita por mês (extração de data com DATE_TRUNC)\n'
            'SELECT DATE_TRUNC("month", InvoiceDate) AS mes, ROUND(SUM(Quantity * UnitPrice), 2) AS receita\n'
            'FROM vendas_vw\n'
            'GROUP BY mes\n'
            'ORDER BY mes\n'
            'LIMIT 12'),
        dica_prova("A prova DEA 2026 enfatiza **ELT com Spark SQL e Python**. Saber escrever "
                   "agregações, CTEs, window functions e conectar Python↔SQL via views é o "
                   "núcleo do domínio 1 da prova."),
        exercicios([
            "Qual a receita total do Reino Unido (United Kingdom)?",
            "Quantos clientes únicos (CustomerID não nulo) existem?",
            "Qual o dia com mais vendas do dataset?",
            "Crie uma view `top_paises_vw` com os 10 países por receita e consulte-a em Python.",
        ]),
        gabarito([
            ("Receita UK",
             "`SELECT ROUND(SUM(Quantity*UnitPrice),2) FROM vendas_vw WHERE Country='United Kingdom'` — "
             "resultado ~ R$ 7,5 milhões (o dataset é dominado pelo UK)."),
            ("Clientes únicos",
             "`SELECT COUNT(DISTINCT CustomerID) FROM vendas_vw WHERE CustomerID IS NOT NULL` — ~4.372."),
            ("Dia com mais vendas",
             "`SELECT DATE_TRUNC('day', InvoiceDate) dia, COUNT(*) n FROM vendas_vw GROUP BY dia ORDER BY n DESC LIMIT 1` — "
             "tipicamente um dia de novembro (Black Friday)."),
            ("View + Python",
             "`spark.sql('CREATE OR REPLACE TEMP VIEW top_paises_vw AS SELECT Country, SUM(Quantity*UnitPrice) receita FROM vendas_vw GROUP BY Country ORDER BY receita DESC LIMIT 10')` "
             "e depois `spark.table('top_paises_vw').collect()`."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana1_dia5_sql_avancado_tabelas_bronze",
    [
        header(
            "1", "5", "SQL analítico profundo e criação das tabelas Bronze",
            "Dominar os padrões SQL da prova DEA (GROUP BY, HAVING, CASE, joins) e criar as "
            "primeiras tabelas Delta governadas do projeto.",
            "DEA (ELT with Spark SQL)", "Tabelas `vendas_bronze` e `voos_bronze` criadas",
            "✅ Free Edition",
        ),
        teoria(
            "Padrões SQL que caem na prova",
            "**HAVING** filtra o resultado de uma agregação (diferente de WHERE, que filtra antes):\n"
            "```sql\nSELECT Country, COUNT(*) n FROM vendas GROUP BY Country HAVING n > 100\n```\n"
            "**CASE WHEN** cria colunas condicionais (essencial para faixas, flag de devolução):\n"
            "```sql\nCASE WHEN Quantity < 0 THEN 'devolução' ELSE 'venda' END\n```\n"
            "**JOINs**: inner, left, right, full, semi (existe na esquerda), anti (não existe na esquerda).\n"
            "**CTE (WITH)**: legibilidade para pipelines complexos.\n\n"
            "> 🎯 **Dica de prova**: SEMI e ANTI joins caem direto. Semi = filtro; Anti = "
            "exclusão. Memorize: `LEFT SEMI` devolve só colunas da esquerda; `LEFT ANTI` devolve "
            "linhas da esquerda sem correspondência na direita.",
        ),
        pratica("Criando as tabelas Bronze",
            "Agora criamos as tabelas governadas pelo UC com tipo `DELTA` — a base da arquitetura "
            "Medallion. Adicionamos `_ingested_at` (quando o dado chegou) — padrão de Bronze."),
        sql('CREATE SCHEMA IF NOT EXISTS workspace.bronze;\n'
            'CREATE OR REPLACE TABLE workspace.bronze.vendas_bronze (\n'
            '  InvoiceNo      STRING,\n'
            '  StockCode      STRING,\n'
            '  Description    STRING,\n'
            '  Quantity       INT,\n'
            '  InvoiceDate    TIMESTAMP,\n'
            '  UnitPrice      DOUBLE,\n'
            '  CustomerID     STRING,\n'
            '  Country        STRING,\n'
            '  _ingested_at   TIMESTAMP DEFAULT current_timestamp()\n'
            ') USING DELTA;'),
        code('# Carregar os dados limpos do CSV para a tabela Delta\n'
             'from pyspark.sql.functions import to_timestamp\n'
             'df_vendas = spark.read.format("csv") \\\n'
             '    .option("header", True) \\\n'
             '    .option("inferSchema", True) \\\n'
             '    .option("multiLine", True) \\\n'
             '    .load("/Volumes/workspace/bronze/vol_dados_curso/vendas.csv")\n'
             'df_limpo = (df_vendas\n'
             '    .withColumn("InvoiceDate", to_timestamp("InvoiceDate", "M/d/yyyy H:mm"))\n'
             '    .filter("Quantity > 0 AND UnitPrice > 0"))\n'
             'df_limpo.write.mode("overwrite").saveAsTable("workspace.bronze.vendas_bronze")\n'
             'print("vendas_bronze:", df_limpo.count(), "linhas")'),
        pratica("Segunda tabela: voos (dados secundários)",
            "Criamos dados sintéticos de voos para enriquecer o projeto (frequência de viagem dos "
            "clientes). Será usado no RAG na Semana 11."),
        sql('CREATE OR REPLACE TABLE workspace.bronze.voos_bronze (\n'
            '  CustomerID   STRING,\n'
            '  Voo          STRING,\n'
            '  Origem       STRING,\n'
            '  Destino      STRING,\n'
            '  Data_Voo     TIMESTAMP,\n'
            '  Classe       STRING,\n'
            '  Valor_Bilhete DOUBLE,\n'
            '  _ingested_at TIMESTAMP DEFAULT current_timestamp()\n'
            ') USING DELTA;'),
        code('# Gerar dados sintéticos de voos para clientes do varejo\n'
             'from datetime import datetime, timedelta\n'
             'import random\n'
             'random.seed(42)\n'
             'clientes = [r["CustomerID"] for r in spark.sql(\n'
             '    "SELECT DISTINCT CustomerID FROM workspace.bronze.vendas_bronze WHERE CustomerID IS NOT NULL").collect()]\n'
             'aeroportos = ["GRU", "CGH", "GIG", "BSB", "POA", "CNF", "REC", "SSA", "CWB", "FLN"]\n'
             'classes = ["Econômica", "Econômica", "Executiva", "Primeira"]\n'
             'voos = []\n'
             'for i, c in enumerate(clientes[:200]):\n'
             '    for _ in range(random.randint(1, 4)):\n'
             '        voos.append((c, f"VOO-{random.randint(1000,9999)}", random.choice(aeroportos),\n'
             '                     random.choice(aeroportos),\n'
             '                     datetime(2024,1,1) + timedelta(days=random.randint(0,365)),\n'
             '                     random.choice(classes),\n'
             '                     round(random.uniform(150, 2500), 2)))\n'
             'df_voos = spark.createDataFrame(voos, ["CustomerID","Voo","Origem","Destino","Data_Voo","Classe","Valor_Bilhete"])\n'
             'df_voos.write.mode("overwrite").saveAsTable("workspace.bronze.voos_bronze")\n'
             'print(f"voos_bronze: {df_voos.count()} registros")'),
        sql('-- Conferindo o que foi criado\n'
            'SHOW TABLES IN workspace.bronze;\n'
            'SELECT * FROM workspace.bronze.vendas_bronze LIMIT 5;'),
        pratica("SQL analítico sobre as tabelas Bronze",
            "Agora as queries rodam sobre a tabela governada (não mais sobre view temporária)."),
        sql('-- HAVING: países com mais de 2.000 vendas\n'
            'SELECT Country, COUNT(*) AS n FROM workspace.bronze.vendas_bronze\n'
            'GROUP BY Country HAVING n > 2000 ORDER BY n DESC'),
        sql('-- CASE WHEN: flag de ticket alto\n'
            'SELECT Country,\n'
            '       COUNT(*) AS vendas,\n'
            '       SUM(CASE WHEN Quantity * UnitPrice > 50 THEN 1 ELSE 0 END) AS vendas_caras\n'
            'FROM workspace.bronze.vendas_bronze\n'
            'GROUP BY Country ORDER BY vendas DESC LIMIT 5'),
        dica_prova("`DATE_TRUNC`, `CASE WHEN`, `HAVING` e os 6 tipos de JOIN são perguntas "
                   "garantidas. Pratique escrevê-los de memória."),
        exercicios([
            "Crie uma tabela `workspace.bronze.clientes_bronze` com dados sintéticos de clientes "
            "(CustomerID, Nome, Email, Cidade, Pais).",
            "Escreva uma query com CTE que calcula receita por país e filtra países com receita > 100 mil.",
            "Use LEFT ANTI para achar clientes que aparecem em vendas mas não na tabela de clientes.",
            "O que `_ingested_at` representa e por que é padrão em camadas Bronze?",
        ]),
        gabarito([
            ("clientes_bronze",
             "```sql\nCREATE OR REPLACE TABLE workspace.bronze.clientes_bronze (CustomerID STRING, Nome STRING, Email STRING, Cidade STRING, Pais STRING) USING DELTA;\n```\n"
             "Depois insira ~50 linhas sintéticas com Python (spark.createDataFrame)."),
            ("CTE com HAVING equivalente",
             "```sql\nWITH receita_pais AS (\n  SELECT Country, SUM(Quantity*UnitPrice) receita\n  FROM workspace.bronze.vendas_bronze GROUP BY Country)\nSELECT * FROM receita_pais WHERE receita > 100000 ORDER BY receita DESC;\n```"),
            ("LEFT ANTI",
             "```sql\nSELECT DISTINCT v.CustomerID FROM workspace.bronze.vendas_bronze v\nLEFT ANTI JOIN workspace.bronze.clientes_bronze c ON v.CustomerID = c.CustomerID;\n```"),
            ("_ingested_at",
             "Marca o momento em que a linha entrou no Bronze — permite reprocessamento, auditoria "
             "e janelas de ingestão. É o padrão de Bronze (append-only com timestamp de chegada)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana1_dia6_dashboard_bi_checklist",
    [
        header(
            "1", "6", "Primeiro dashboard e fechamento da Semana 1",
            "Publicar um dashboard simples de BI sobre as tabelas Bronze e fechar o ciclo da "
            "semana com revisão e checklist.",
            "DEA + DAA (BI)", "Dashboard publicado + checklist da semana concluído",
            "✅ Free Edition",
        ),
        teoria(
            "BI direto na fonte: a vantagem do Lakehouse",
            "No Lakehouse, os dashboards consultam **as mesmas tabelas Delta** que os pipelines "
            "escrevem — sem cópias para um BI separado. Isso elimina duplicidade, atraso e "
            "divergência de números.\n\n"
            "O **Databricks SQL** permite: visualizações, dashboards, alertas e agendamento de "
            "queries — tudo sobre o Unity Catalog.",
        ),
        pratica("Criando o primeiro dashboard",
            "1. Abra **SQL Warehouses** e garanta que o warehouse está **Running** (2X-Small).\n"
            "2. Vá em **Queries → New Query** e rode:\n"
            "```sql\nSELECT Country, COUNT(*) AS vendas, ROUND(SUM(Quantity*UnitPrice),2) AS receita\n"
            "FROM workspace.bronze.vendas_bronze GROUP BY Country ORDER BY receita DESC LIMIT 10;\n```\n"
            "3. No resultado, clique em **Visualization** e escolha **Bar chart**.\n"
            "4. Clique em **Save → Create dashboard** e adicione mais 2–3 queries (vendas por mês, "
            "top produtos).\n"
            "5. Publique o dashboard (botão **Publish**).",
        ),
        code('# A mesma consulta, via notebook (para conferência)\n'
             'display(spark.sql("""\n'
             '    SELECT Country, COUNT(*) AS vendas, ROUND(SUM(Quantity*UnitPrice),2) AS receita\n'
             '    FROM workspace.bronze.vendas_bronze GROUP BY Country ORDER BY receita DESC LIMIT 10\n'
             '"""))'),
        teoria(
            "Revisão da semana — o mapa mental que você deve ter",
            "```\nSemana 1\n ├─ Conta Free Edition (serverless, quotas)\n ├─ Interface (sidebar, workspace, data, compute)\n ├─ Lakehouse (7 características)\n ├─ Unity Catalog (catalog.schema.object)\n ├─ DBFS vs Volumes\n ├─ Formatos (CSV/JSON/Parquet/Delta)\n ├─ SQL Warehouse + queries\n ├─ Views temporárias (ponte Python↔SQL)\n └─ Bronze: vendas_bronze + voos_bronze (+clientes)\n```",
        ),
        dica_prova("Os dashboards do Databricks SQL caem na prova **DAA** (Data Analyst "
                   "Associate) e no domínio de BI do DEA. Saber montar visualização, agendar "
                   "query e configurar alerta é diferencial."),
        exercicios([
            "Crie uma query agendada que roda todo dia às 8h e envia o resultado por e-mail.",
            "Crie um alerta que dispara quando a receita diária cair 30% vs o dia anterior.",
            "Explique por que dashboards consultando o Ouro (futuro) são melhores que consultando o Bronze.",
        ]),
        gabarito([
            ("Query agendada",
             "Em Queries: botão **Schedule** → frequência diária 08:00 → **Refresh**. Com "
             "destino e-mail configurados no workspace, o resultado chega por e-mail."),
            ("Alerta de queda de receita",
             "Criar query com `(receita_hoje - receita_ontem)/receita_ontem`, e em **Alerts** "
             "definir condição (< -0.30) e ação (notificação por e-mail)."),
            ("Bronze vs Ouro",
             "O Ouro é modelado, limpo, denormalizado e estável para negócio; o Bronze é "
             "append-only e pode ter erros/lixo. Consultar Ouro evita respostas erradas e "
             "reprocessamentos."),
        ]),
        footer([
            "Rodei todos os 6 notebooks da Semana 1 sem erros.",
            "Expliquei Lakehouse, UC e Medallion em 3 frases cada.",
            "Criei vendas_bronze, voos_bronze e clientes_bronze.",
            "Publiquei um dashboard com 3 visualizações.",
            "Anotei as dúvidas restantes (se houver).",
        ]),
    ],
))
