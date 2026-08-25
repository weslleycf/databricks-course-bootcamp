"""Semana 2 — SQL avançado, Git e modelagem dimensional (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana2_dia1_sql_avancado_window_cte",
    [
        header(
            "2", "1", "SQL avançado: CTEs, Window Functions e PIVOT",
            "Dominar os padrões SQL cobrados na prova DEA e em entrevistas: CTEs, subqueries, "
            "window functions (ROW_NUMBER, LAG, RANK), PIVOT e filtros eficientes.",
            "DEA (ELT with Spark SQL)", "Exercícios de SQL avançado resolvidos",
            "✅ Free Edition",
        ),
        teoria(
            "Por que SQL avançado antes de Spark?",
            "Spark SQL é o motor de transformação número 1 no Databricks — a prova DEA 2026 é "
            "chamada oficialmente de *ELT with Spark SQL and Python*. Quem domina SQL analítico "
            "avançado domina 60% das transformações de um pipeline sem escrever uma linha de Python.",
        ),
        teoria(
            "CTEs e subqueries",
            "Uma **CTE (Common Table Expression)** nomeia uma subconsulta para reutilização e "
            "legibilidade:\n\n"
            "```sql\nWITH receita_pais AS (\n"
            "  SELECT Country, SUM(Quantity*UnitPrice) AS receita\n"
            "  FROM vendas GROUP BY Country)\n"
            "SELECT * FROM receita_pais WHERE receita > 100000;\n```\n\n"
            "**Regra mental**: WHERE filtra linhas antes da agregação; HAVING filtra o resultado "
            "depois. CTE é lida de cima para baixo — cada bloco é uma etapa do pipeline.",
        ),
        teoria(
            "Window Functions — o que fazem",
            "Uma window function calcula um valor **para cada linha** usando uma 'janela' de linhas "
            "relacionadas, SEM agrupar o resultado:\n\n"
            "```sql\nSELECT Country, InvoiceDate,\n"
            "       ROW_NUMBER()   OVER (PARTITION BY Country ORDER BY InvoiceDate DESC) AS rn,\n"
            "       RANK()         OVER (PARTITION BY Country ORDER BY receita DESC) AS rank,\n"
            "       LAG(receita)   OVER (PARTITION BY Country ORDER BY mes) AS receita_mes_anterior,\n"
            "       SUM(receita)   OVER (PARTITION BY Country ORDER BY mes) AS acumulado\n"
            "FROM ...;\n```\n\n"
            "- `ROW_NUMBER()`: numeração sem empates\n"
            "- `RANK()`: numeração com empates (pula posições)\n"
            "- `DENSE_RANK()`: empates sem pular posições\n"
            "- `LAG(col)`: valor da linha anterior na janela (para variação mês a mês)\n"
            "- `LEAD(col)`: valor da próxima linha\n"
            "- `SUM/AVG ... OVER`: agregação móvel/acumulada (running total)\n\n"
            "> 🎯 **Dica de prova**: window functions são o tópico #1 em SQL avançado na DEA. "
            "Decore a diferença entre ROW_NUMBER / RANK / DENSE_RANK e o papel de PARTITION BY "
            "(fatiar) vs ORDER BY (ordenar dentro da fatia).",
        ),
        pratica("Na prática",
            "Rode as consultas sobre a tabela Bronze e observe os resultados linha a linha."),
        sql('-- ROW_NUMBER: top 3 produtos por país\n'
            'WITH vendas_prod AS (\n'
            '  SELECT Country, StockCode, SUM(Quantity) AS qtd\n'
            '  FROM workspace.bronze.vendas_bronze GROUP BY Country, StockCode)\n'
            'SELECT Country, StockCode, qtd,\n'
            '       ROW_NUMBER() OVER (PARTITION BY Country ORDER BY qtd DESC) AS rn\n'
            'FROM vendas_prod QUALIFY rn <= 3\n'
            'ORDER BY Country, rn'),
        sql('-- LAG: variação de receita mês a mês\n'
            'WITH receita_mes AS (\n'
            '  SELECT DATE_TRUNC("month", InvoiceDate) AS mes,\n'
            '         SUM(Quantity*UnitPrice) AS receita\n'
            '  FROM workspace.bronze.vendas_bronze GROUP BY mes)\n'
            'SELECT mes, receita,\n'
            '       LAG(receita) OVER (ORDER BY mes) AS receita_anterior,\n'
            '       ROUND((receita - LAG(receita) OVER (ORDER BY mes)) / LAG(receita) OVER (ORDER BY mes) * 100, 2)\n'
            '         AS variacao_pct\n'
            'FROM receita_mes ORDER BY mes'),
        sql('-- PIVOT: vendas por país x trimestre\n'
            'SELECT * FROM (\n'
            '  SELECT Country,\n'
            '         QUARTER(InvoiceDate) AS trimestre,\n'
            '         Quantity * UnitPrice AS valor\n'
            '  FROM workspace.bronze.vendas_bronze)\n'
            'PIVOT (SUM(valor) FOR trimestre IN (1, 2, 3, 4))\n'
            'ORDER BY Country LIMIT 5'),
        dica_prova("`QUALIFY` filtra o resultado de uma window function (como HAVING para GROUP BY) "
                   "— cai com frequência. No Databricks, QUALIFY é suportado nativamente."),
        exercicios([
            "Qual o ticket médio por país usando CTE e window (média móvel de 3 meses por país)?",
            "Liste os 2 produtos mais vendidos de cada país (use ROW_NUMBER + QUALIFY).",
            "Calcule a receita acumulada por país ao longo dos meses (running total).",
            "Diferencie ROW_NUMBER, RANK e DENSE_RANK com um exemplo de empate.",
        ]),
        gabarito([
            ("Média móvel 3 meses",
             "```sql\nWITH rec AS (\n  SELECT Country, DATE_TRUNC('month',InvoiceDate) mes, SUM(Quantity*UnitPrice) receita\n  FROM workspace.bronze.vendas_bronze GROUP BY Country, mes)\nSELECT Country, mes, AVG(receita) OVER (PARTITION BY Country ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) media_3m\nFROM rec;\n```"),
            ("Top 2 por país",
             "```sql\nWITH vp AS (SELECT Country, StockCode, SUM(Quantity) qtd FROM workspace.bronze.vendas_bronze GROUP BY Country, StockCode)\nSELECT * FROM (SELECT Country, StockCode, qtd, ROW_NUMBER() OVER (PARTITION BY Country ORDER BY qtd DESC) rn FROM vp) WHERE rn <= 2;\n```"),
            ("Running total",
             "`SUM(receita) OVER (PARTITION BY Country ORDER BY mes)` — sem ROWS BETWEEN, o padrão é "
             "até a linha atual (cumulativo)."),
            ("ROW_NUMBER vs RANK",
             "Com empate (qtd 10,10,9): ROW_NUMBER dá 1,2,3; RANK dá 1,1,3; DENSE_RANK dá 1,1,2. "
             "RANK pula posição após empate; DENSE_RANK não."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana2_dia2_qualidade_dados_constraints",
    [
        header(
            "2", "2", "Qualidade de dados: 6 dimensões e constraints",
            "Entender as 6 dimensões de qualidade de dados, fazer profiling e aplicar "
            "constraints (CHECK, NOT NULL) nas tabelas Delta.",
            "DEA (qualidade de dados)", "Regras de qualidade aplicadas no Bronze",
            "✅ Free Edition",
        ),
        teoria(
            "As 6 dimensões de qualidade de dados",
            "| Dimensão | Pergunta | Exemplo de falha |\n|---|---|---|\n"
            "| **Completude** | Todos os valores estão presentes? | `CustomerID` nulo |\n"
            "| **Unicidade** | Há duplicatas? | mesma nota 2x |\n"
            "| **Validade** | Valores respeitam o domínio? | `Quantity = -999` |\n"
            "| **Pontualidade** | Os dados chegaram a tempo? | ingestão atrasada 3h |\n"
            "| **Precisão** | Os valores são exatos? | preço 10.0 registrado 9.97 |\n"
            "| **Consistência** | Dados coerentes entre fontes? | país 'BR' vs 'BRA' |\n\n"
            "> 🎯 **Dica de prova**: a DEA pede para **classificar** um problema de qualidade na "
            "dimensão correta. Ex.: duplicata = unicidade; CPF inválido = validade; campo vazio = "
            "completude.",
        ),
        teoria(
            "Enforcement de qualidade no Delta",
            "O Delta Lake permite **constraints** que o motor **impõe na escrita**:\n\n"
            "```sql\nALTER TABLE t ADD CONSTRAINT ck_qtd CHECK (Quantity > 0);\nALTER TABLE t ADD CONSTRAINT nn_cliente NOT NULL (CustomerID);\n```\n\n"
            "Se uma escrita violar a constraint, a transação **falha inteira** (ACID) — nenhuma "
            "linha entra. Isso é a diferença entre 'esperar qualidade' e 'garantir qualidade'.",
        ),
        pratica("Profiling do Bronze",
            "Primeiro: conheça o dado. Faça o perfil de completude, unicidade e validade."),
        code('# Profiling: completude e unicidade\n'
             'from pyspark.sql.functions import col, count, countDistinct, isnan, isnull\n'
             'df = spark.table("workspace.bronze.vendas_bronze")\n'
             'df.select([count(isnull(c)).alias(f"nulos_{c}") for c in df.columns]).show()\n'
             'print("Linhas totais:", df.count())\n'
             'print("Notas únicas:", df.select(countDistinct("InvoiceNo")).collect()[0][0])'),
        code('# Profiling: validade e consistência\n'
             'display(df.select("Country").distinct().orderBy("Country"))\n'
             'df.filter("Quantity <= 0 OR UnitPrice <= 0").count()'),
        pratica("Aplicando constraints",
            "Agora travamos as regras no schema — qualquer escrita que viole falha a transação."),
        sql('ALTER TABLE workspace.bronze.vendas_bronze\n'
            '  ADD CONSTRAINT ck_vendas_quantidade_positiva CHECK (Quantity > 0);\n'
            'ALTER TABLE workspace.bronze.vendas_bronze\n'
            '  ADD CONSTRAINT ck_vendas_preco_positivo CHECK (UnitPrice > 0);\n'
            'SHOW TBLPROPERTIES workspace.bronze.vendas_bronze ("delta.constraints.*")'),
        code('# Testar a constraint: essa escrita DEVE falhar\n'
             'from pyspark.sql import Row\n'
             'try:\n'
             '    spark.createDataFrame([Row(InvoiceNo="T", StockCode="X", Description="", Quantity=-1,\n'
             '                                 InvoiceDate="2024-01-01", UnitPrice=10.0, CustomerID=None,\n'
             '                                 Country="BR")]) \\\n'
             '        .write.mode("append").saveAsTable("workspace.bronze.vendas_bronze")\n'
             '    print("ERRO: deveria ter falhado!")\n'
             'except Exception as e:\n'
             '    print("Constraint funcionou — escrita bloqueada:", str(e)[:120])'),
        dica_prova("Constraints `CHECK` e `NOT NULL` são garantia de prova (DEA). Memorize a "
                   "sintaxe e o comportamento: violação → transação inteira falha."),
        exercicios([
            "Classifique em qual dimensão cai: (a) mesmo cliente com 2 IDs; (b) email inválido; (c) coluna vazia; (d) dado de ontem que chegou hoje.",
            "Adicione uma constraint que garanta que `UnitPrice >= 0`.",
            "Por que constraints falham a transação inteira em vez de descartar a linha?",
        ]),
        gabarito([
            ("Classificação",
             "(a) unicidade; (b) validade; (c) completude; (d) pontualidade."),
            ("Constraint",
             "```sql\nALTER TABLE workspace.bronze.vendas_bronze ADD CONSTRAINT ck_preco CHECK (UnitPrice >= 0);\n```"),
            ("Transação inteira",
             "Porque o Delta é ACID: uma escrita que viola constraint fica 'incompleta' — aceitar "
             "parcialmente quebraria a atomicidade e a consistência. O produtor deve corrigir o "
             "dado na origem."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana2_dia3_git_github_fundamentos",
    [
        header(
            "2", "3", "Git e GitHub do zero",
            "Dominar os fundamentos de Git (commit, branch, merge, PR) — pré-requisito para "
            "Databricks Repos e DABs na Semana 6, e para qualquer vaga no mercado.",
            "DEP (IaC/CI/CD), carreira", "Repositório do curso criado no GitHub",
            "✅ Free Edition (Git local + GitHub)",
        ),
        teoria(
            "Por que Git antes de DABs?",
            "A Semana 6 vai versionar pipelines com **Databricks Asset Bundles (DABs)** — e DABs "
            "é 100% Git. Sem dominar commit/branch/merge, você trava o fluxo de produção. Git "
            "também é a base do seu portfólio: entrevistadores pedem para ver seu repositório.",
        ),
        teoria(
            "Conceitos fundamentais",
            "**Repositório** = pasta versionada. **Commit** = snapshot do código com mensagem. "
            "**Branch** = linha de trabalho independente (ex.: `feature/x`, `workspace`). "
            "**Merge** = integrar branches. **Pull Request (PR)** = proposta de merge com revisão "
            "antes de integrar.\n\n"
            "**Fluxo Git simples e profissional**:\n"
            "```\nmain ──●───●───●───●\n           \\         /\nfeature ────●───●───\n```\n\n"
            "**Regra de ouro**: commits pequenos, mensagens descritivas, e nunca trabalhar "
            "diretamente na `workspace` em equipes (sempre branch + PR).",
        ),
        pratica("Configurando",
            "Rode no seu computador (não no notebook). Se não tiver Git instalado: "
            "https://git-scm.com/downloads."),
        code('# COMANDOS PARA O SEU TERMINAL LOCAL (não no Databricks)\n'
             '# 1. Configurar identidade\n'
             '!git config --global user.name "Seu Nome"        # ajuste para seu nome\n'
             '!git config --global user.email "seu@email.com"  # ajuste para seu email\n'
             'print("Configure sua identidade no terminal local!")'),
        pratica("Criando o repositório",
            "1. Crie um repo **vazio** no GitHub (sem README).\n"
            "2. No terminal:\n"
            "```\ngit clone https://github.com/SEU_USUARIO/databricks-course.git\ncd databricks-course\n```\n"
            "3. Adicione os arquivos e o primeiro commit."),
        code('# Fluxo básico (terminal local)\n'
             '!git add README.md\n'
             '!git commit -m "docs: README inicial do curso"\n'
             '!git push origin main\n'
             'print("Fluxo: git add -> git commit -> git push")'),
        pratica("Branches e merge",
            "Trabalhe em uma branch e integre com PR — o fluxo que as empresas usam."),
        code('# Terminal local\n'
             '!git checkout -b feature/primeiro-notebook\n'
             '!git add .\n'
             '!git commit -m "feat: primeiro notebook da Semana 1"\n'
             '!git push origin feature/primeiro-notebook\n'
             'print("Abra o GitHub e crie um Pull Request da branch para main.")'),
        teoria(
            "Bons padrões de commit (conventional commits)",
            "Formato `tipo(escopo): descrição`:\n"
            "- `feat:` nova funcionalidade\n"
            "- `fix:` correção\n"
            "- `docs:` documentação\n"
            "- `refactor:` reorganização sem mudar comportamento\n"
            "- `test:` testes\n\n"
            "Ex.: `feat: cria pipeline de vendas Bronze` · `docs: adiciona diagrama Medallion`\n\n"
            "> 🎯 **Dica de prova (DEP)**: a prova cobra o fluxo de trabalho com Git em "
            "Databricks Repos (branch, PR, integração com CI). Saber `git add/commit/push` e "
            "branches é o mínimo.",
        ),
        dica_prova("Databricks Repos integra seu repositório Git ao workspace: você edita "
                   "notebooks direto no branch e faz merge via PR. Sem Git, não há Repos."),
        exercicios([
            "O que faz cada comando: add, commit, push, pull, merge?",
            "Crie uma branch, altere um arquivo, faça commit e abra um PR no GitHub.",
            "Qual a diferença entre merge e pull request?",
            "Escreva 3 mensagens de commit seguindo conventional commits.",
        ]),
        gabarito([
            ("Comandos",
             "add = marca mudanças para o próximo commit; commit = snapshot com mensagem; push = "
             "envia commits locais ao remoto; pull = traz commits do remoto; merge = integra uma "
             "branch em outra."),
            ("Exercício prático",
             "`git checkout -b nova-branch` → edite → `git add .` → `git commit -m` → "
             "`git push origin nova-branch` → GitHub: New Pull Request → merge."),
            ("Merge vs PR",
             "Merge é a operação técnica de integrar; PR é o processo de propor/revisar a "
             "integração (code review, testes antes de aceitar)."),
            ("Conventional commits",
             "Ex.: `feat: adiciona constraint de qualidade`, `fix: corrige timezone da data`, "
             "`docs: atualiza README do projeto`."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4 — CURSO COMPLETO DE MODELAGEM DIMENSIONAL
NOTEBOOKS.append((
    "semana2_dia4_modelagem_dimensional_star_schema",
    [
        header(
            "2", "4", "Modelagem Dimensional Completa — Curso Intensivo",
            "Curso completo de modelagem dimensional (Kimball): de OLTP vs OLAP à Bus Matrix, "
            "todos os tipos de fato/dimensão, SCD 0–7, hierarquias, casos avançados e o mapeamento "
            "definitivo na arquitetura Medallion do Databricks (Bronze → Prata → Ouro).",
            "DEA (modelagem + SQL), DEP (SCD/CDC)", "Modelo dimensional completo + Bus Matrix do projeto",
            "✅ Free Edition",
        ),

        # =======================================================================
        # BLOCO 1 — FUNDAMENTOS
        # =======================================================================
        teoria(
            "1. Por que modelar? O pecado original dos dados não modelados",
            "Imagine um armazém onde cada caixa chega com etiqueta diferente, sem corredor, sem "
            "prateleira. Você até guarda tudo — mas **ninguém acha nada**, e quando acha, o número "
            "não bate com o do colega. É exatamente o que acontece quando dados vão do Bronze direto "
            "para dashboards sem modelagem.\n\n"
            "**Sintomas de um modelo ausente**:\n"
            "- 10 dashboards, 10 números diferentes para 'receita do mês'.\n"
            "- Qualquer pergunta nova exige um engenheiro escrever SQL complexo.\n"
            "- Uma coluna muda de nome e 30 relatórios quebram.\n\n"
            "A **modelagem dimensional** (Ralph Kimball, anos 90) resolve isso separando o **evento** "
            "(o fato que aconteceu) do **contexto** (quem, o que, onde, quando). Essa separação é a "
            "base de todo BI, de todo Data Warehouse moderno — e da camada **Prata/Ouro** da "
            "Medallion.",
        ),
        teoria(
            "2. OLTP vs OLAP — duas gravidades diferentes",
            "| Aspecto | OLTP (transacional) | OLAP (analítico) |\n"
            "|---|---|---|\n"
            "| Objetivo | Registrar a operação | Entender o negócio |\n"
            "| Operação típica | `INSERT 1 pedido` | `SUM(receita) por país no ano` |\n"
            "| Modelo | Normalizado (3FN), sem redundância | Denormalizado (Star), redundância proposital |\n"
            "| Leitura vs Escrita | 1 linha por vez, muita escrita | Milhões de linhas, quase só leitura |\n"
            "| Exemplo | Postgres do e-commerce (pedidos) | Lakehouse `fato_vendas` (análise) |\n\n"
            "**Regra de ouro**: NUNCA faça BI direto no OLTP. O OLAP é uma **cópia modelada** otimizada "
            "para perguntas. Na Medallion: OLTP → Bronze (cópia crua) → Prata/Ouro (modelo OLAP).",
        ),
        teoria(
            "3. Inmon vs Kimball — e onde a Medallion se posiciona",
            "- **Inmon (top-down)**: modela tudo normalizado (3FN) primeiro, depois cria marts. Rigoroso, lento.\n"
            "- **Kimball (bottom-up)**: começa pelos **processos de negócio**, entrega um Star por vez, "
            "integra por **dimensões conformadas**. Ágil, incremental.\n\n"
            "**A Medallion é Kimball moderna**:\n"
            "- Bronze = staging/raw (como a área de stage do Kimball).\n"
            "- Prata = dimensões e fatos limpos, **conformed**, SCD — o Data Warehouse dimensional.\n"
            "- Ouro = marts e agregados denormalizados — os Data Marts.\n\n"
            "Ou seja: Kimball descreve **o que modelar**; Medallion descreve **onde guardar cada camada** "
            "no Lakehouse. Usamos os dois juntos.",
        ),
        teoria(
            "4. Os 4 passos do design dimensional (Kimball) — o método",
            "Todo modelo dimensional nasce de 4 decisões, **nesta ordem**:\n\n"
            "1. **Escolher o processo de negócio** — ex.: 'Vendas', 'Estoque', 'Atendimento'.\n"
            "2. **Declarar o grain** — a granularidade de UMA linha da fato. Ex.: 'uma linha por item de nota'.\n"
            "3. **Escolher as dimensões** — o contexto: quem comprou, o que, quando, onde, como pagou.\n"
            "4. **Identificar os fatos** — as medidas numéricas: quantidade, preço, desconto, receita.\n\n"
            "> ⚠️ Se errar o grain, todo o resto fica errado. Por isso o passo 2 merece uma seção inteira.",
        ),

        # =======================================================================
        # BLOCO 2 — GRAIN
        # =======================================================================
        teoria(
            "5. Grain — a decisão #1 do projeto (e a mais cara se errar)",
            "**Grain** = o que UMA linha da fato representa. É a 'frase' do modelo.\n\n"
            "Exemplos no varejo:\n"
            "- `fato_vendas` → **uma linha por item de nota** (InvoiceNo + StockCode). Grain atômico.\n"
            "- `fato_vendas_diaria` → **uma linha por dia x país** (agregado). Grain diário.\n"
            "- `foto_estoque_diaria` → **uma linha por produto x dia** (snapshot).\n\n"
            "**Perguntas para declarar o grain**:\n"
            "- A linha pode ser duplicada? Se sim, o grain está errado.\n"
            "- Posso responder 'quantas linhas há por pedido'? Se não, o grain esconde detalhe.\n"
            "- Preciso de histórico por item ou só total do dia?\n\n"
            "**Regra de ouro da Medallion**: a Prata guarda o **grain mais atômico** que o negócio precisa. "
            "O Ouro agrega a partir dela. Nunca agregue cedo demais — detalhe perdido não volta.",
        ),
        pratica(
            "Declarando o grain do projeto (varejo)",
            "Vamos explicitar os 3 grains que usaremos:",
        ),
        code('# Os 3 grains do nosso projeto — documente assim em todo projeto\n'
             'grains = {\n'
             '    "fato_vendas (Prata)":       "1 linha = 1 ITEM de 1 NOTA (atômico) — InvoiceNo+StockCode",\n'
             '    "fato_vendas_diaria (Ouro)": "1 linha = 1 DIA x 1 PAIS (agregado) — data_venda+Country",\n'
             '    "foto_estoque (Prata)":      "1 linha = 1 PRODUTO x 1 DIA (snapshot)",\n'
             '}\n'
             'for k, v in grains.items():\n'
             '    print(f"{k:30s} → {v}")\n'
             'print("\\nGrain atômico na Prata = máxima flexibilidade; agregados no Ouro = performance.")'),
        teoria(
            "6. O teste do grain — 3 perguntas que salvam o projeto",
            "Antes de criar qualquer tabela, responda:\n\n"
            "1. **'Se eu contar linhas, o que estou contando?'** — Se a resposta não for cristalina, o grain está vago.\n"
            "2. **'Posso ter duas linhas com a mesma chave natural?'** — Se sim, falta coluna na PK.\n"
            "3. **'Se eu agregar para um grain maior, perco informação essencial?'** — Se sim, mantenha o atômico.\n\n"
            "No nosso `fato_vendas`, a PK é `(InvoiceNo, StockCode, InvoiceDate)` no Bronze; na Prata vira "
            "surrogate keys + medidas. Duplicata nesse grain = erro de ingestão (capturado por expectation).",
        ),

        # =======================================================================
        # BLOCO 3 — FATOS
        # =======================================================================
        teoria(
            "7. Tabelas Fato — o coração que bate",
            "**Fato** = evento de negócio mensurável. Características:\n"
            "- **Muitas linhas** (centenas de milhões é normal).\n"
            "- **Poucas colunas textuais** — quase tudo é chave estrangeira + medida numérica.\n"
            "- **Cresce sempre** — append-only por natureza (como o Bronze, mas limpo).\n"
            "- **Chave primária** é composta pelas FKs (ou surrogate da fato, se precisar).\n\n"
            "Cada linha **deve** ter: FKs para todas as dimensões + pelo menos 1 medida. "
            "Fato sem medida = **factless** (ver §8).",
        ),
        teoria(
            "8. Os 5 tipos de fato — quando usar cada um",
            "| Tipo | O que registra | Exemplo no varejo | Quando usar |\n"
            "|---|---|---|---|\n"
            "| **Transaction** | Um evento pontual | `fato_vendas` (cada item vendido) | Quase sempre — é o grain atômico |\n"
            "| **Periodic Snapshot** | Estado em intervalo fixo | `foto_estoque_diaria` (estoque todo dia) | Monitorar evolução (estoque, saldo) |\n"
            "| **Accumulating Snapshot** | Ciclo de vida com datas móveis | `fato_pedido` (pedido → pagamento → envio → entrega, 1 linha que é atualizada) | Pipeline com marcos |\n"
            "| **Factless (coverage)** | Evento sem medida | `fato_promocao_produto` (produto esteve em promoção?) | Cobertura, participação, elegibilidade |\n"
            "| **Consolidated / Aggregate** | Fato de fatos | `fato_vendas_diaria` (Ouro) | Performance de BI |\n\n"
            "**Regra**: comece sempre por **Transaction**. Os outros são derivados ou complementares.",
        ),
        teoria(
            "9. Additivity — a matemática que decide se a soma faz sentido",
            "Nem toda medida pode ser somada livremente:\n\n"
            "- **Aditiva** — soma em qualquer dimensão sem distorcer. Ex.: `quantidade`, `receita`. Pode `SUM` por dia, país, produto.\n"
            "- **Semi-aditiva** — soma em algumas dimensões, não em outras. Ex.: `saldo_em_estoque` (soma por produto OK, por dia NÃO — tem que pegar o último dia). `AVG` é semi-aditivo.\n"
            "- **Não-aditiva** — nunca soma direto. Ex.: `percentual`, `taxa_conversao`, `ticket_medio`. Tem que recalcular: `SUM(receita)/COUNT(pedidos)`.\n\n"
            "> 🎯 **Pegadinha de prova e de entrevista**: 'Posso somar ticket médio por país para ter a média geral?' — NÃO. Média de médias distorce. Recalcule sempre.",
        ),
        pratica(
            "Classificando as medidas do varejo",
            "Vamos explicitar a aditividade de cada medida:",
        ),
        code('# Aditividade das medidas do fato_vendas\n'
             'medidas = {\n'
             '    "quantidade":      "ADITIVA — SUM(quantidade) por qualquer dimensão",\n'
             '    "receita":          "ADITIVA — SUM(quantidade*preço) por qualquer dimensão",\n'
             '    "saldo_estoque":    "SEMI-ADITIVA — SUM por produto OK, por tempo pegue o último snapshot",\n'
             '    "ticket_medio":     "NAO-ADITIVA — recalcule SUM(receita)/COUNT(pedidos)",\n'
             '    "taxa_desconto":    "NAO-ADITIVA — recalcule a cada consulta",\n'
             '}\n'
             'for k, v in medidas.items():\n'
             '    print(f"{k:18s} → {v}")'),

        # =======================================================================
        # BLOCO 4 — DIMENSÕES
        # =======================================================================
        teoria(
            "10. Tabelas Dimensão — o contexto que dá significado",
            "**Dimensão** = o 'quem, o que, onde, quando, como, por quê' do fato.\n"
            "- **Poucas linhas** (milhares, não milhões).\n"
            "- **Muitas colunas textuais** — atributos descritivos, hierarquias.\n"
            "- **Chave primária = surrogate key** (`sk_*`).\n"
            "- **Muda lentamente** — por isso existe SCD.\n\n"
            "Boa dimensão é **larga e rasa**: muitas colunas, poucas linhas, desnormalizada de propósito "
            "para evitar joins em cadeia no BI.",
        ),
        teoria(
            "11. Star vs Snowflake vs Galaxy — a geometria do modelo",
            "- **Star (estrela)** ★ — fato no centro, dimensões desnormalizadas ao redor. 1 join por dimensão. "
            "**Padrão do Databricks e da prova**. Rápido, simples para o usuário.\n"
            "- **Snowflake (floco)** ❄ — dimensões normalizadas em sub-dimensões (ex.: `dim_produto` → `dim_categoria` → `dim_departamento`). "
            "Economiza espaço, mas cria joins em cadeia. Evite, a menos que a dimensão seja gigante e compartilhada.\n"
            "- **Galaxy / Constellation** 🌌 — múltiplos fatos compartilhando dimensões conformadas (ex.: `fato_vendas` e `fato_estoque` compartilham `dim_produto` e `dim_tempo`). "
            "É o **DW completo**: vários Stars conectados.\n\n"
            "```\n"
            "         dim_cliente\n"
            "             │\n"
            "dim_tempo ──fato_vendas── dim_produto          ← STAR (1 fato)\n"
            "             │\n"
            "         dim_loja\n\n"
            "  fato_vendas ─┐\n"
            "               ├─ dim_produto (conformed) ─┐  ← GALAXY (2 fatos)\n"
            "  foto_estoque ─┘                          │\n"
            "               └─ dim_tempo  (conformed) ──┘\n"
            "```",
        ),
        pratica(
            "O Star do projeto — e o Galaxy que vamos construir",
            "Hoje: 1 Star (`fato_vendas`). No curso: Galaxy com `foto_estoque` compartilhando dimensões.",
        ),
        code('# Star atual do projeto (Prata)\n'
             'print("STAR: fato_vendas no centro")\n'
             'print("  ├─ dim_cliente  (sk_cliente, CustomerID, Country, ... )")\n'
             'print("  ├─ dim_produto  (sk_produto, StockCode, Description, categoria)")\n'
             'print("  ├─ dim_tempo    (sk_tempo, data, ano, mes, trimestre)")\n'
             'print("  └─ dim_loja     (sk_loja, Country → futuro: loja física)")\n'
             'print("\\nGALAXY futuro: fato_vendas + foto_estoque compartilham dim_produto e dim_tempo")'),
        teoria(
            "12. Os 9 tipos de dimensão que você precisa conhecer",
            "| Tipo | O que é | Exemplo | Quando usar |\n"
            "|---|---|---|---|\n"
            "| **Conformed** | Dimensão compartilhada entre fatos (mesma chave e atributos) | `dim_tempo` usada por vendas e estoque | Sempre que possível — é o que integra o DW |\n"
            "| **Role-Playing** | Mesma dimensão com papéis diferentes | `dim_data` como `data_pedido`, `data_envio`, `data_entrega` | Reutilize sem duplicar tabela |\n"
            "| **Junk (garbage)** | Agrupa flags/indicadores de baixa cardinalidade | `dim_transacao` (tipo_pagamento, canal, indicador_fraude) | Evita Fato com 15 colunas booleanas |\n"
            "| **Degenerate** | Dimensão sem tabela (atributo direto na fato) | `InvoiceNo` (número da nota) | Chave operacional sem atributos |\n"
            "| **Outrigger** | Dimensão de dimensão (snowflake pontual) | `dim_cliente` → `dim_endereco` | Atributo gigante e volátil (endereço) |\n"
            "| **Bridge** | Resolve N:N | `bridge_cliente_programa` (cliente ↔ programas de fidelidade) | Fato precisa contar por múltiplos valores |\n"
            "| **Mini-dim** | Fatia atributos voláteis | `dim_cliente_profile` (faixa de crédito volátil) | Evita SCD2 explosivo |\n"
            "| **Heterogeneous (combo)** | Supertabela de subtipos | `dim_produto` (livro tem ISBN, roupa tem tamanho) | Subtipos com atributos distintos |\n"
            "| **Shrunken / Rollup** | Dimensão agregada | `dim_mes` (só ano/mês) | Fato agregado mensal |\n\n"
            "> 💡 No curso, você verá na prática: **conformed** (semana 4), **junk** e **degenerate** (semana 5), "
            "**role-playing** (semana 8), **bridge** e **mini-dim** (§15).",
        ),
        teoria(
            "13. Hierarquias — o mapa de navegação do usuário",
            "Toda dimensão tem hierarquias que o usuário usa para drill-down:\n"
            "- `dim_tempo`: ano → trimestre → mês → dia\n"
            "- `dim_produto`: departamento → categoria → subcategoria → produto\n"
            "- `dim_loja`: país → região → cidade → loja\n\n"
            "Tipos:\n"
            "- **Balanceada**: todo ramo tem mesma profundidade (tempo).\n"
            "- **Ragged / variável**: ramos com profundidades diferentes (organograma).\n"
            "- **Skip-level (ragged)**: níveis pulados (produto sem subcategoria).\n\n"
            "**Best practice**: mantenha hierarquias **achatadas (flattened)** na dimensão (uma coluna por nível), "
            "não normalizadas. O BI agradece. No Delta, use `COMMENT` para documentar cada nível.",
        ),

        # =======================================================================
        # BLOCO 5 — CHAVES
        # =======================================================================
        teoria(
            "14. Chaves — natural, surrogate e durable (NK / SK / DK)",
            "- **Natural Key (NK)**: o ID do sistema de origem (`CustomerID=17850`). Instável: pode mudar, ser reutilizado, ter formato diferente por fonte.\n"
            "- **Surrogate Key (SK)**: inteiro sequencial artificial (`sk_cliente=42`). Estável, compacto, imune a mudanças da origem. **PK da dimensão** e **FK da fato**.\n"
            "- **Durable Key (DK) / BKCC**: chave estável da entidade ao longo do tempo, mesmo com SCD2 (ex.: `dk_cliente`). Permite contar 'quantos clientes únicos' ignorando versões.\n\n"
            "**Regra de ouro**: Fatos referenciam **SK**, nunca NK. A NK fica na dimensão como `nk_cliente` para rastreabilidade.\n\n"
            "```\n"
            "dim_cliente\n"
            "  sk_cliente  (PK, surrogate, ex.: 42)\n"
            "  nk_cliente  (NK, ex.: '17850' do ERP)\n"
            "  dk_cliente  (DK, ex.: 'C17850' estável)\n"
            "  nome, país, ...\n\n"
            "fato_vendas\n"
            "  sk_cliente  (FK → dim_cliente.sk_cliente)\n"
            "  sk_produto  (FK → dim_produto.sk_produto)\n"
            "  quantidade, receita  (medidas)\n"
            "```",
        ),
        pratica(
            "Criando surrogate keys no Lakehouse — 3 estratégias",
            "Vamos comparar as 3 formas de gerar SK e quando usar cada uma:",
        ),
        code('# Estratégia 1: row_number (simples, para carga full)\n'
             'from pyspark.sql.window import Window\n'
             'from pyspark.sql.functions import row_number, sha2, col, monotonically_increasing_id\n'
             'df_dim = spark.table("workspace.bronze.vendas_bronze") \\\n'
             '    .select("CustomerID", "Country").dropDuplicates(["CustomerID"])\n'
             'df_dim_sk1 = df_dim.withColumn("sk_cliente", row_number().over(Window.orderBy("CustomerID")))\n'
             'df_dim_sk1.show(3)\n'
             'print("row_number: simples, mas muda a cada recarga full — não é estável para SCD2.")'),
        code('# Estratégia 2: hash da NK (determinística, idempotente)\n'
             'df_dim_sk2 = df_dim.withColumn("sk_cliente", sha2(col("CustomerID"), 256))\n'
             'df_dim_sk2.show(3, truncate=False)\n'
             'print("sha2(NK): determinística — mesmo cliente sempre gera mesma SK. Boa para idempotência.")'),
        code('# Estratégia 3: sequence + MERGE (incremental, estável, padrão SCD2 em produção)\n'
             '# Na Prata SCD2 real (semana 8), a SK é gerada por `APPLY CHANGES INTO` (Delta Live Tables)\n'
             '# ou por sequence + MERGE. Nunca recalcule SK de dimensões SCD2 com row_number.\n'
             'print("Em produção SCD2: use APPLY CHANGES / sequence — SK estável entre cargas.")'),
        teoria(
            "15. O erro mais caro: usar NK na fato",
            "Se a fato referencia NK e o cliente muda de código (fusão de sistemas), todas as linhas antigas "
            "ficam órfãs. Com SK, a dimensão mapeia NK→SK e a fato continua íntegra. "
            "Além disso, SK inteiro é **10–100x mais rápido** para joins que string.",
        ),

        # =======================================================================
        # BLOCO 6 — SCD
        # =======================================================================
        teoria(
            "16. SCD — Slowly Changing Dimensions (o capítulo inteiro)",
            "Dimensões mudam devagar (cliente muda de cidade, produto muda de categoria). Como registrar?\n\n"
            "| Tipo | Estratégia | Perde histórico? | Complexidade | Quando usar |\n"
            "|---|---|---|---|---|\n"
            "| **SCD 0** | Nunca muda (fixo) | N/A | Zero | Atributos imutáveis (data de nascimento) |\n"
            "| **SCD 1** | Sobrescreve | ✅ Sim | Baixa | Correção de erro — histórico não importa |\n"
            "| **SCD 2** | Nova linha com vigência | ❌ Não | Alta | Auditoria / análise temporal (padrão) |\n"
            "| **SCD 3** | Coluna de valor anterior | Parcial | Média | Só precisa do 'antes e agora' (ex.: `cidade_atual`, `cidade_anterior`) |\n"
            "| **SCD 4** | Tabela de histórico separada | ❌ Não | Alta | Quer manter dimensão 'atual' magra |\n"
            "| **SCD 6** | SCD1 + SCD2 + SCD3 (híbrido) | ❌ Não | Muito alta | Precisa do atual sobrescrito E do histórico |\n"
            "| **SCD 7** | SCD1 na dim + SCD2 em outrigger | ❌ Não | Alta | Atributos voláteis vs estáveis separados |\n\n"
            "> 🎯 **Dica de prova/interview**: 90% das perguntas são SCD1 vs SCD2. Resposta-padrão: "
            "'Correção → SCD1; histórico/auditoria → SCD2; só anterior→ SCD3.' Na Medallion, SCD2 vive na **Prata**.",
        ),
        teoria(
            "17. SCD2 em detalhes — as colunas que não podem faltar",
            "Uma dimensão SCD2 tem, além dos atributos, estas colunas técnicas:\n\n"
            "| Coluna | Papel | Exemplo |\n"
            "|---|---|---|\n"
            "| `sk_*` | PK surrogate da versão | 101, 102 |\n"
            "| `nk_*` | NK da origem | '17850' |\n"
            "| `valid_from` | Início da vigência | 2024-01-01 |\n"
            "| `valid_to` | Fim da vigência (NULL = atual) | NULL |\n"
            "| `is_current` | Flag de versão atual | true/false |\n"
            "| `row_hash` | Hash dos atributos (detectar mudança) | sha2(concat(*), 256) |\n\n"
            "Consulta 'estado atual': `WHERE is_current = true`. Consulta 'como era em 2024-06-01': "
            "`WHERE '2024-06-01' BETWEEN valid_from AND coalesce(valid_to, '9999-12-31')`.",
        ),
        pratica(
            "SCD2 — antes e depois (visual)",
            "Veja o efeito de um SCD2 quando o cliente 17850 muda de país:",
        ),
        code('# SCD2: estado ANTES da mudança\n'
             'print("dim_cliente (SCD2) — ANTES:")\n'
             'print("sk | nk    | país           | valid_from | valid_to | current")\n'
             'print(" 1 | 17850 | United Kingdom | 2010-12-01 | NULL     | true")\n'
             'print("\\nSCD2: DEPOIS de mudar para France em 2024-06-15:")\n'
             'print("sk | nk    | país           | valid_from | valid_to   | current")\n'
             'print(" 1 | 17850 | United Kingdom | 2010-12-01 | 2024-06-14 | false")\n'
             'print(" 2 | 17850 | France         | 2024-06-15 | NULL       | true")\n'
             'print("\\nFatos antigos apontam para sk=1 (UK); fatos novos para sk=2 (France).")\n'
             'print("Relatórios históricos continuam corretos — sem reescrever a fato.")'),
        teoria(
            "18. Como implementar SCD2 no Databricks — as 3 opções",
            "**Opção A — `APPLY CHANGES INTO` (Delta Live Tables, padrão da Medallion)** — declarativa, "
            "gerencia `valid_from/to/is_current` sozinha. É o que usamos na Semana 8:\n"
            "```python\n"
            "@dlt.table\n"
            "def dim_cliente_scd2():\n"
            "    return dlt.apply_changes(\n"
            "        target='dim_cliente', source='stg_cliente',\n"
            "        keys=['nk_cliente'], sequence_by='updated_at',\n"
            "        stored_as_scd_type=2)\n"
            "```\n"
            "**Opção B — `MERGE` + lógica de vigência** — manual, para notebooks sem DLT.\n"
            "**Opção C — `DeltaTable.merge` (Python)** — mesma lógica, API DataFrame.\n\n"
            "Nunca faça SCD2 com `overwrite` — você apagaria o histórico.",
        ),
        pratica(
            "SCD1 vs SCD2 — quando dói escolher errado",
            "Um caso real para fixar:",
        ),
        md("**Cenário**: o cliente 17850 aparece como `United Kingdom` em 2010 e `France` em 2024.\n\n"
           "- **Se usar SCD1** (sobrescreve): todo o histórico de 2010–2024 passa a dizer `France`. "
           "Relatório de 'vendas por país em 2011' fica errado. Mas é simples e a dimensão tem 1 linha por cliente.\n"
           "- **Se usar SCD2** (nova linha): 2010–2024 continua `UK` (sk=1), 2024+ vira `France` (sk=2). "
           "Histórico preservado, mas a dimensão dobra de tamanho e todo join precisa considerar `is_current`.\n\n"
           "**Decisão**: Relatórios históricos precisam estar corretos? → SCD2. Correção de cadastro? → SCD1. "
           "No varejo, `dim_cliente` (endereço) = SCD2; `dim_produto` (descrição corrigida) = SCD1."),
        teoria(
            "19. SCD avançados que caem em entrevista sênior",
            "- **SCD4**: mantém `dim_cliente` (só atuais) + `dim_cliente_hist` (todas as versões). A fato aponta para a atual; "
            "quem precisa de histórico join com a hist. Mantém a dimensão 'quente' pequena.\n"
            "- **SCD6 (1+2+3)**: guarda `cidade_atual` (SCD1, sempre atualizado), `cidade_hist` (SCD2, vigência) e `cidade_anterior` (SCD3). "
            "Permite responder 'onde o cliente mora hoje' e 'onde morava na época da venda' na mesma linha.\n"
            "- **SCD7**: separa atributos voláteis (ex.: `status_credito`) em outrigger SCD2, mantendo o núcleo SCD1.\n\n"
            "Você não precisa implementar SCD4/6/7 no curso — mas **saber explicar** mostra senioridade.",
        ),

        # =======================================================================
        # BLOCO 7 — CASOS AVANÇADOS
        # =======================================================================
        teoria(
            "20. Casos avançados que separam júnior de sênior",
            "**1. Late-arriving dimension** — o fato chega antes da dimensão (venda com `CustomerID` que ainda não existe em `dim_cliente`). "
            "Solução: criar linha 'inferred member' (só NK, resto NULL) e preencher depois (SCD1).\n\n"
            "**2. Late-arriving fact** — fato antigo chega atrasado (venda de 2024-01 chega em março). "
            "Solução: inserir na fato e **recalcular agregados do Ouro** (não só append).\n\n"
            "**3. Many-to-many (N:N)** — venda com múltiplos vendedores. Solução: **bridge table** + **weight factor**.\n"
            "```\n"
            "fato_vendas ── bridge_venda_vendedor ── dim_vendedor\n"
            "  receita=100       vendedor A (peso 0.6) → 60\n"
            "                    vendedor B (peso 0.4) → 40\n"
            "```\n"
            "Sem weight, a receita seria contada 2x.\n\n"
            "**4. Factless + Bridge** — `fato_aluno_curso` (aluno fez quais cursos?) sem medida, com bridge para múltiplos cursos.\n\n"
            "**5. Mini-dimensão** — atributos voláteis (ex.: `score_credito` que muda todo mês) viram `dim_cliente_mini` separada, "
            "evitando SCD2 explosivo em `dim_cliente`. A fato referencia as duas.\n\n"
            "**6. Heterogeneous products** — produtos com atributos distintos (livro tem ISBN, roupa tem tamanho). "
            "Solução: **dim_produto** com colunas genéricas + `dim_produto_livro` / `dim_produto_roupa` (subtipo) ou JSON Variant.",
        ),
        pratica(
            "Bridge N:N na prática — venda com 2 vendedores",
            "Veja como o weight evita dupla contagem:",
        ),
        code('# Fato (1 venda) + bridge (2 vendedores) + weight\n'
             'fato = [("NF001", 100.0)]  # 1 venda, receita 100\n'
             'bridge = [("NF001", "VEND_A", 0.6), ("NF001", "VEND_B", 0.4)]\n'
             '# Receita por vendedor = receita * weight\n'
             'for _, vend, w in bridge:\n'
             '    print(f"{vend}: {100*w:.0f} (100 x {w})")\n'
             'print("\\nSem weight, cada vendedor pareceria ter vendido 100 — total 200 (errado).")\n'
             'print("Com weight, total continua 100 — correto.")'),

        # =======================================================================
        # BLOCO 8 — MEDALLION MAPEADA
        # =======================================================================
        teoria(
            "21. Medallion × Modelagem — onde cada coisa vive",
            "| Camada | Conteúdo | Modelagem | Chave | SCD | Exemplo |\n"
            "|---|---|---|---|---|---|\n"
            "| **Bronze** | Dado cru, como chegou | Nenhuma — espelho da origem | NK da origem | Não | `workspace.bronze.vendas_bronze` (append-only, `_ingested_at`) |\n"
            "| **Prata** | Dado limpo, tipado, deduplicado | **Star completo**: dimensões + fatos atômicos | **SK** | **SCD1/2 aqui** | `workspace.prata.dim_cliente` (SCD2), `workspace.prata.fato_vendas` (grain atômico) |\n"
            "| **Ouro** | Agregados de negócio | **Marts denormalizados** (1 Star → 1 mart) | SK do agregado | Não (derivado) | `workspace.ouro.vendas_por_dia`, `workspace.ouro.receita_por_pais` |\n\n"
            "**Fluxo**: Bronze (raw) → Prata (dimensional, SCD) → Ouro (mart, agregado). "
            "Essa é a frase que você repete em entrevista: 'Bronze append-only, Prata dimensional SCD, Ouro mart agregado.'",
        ),
        pratica(
            "O que NÃO fazer em cada camada",
            "Regras que salvam o projeto:",
        ),
        md("- **Bronze NUNCA** modela: sem joins, sem SK, sem SCD, sem `DROP`. É o 'HD externo' — se perder, não tem como reconstituir.\n"
           "- **Prata NUNCA** agrega: grain atômico + dimensões. Se agregar na Prata, você perde detalhe para o Ouro.\n"
           "- **Ouro NUNCA** recebe dado cru: só consome Prata. Se o Ouro lê Bronze direto, você fura a governança e a linhagem.\n"
           "- **Nenhuma camada lê 'para trás'**: Ouro não alimenta Prata; Prata não alimenta Bronze. Fluxo é **sempre para frente**."),

        teoria(
            "22. Prata em detalhes — o Data Warehouse dimensional dentro do Lakehouse",
            "A Prata do nosso projeto tem:\n\n"
            "```\n"
            "dim_cliente  (SCD2)  — sk_cliente PK, nk_cliente, nome, país, valid_from/to, is_current\n"
            "dim_produto  (SCD1)  — sk_produto PK, StockCode NK, Description, categoria\n"
            "dim_tempo             — sk_tempo PK, data, ano, mês, trimestre, dia_semana (conformed)\n"
            "dim_loja     (SCD1)  — sk_loja PK, Country NK\n"
            "fato_vendas           — PK = (sk_cliente, sk_produto, sk_tempo, sk_loja) + medidas\n"
            "foto_estoque (futuro) — snapshot diário, semi-aditivo\n"
            "```\n\n"
            "Tudo **tipado** (TIMESTAMP, não STRING), **deduplicado** (`dropDuplicates`), **validado** "
            "(constraints, expectations) e **idempotente** (`overwrite` ou `MERGE` + `APPLY CHANGES`). "
            "É aqui que vivem `CHECK (Quantity > 0)` e `NOT NULL (CustomerID)`.",
        ),
        pratica(
            "Prata na prática — o esqueleto que vamos materializar na Semana 4",
            "Este é o código que a Semana 4 executa. Entenda cada linha:",
        ),
        code('# ESQUELETO da Prata — Semana 4 materializa isso de verdade\n'
             'from pyspark.sql.functions import col, row_number, sha2, current_timestamp\n'
             'from pyspark.sql.window import Window\n'
             'w = Window.orderBy("CustomerID")\n'
             '# dim_cliente SCD2 (simplificada — Semana 8 usa APPLY CHANGES)\n'
             'bronze = spark.table("workspace.bronze.vendas_bronze")\n'
             'dim_cliente = (bronze.select("CustomerID", "Country").dropDuplicates(["CustomerID"])\n'
             '    .withColumn("sk_cliente", row_number().over(w))\n'
             '    .withColumn("valid_from", current_timestamp())\n'
             '    .withColumn("valid_to", col("valid_from").cast("timestamp").alias("valid_to"))  # NULL = atual\n'
             '    .withColumn("is_current", col("valid_from").isNotNull()))\n'
             'print("dim_cliente: SK + vigência SCD2 (esqueleto)")\n'
             'print("Na Semana 8, valid_from/to/is_current são geridos por APPLY CHANGES.")'),
        teoria(
            "23. Ouro em detalhes — os marts que o usuário vê",
            "Se a Prata é o 'estoque organizado', o Ouro é a 'vitrine' — poucas tabelas, nomes de negócio, "
            "sem SK exposto (ou com SK simplificado), prontas para `SELECT *`.\n\n"
            "| Ouro | Grain | Para quem | Pergunta que responde |\n"
            "|---|---|---|---|\n"
            "| `vendas_por_dia` | dia | BI / ML (forecast) | 'Como foi hoje vs ontem?' |\n"
            "| `receita_por_pais` | país | Diretoria | 'Onde vendemos mais?' |\n"
            "| `top_produtos` | produto | Compras | 'O que mais vende?' |\n"
            "| `vendas_por_dia_pais` | dia × país | BI drill-down | 'Como foi o UK ontem?' |\n\n"
            "O Ouro é **derivado**: `CREATE OR REPLACE TABLE ... AS SELECT ... FROM Prata GROUP BY ...`. "
            "Se a Prata mudar, o Ouro recalcula. Nunca edite Ouro manualmente — ele é **efêmero** por design.",
        ),
        teoria(
            "24. Implementação no Databricks — Delta, DLT, UC e performance a serviço da modelagem",
            "| Recurso do Databricks | Papel na modelagem |\n"
            "|---|---|\n"
            "| **Delta Lake** (`_delta_log`, Time Travel, `MERGE`, CDF) | SCD sem medo: versiona, audita e recupera |\n"
            "| **DLT `APPLY CHANGES INTO`** | SCD2 declarativo (sem MERGE manual) |\n"
            "| **Constraints (`CHECK`, `NOT NULL`)** | Garante grain e medidas na Prata (falha a transação se violar) |\n"
            "| **Expectations (`expect_or_drop`)** | Qualidade no pipeline (ex.: `Quantity > 0`) |\n"
            "| **Liquid Clustering (`CLUSTER BY`)** | Performance da fato sem particionar demais |\n"
            "| **Unity Catalog (tags, linhagem, RLS)** | Governança: `PII` tag em `dim_cliente`, lineage Bronze→Ouro |\n"
            "| **Volumes** | Arquivos de stage (não tabelas) |\n"
            "| **Genie / Dashboards** | Consumo do Ouro em linguagem natural |\n\n"
            "Modelagem sem Delta/UC é **teoria**; com eles é **produção**.",
        ),
        pratica(
            "Delta a favor da modelagem — 3 exemplos que salvam o dia",
            "Rode e entenda por que Delta é o melhor amigo do modelador:",
        ),
        code('# 1) Time Travel: "como estava a dimensão ontem?" — auditoria de SCD\n'
             'df_ontem = spark.read.format("delta").option("timestampAsOf", "2024-06-14") \\\n'
             '    .table("workspace.prata.dim_cliente")\n'
             'print("Time Travel: dimensão como era em 2024-06-14 (sem recriar nada).")'),
        code('# 2) CDF: "o que mudou na dimensão?" — alimenta o Ouro incremental\n'
             'df_mudancas = spark.read.format("delta").option("readChangeFeed", "true") \\\n'
             '    .option("startingVersion", 5).table("workspace.prata.dim_cliente")\n'
             'print("CDF: mudanças desde a versão 5 — base para CDC e auditoria.")'),
        code('# 3) Constraint: grain violado = transação falha (não dado sujo)\n'
             'sql_constraint = """\n'
             'ALTER TABLE workspace.prata.fato_vendas\n'
             '  ADD CONSTRAINT pk_fato_nulo CHECK (sk_cliente IS NOT NULL AND sk_produto IS NOT NULL);\n'
             '-- Se uma carga tentar inserir fato sem dimensão, a transação falha inteira (ACID).\n'
             '"""\n'
             'print(sql_constraint)'),

        # =======================================================================
        # BLOCO 9 — BUS MATRIX E PROCESSO
        # =======================================================================
        teoria(
            "25. A Bus Matrix — o mapa do Data Warehouse inteiro em 1 página",
            "A **Dimensional Bus Matrix** cruza **processos de negócio** (linhas) com **dimensões conformadas** (colunas). "
            "É o documento que impede o caos: toda nova fato deve reutilizar dimensões já conformadas.\n\n"
            "```\n"
            "                    │ dim_cliente │ dim_produto │ dim_tempo │ dim_loja │ dim_vendedor │\n"
            "────────────────────┼─────────────┼─────────────┼───────────┼──────────┼──────────────┤\n"
            "fato_vendas         │      X      │      X      │     X     │    X     │              │\n"
            "foto_estoque        │             │      X      │     X     │    X     │              │\n"
            "fato_atendimento    │      X      │             │     X     │    X     │      X       │\n"
            "```\n\n"
            "Se um novo projeto propõe criar `dim_cliente2`, a Bus Matrix grita: 'Use a conformed `dim_cliente`!'",
        ),
        pratica(
            "A Bus Matrix do nosso curso — e seu próximo passo",
            "Vamos desenhar a Bus Matrix do varejo. Este é o exercício que você leva para entrevista:",
        ),
        code('# Bus Matrix do projeto (Prata atual + futuro)\n'
             'import pandas as pd\n'
             'bus = pd.DataFrame({\n'
             '    "processo": ["fato_vendas", "foto_estoque_diaria", "fato_devolucao (futuro)"],\n'
             '    "dim_cliente": ["X", "", "X"],\n'
             '    "dim_produto": ["X", "X", "X"],\n'
             '    "dim_tempo":   ["X", "X", "X"],\n'
             '    "dim_loja":    ["X", "X", ""],\n'
             '})\n'
             'display(bus)\n'
             'print("Toda nova fato deve reutilizar estas dimensões — é a integração do DW.")'),
        teoria(
            "26. O processo de modelagem — do requisito ao deploy",
            "1. **Entrevistar o negócio** — 'O que você decide com esses dados?' (não 'que relatório você quer?').\n"
            "2. **Listar processos e grains** — 1 processo = 1 fato.\n"
            "3. **Desenhar a Bus Matrix** — dimensões conformadas.\n"
            "4. **Detalhar cada dimensão** — atributos, hierarquias, SCD, fonte.\n"
            "5. **Detalhar cada fato** — medidas, additivity, FKs.\n"
            "6. **Prototipar em SQL** — `CREATE TABLE` + `INSERT` de exemplo, validar com o usuário.\n"
            "7. **Implementar na Prata** — DLT + expectations + `APPLY CHANGES`.\n"
            "8. **Publicar Ouro e documentar** — `COMMENT ON TABLE`, tags UC, linhagem, dashboard.\n\n"
            "Pular direto para o passo 7 é o erro #1 de iniciantes.",
        ),

        # =======================================================================
        # BLOCO 10 — BOAS PRÁTICAS, ANTIPATTERNS E VALIDAÇÃO
        # =======================================================================
        teoria(
            "27. As 20 melhores práticas — checklist de produção",
            "1. Grain atômico na Prata, agregados só no Ouro.\n"
            "2. Fatos com SK, nunca NK.\n"
            "3. Dimensões com `sk_*` (PK), `nk_*` e `dk_*` quando houver SCD2.\n"
            "4. `is_current` + `valid_from/to` em toda SCD2.\n"
            "5. `row_hash` para detectar mudanças sem comparar 20 colunas.\n"
            "6. Constraints na Prata: `NOT NULL` em SKs, `CHECK` em medidas.\n"
            "7. Expectations no DLT: `Quantity > 0`, `CustomerID IS NOT NULL`.\n"
            "8. Idempotência: `MERGE` ou `APPLY CHANGES`, nunca `append` cego em dimensão.\n"
            "9. Dimensões conformadas — 1 `dim_tempo`, não 3 cópias.\n"
            "10. Nomes de negócio no Ouro (`receita_por_pais`, não `agg_02`).\n"
            "11. `COMMENT ON TABLE/COLUMN` em tudo — documentação viva.\n"
            "12. Tags UC (`PII`, `financeiro`) + linhagem ativa.\n"
            "13. `CLUSTER BY` na fato por colunas de filtro (não particione SCD2 por `is_current`).\n"
            "14. Bridge com `weight` — nunca dupla contagem.\n"
            "15. Junk dimension para flags — não polua a fato.\n"
            "16. Teste de grain: `COUNT(*) = COUNT(DISTINCT PK)` deve ser 0 duplicatas.\n"
            "17. Time Travel habilitado — auditoria gratuita.\n"
            "18. CDF ligado em dimensões SCD2 (`delta.enableChangeDataFeed = true`).\n"
            "19. Ouro recalculável: `CREATE OR REPLACE` a partir da Prata, sem estado próprio.\n"
            "20. Bus Matrix versionada no Git — o contrato do DW.",
        ),
        teoria(
            "28. Os 7 antipatterns que destroem um Lakehouse",
            "1. **Bronze modelado** — modelar no Bronze impede reprocessamento.\n"
            "2. **Fato sem grain declarado** — ninguém sabe o que uma linha significa.\n"
            "3. **NK na fato** — quebra quando a origem muda.\n"
            "4. **SCD2 sem `is_current`** — todo `SELECT` precisa de `MAX(valid_from)`.\n"
            "5. **Snowflake desnecessário** — normalizar `dim_produto` em 4 tabelas só para 'economizar' 10 MB.\n"
            "6. **Ouro lendo Bronze** — fura a Prata, perde SCD e qualidade.\n"
            "7. **Dimensão gigante sem mini-dim** — `dim_cliente` com 50 colunas voláteis explode em SCD2.\n\n"
            "Se você evitar esses 7, já está no top 10% dos modeladores.",
        ),
        pratica(
            "Validação do modelo — as 7 perguntas que todo modelo deve responder",
            "Antes de chamar o modelo de 'pronto', ele deve passar neste teste:",
        ),
        code('# Checklist de validação — responda SIM para todas\n'
             'checklist = [\n'
             '    "1. Posso explicar o grain em 1 frase sem gaguejar?",\n'
             '    "2. COUNT(*) = COUNT(DISTINCT PK) — zero duplicatas?",\n'
             '    "3. Toda FK da fato existe na dimensão? (sem órfãs)",\n'
             '    "4. Medidas não-aditivas estão documentadas como tal?",\n'
             '    "5. SCD2 tem is_current + valid_from/to + row_hash?",\n'
             '    "6. Dimensões são conformed (Bus Matrix)?",\n'
             '    "7. Um usuário de negócio entende os nomes do Ouro?",\n'
             ']\n'
             'for q in checklist:\n'
             '    print(f"☐ {q}")\n'
             'print("\\nSe algum ☐ ficar em branco, volte ao design.")'),
        teoria(
            "29. Do modelo ao consumo — BI, Genie, ML e RAG",
            "- **BI (Dashboards)**: Ouro denormalizado → `SELECT * FROM workspace.ouro.vendas_por_dia` sem joins.\n"
            "- **Genie (linguagem natural)**: Genie lê o Ouro + `COMMENT` das colunas para responder 'qual a receita por país?'.\n"
            "- **ML (Feature Store)**: features vêm de Prata/Ouro tipadas e SCD-correctas.\n"
            "- **RAG (Vector Search)**: descrições de `dim_produto` viram chunks com `StockCode` como metadata.\n\n"
            "Modelagem bem feita **serve todos** — mal feita, serve ninguém.",
        ),

        # =======================================================================
        # BLOCO 10B — MEDALLION NA PRÁTICA DO ARQUITETO
        # =======================================================================
        teoria(
            "30. Medallion além do 'Bronze → Prata → Ouro' — as variações que um arquiteto domina",
            "O Medallion de “3 camadas” é o **esqueleto**. Em produção, ele ganha musculatura:\n\n"
            "```\n"
            "  ┌─────────┐\n"
            "  │ LANDING │  arquivos crus como chegaram (S3/ADLS), sem ACID, com _ingested_at\n"
            "  └────┬────┘  (às vezes fora do Lakehouse; às vezes Bronze = Landing)\n"
            "       │ Auto Loader / COPY INTO / Kafka\n"
            "  ┌────▼────┐\n"
            "  │  BRONZE │  Delta ACID, schema-on-read, append-only, histórico intocável\n"
            "  └────┬────┘  vacuuming longo, CDF ligado, tag `pii=true`\n"
            "       │ DLT / Structured Streaming + Expectations\n"
            "  ┌────▼────┐\n"
            "  │  PRATA  │  Star conformed, SCD1/2, tipado, deduplicado, constraints\n"
            "  └────┬────┘  Liquid Clustering por (sk_tempo, sk_produto)\n"
            "       │ Gold pipelines (batch ou streaming)\n"
            "  ┌────▼────┐\n"
            "  │   OURO  │  Marts por domínio OU tabelões wide — ver estratégias 31–34\n"
            "  └────┬────┘\n"
            "       │ BI / ML / RAG / API\n"
            "  ┌────▼────┐\n"
            "  │ CONSUMO │  Dashboard, Genie, Feature Store, endpoint\n"
            "  └─────────┘\n"
            "```\n\n"
            "**Variações comuns**:\n"
            "- **Bronze = Landing**: simplifica, mas perde o “antes e depois” da ingestão.\n"
            "- **Quarantine / Dead-letter** entre Bronze→Prata: linhas que falham expectation vão para `quarantine.*` em vez de travar o pipeline.\n"
            "- **Ouro em 2 níveis**: `ouro_core` (marts canônicos) + `ouro_mart_*` (marts por equipe).",
        ),
        teoria(
            "31. Estratégia A — Classic Kimball sobre Medallion (a mais usada, a que o curso adota)",
            "**Ideia**: Star conformed na Prata; marts desnormalizados no Ouro; fatos sempre aditivos.\n\n"
            "```\n"
            "  OLTP/SaaS ──► BRONZE (raw) ──► PRATA (Star: dim + fato, SCD2) ──► OURO (marts)\n"
            "                      │                    │                          │\n"
            "                      │ _ingested_at       │ sk_*, is_current         │ receita_por_pais\n"
            "                      │ sem PK             │ constraints              │ vendas_por_dia\n"
            "```\n\n"
            "| Quando usar | Vantagens | Custos |\n"
            "|---|---|---|\n"
            "| 80% dos casos; BI + ML precisam do mesmo núcleo | Reuso máximo, Bus Matrix, SCD correto | Ouro precisa ser bem desenhado para não virar “Prata 2” |\n\n"
            "**Regra**: 1 Star = 1 processo de negócio (vendas). Novo processo = novo Star que **reusa** dimensões conformadas.",
        ),
        teoria(
            "32. Estratégia B — Data Vault 2.0 sobre Medallion (auditoria extrema)",
            "- **Bronze**: Vault Raw — Hub (chave de negócio), Link (relação), Satellite (atributos + hash, com `load_date`).\n"
            "- **Prata**: Vault Business — mesma estrutura + regras de negócio.\n"
            "- **Ouro**: Stars derivados do Vault (PIT/Bridge para SCD2).\n\n"
            "```\n"
            "  hub_cliente ─┬─ sat_cliente_endereco (hash, load_date)\n"
            "               └─ link_cliente_pedido ── hub_pedido\n"
            "```\n\n"
            "| Quando usar | Vantagens | Custos |\n"
            "|---|---|---|\n"
            "| Auditoria total, múltiplas fontes com chaves conflitantes, linhagem exigida | Rastreabilidade perfeita, paraleliza ingestão | Complexidade alta; precisa gerar Stars no Ouro para BI consumir |\n",
        ),
        teoria(
            "33. Estratégia C — One Big Table (OBT) / Wide Table no Ouro",
            "O Ouro vira **1 tabela larga denormalizada** (tudo joinado): `w_vendas` com 80 colunas — produto, cliente, tempo, loja já resolvidos.\n\n"
            "```\n"
            "  Prata (Star) ──► Ouro: w_vendas (fato + dims achatadas)\n"
            "                   SELECT f.*, c.nome, c.pais, p.categoria, t.ano, t.mes FROM fato_vendas f\n"
            "                   JOIN dim_cliente c USING (sk_cliente) ...\n"
            "```\n\n"
            "| Quando usar | Vantagens | Custos |\n"
            "|---|---|---|\n"
            "| BI self-service que não quer join; export para Excel/Sheets | Uma tabela responde tudo; Genie/RAG adoram | Redundância; precisa recalc toda se Prata muda; não serve para SCD2 histórico fino |\n\n"
            "**Híbrido recomendado**: mantenha **marts** (receita_por_pais) **e** 1 OBT para exploração. São complementares.",
        ),
        teoria(
            "34. Estratégias D e E — Feature Store Gold e Streaming Medallion",
            "**D. Feature Store Gold** — o Ouro vira **feature tables** para ML:\n"
            "```\n"
            "  Prata (fato_vendas) ──► Ouro: feature_store.cliente_360 (features por cliente)\n"
            "                        features: recencia, frequencia, ticket_medio, categoria_favorita\n"
            "```\n"
            "Ouro versionado, com `feature_timestamp` e `event_timestamp` (point-in-time correctness). No Databricks: **Feature Store** nativo lê direto do Ouro.\n\n"
            "**E. Streaming Medallion** — Bronze e Prata em **Structured Streaming**:\n"
            "```\n"
            "  Kafka/Auto Loader (stream) ──► Bronze (streaming table) ──► Prata (streaming + APPLY CHANGES) ──► Ouro (materialized view)\n"
            "```\n"
            "Latência de segundos. Use **DLT com `APPLY CHANGES`** e `skipChangeCommits=true` na Prata para não travar com SCD2 em stream.\n\n"
            "| Quando usar D | Quando usar E |\n"
            "|---|---|\n"
            "| ML em produção precisa de features frescas | Dashboard operacional / detecção de fraude em tempo real |",
        ),
        teoria(
            "35. Fluxo 1 — Ingestão até o Bronze (batch, streaming e CDC)",
            "**Batch (Auto Loader — padrão do curso)**:\n"
            "```\n"
            "  S3: s3://landing/vendas/2024/06/*.csv\n"
            "       │\n"
            "       ├─ Auto Loader (cloudFiles) ──► workspace.bronze.vendas_bronze\n"
            "       │   - `cloudFiles.inferColumnTypes=true`\n"
            "       │   - `cloudFiles.schemaLocation` para evolução\n"
            "       │   - expectation: `Quantity > 0`\n"
            "       └─ quarantine.vendas_rejected (falhas)\n"
            "```\n\n"
            "**Streaming (Kafka/Kinesis)**:\n"
            "```\n"
            "  Kafka topic `vendas` ──► readStream.format('kafka') ──► Bronze streaming table (append-only)\n"
            "```\n\n"
            "**CDC (Change Data Capture)** — origem OLTP com `UPDATE/DELETE`:\n"
            "```\n"
            "  Debezium/CDC feed ──► Bronze CDC (op, before/after) ──► Prata com APPLY CHANGES (SCD1/2)\n"
            "```\n\n"
            "**Critério do arquiteto**: volume < 1 GB/dia → batch horário; > 1 GB/hora ou SLA < 5 min → streaming; origem com updates → CDC.",
        ),
        pratica(
            "Ingestão na prática — Auto Loader para o Bronze",
            "O padrão que o curso usa (Semana 5). Releia com olhos de arquiteto:",
        ),
        code('# Padrão Auto Loader → Bronze (idempotente, com quarantine)\n'
             'bronze = (spark.readStream.format("cloudFiles")\n'
             '  .option("cloudFiles.format", "csv")\n'
             '  .option("cloudFiles.schemaLocation", "/Volumes/workspace/bronze/_schema/vendas")\n'
             '  .option("cloudFiles.inferColumnTypes", "true")\n'
             '  .load("s3://landing/vendas/"))\n'
             '# Em DLT, o quarantine vira: @dlt.expect_or_fail / expect_or_drop\n'
             'print("Bronze: Auto Loader + schemaLocation + quarantine = ingestão resiliente")'),
        teoria(
            "36. Fluxo 2 — Bronze → Prata (onde a modelagem acontece)",
            "```\n"
            "  workspace.bronze.vendas_bronze (raw, 540k linhas, com _ingested_at)\n"
            "       │\n"
            "       ├─ 1. Limpeza: trim, upper, cast, filter Quantity>0  (expectations)\n"
            "       ├─ 2. Deduplicação: dropDuplicates([InvoiceNo, StockCode])\n"
            "       ├─ 3. Tipagem: to_timestamp(InvoiceDate), DOUBLE price\n"
            "       ├─ 4. SK: row_number / sha2 / sequence\n"
            "       ├─ 5. SCD: dim_cliente (SCD2, APPLY CHANGES), dim_produto (SCD1)\n"
            "       └─ 6. Fato: join com dims por SK + medidas\n"
            "            │\n"
            "            ▼\n"
            "       workspace.prata.dim_cliente (SCD2)  ← is_current, valid_from/to\n"
            "       workspace.prata.dim_produto (SCD1)  ← overwrite por StockCode\n"
            "       workspace.prata.fato_vendas          ← grain atômico, FK = SK\n"
            "```\n\n"
            "**Decisões do arquiteto aqui**:\n"
            "- Grain atômico ou agregado na Prata? → **Atômico** (flexibilidade).\n"
            "- Qual dimensão é SCD2? → Só as que precisam de histórico (cliente). O resto SCD1.\n"
            "- Constraint ou expectation? → Constraint na Prata (falha transação); expectation no DLT (quarantine).",
        ),
        pratica(
            "Prata — o join que materializa o Star",
            "Este é o coração da modelagem. Na Semana 4 ele roda de verdade:",
        ),
        code('# Bronze → Prata: join por NK, grava com SK (Star)\n'
             'fato = (bronze.alias("b")\n'
             '  .join(dim_cliente.filter("is_current"), bronze.CustomerID == dim_cliente.nk_cliente)\n'
             '  .join(dim_produto, bronze.StockCode == dim_produto.StockCode)\n'
             '  .join(dim_tempo, bronze.InvoiceDate == dim_tempo.data)\n'
             '  .selectExpr("sk_cliente", "sk_produto", "sk_tempo", "Quantity", "UnitPrice", "Quantity*UnitPrice as receita"))\n'
             'print("Fato com SK: grain preservado, FK íntegra, medida aditiva")'),
        teoria(
            "37. Fluxo 3 — Prata → Ouro (marts, tabelões e agregados)",
            "```\n"
            "  workspace.prata.fato_vendas (atômico, 540k linhas)\n"
            "       │\n"
            "       ├──► workspace.ouro.vendas_por_dia       (GROUP BY sk_tempo → dia)\n"
            "       ├──► workspace.ouro.receita_por_pais     (GROUP BY Country)\n"
            "       ├──► workspace.ouro.w_vendas             (OBT: fato + dims achatadas)\n"
            "       └──► workspace.ouro.feature_cliente_360  (Feature Store: recencia, frequencia)\n"
            "```\n\n"
            "**Estratégia por domínio (Data Mesh leve)**:\n"
            "- `ouro_financeiro.*` — time de Finanças é dono.\n"
            "- `ouro_marketing.*` — time de Marketing é dono.\n"
            "- Ambos leem da **mesma Prata conformed** — sem duplicar lógica.\n\n"
            "**Padrão de refresh**:\n"
            "- Ouro agregado → `CREATE OR REPLACE TABLE ... AS SELECT ... FROM Prata GROUP BY ...` (recalc total, barato).\n"
            "- Ouro incremental → `MERGE` por `sk_tempo` (só dia novo).\n"
            "- Ouro streaming → `MATERIALIZED VIEW` sobre Prata streaming.",
        ),
        pratica(
            "Ouro — 1 Star, 3 consumos diferentes",
            "Mesma Prata, 3 Ouros para 3 públicos:",
        ),
        code('# Mesmo fato, 3 Ouros\n'
             '# 1) Mart agregado (BI): 1 linha por dia\n'
             'ouro_dia = fato.groupBy("sk_tempo").agg({"receita": "sum"}).withColumnRenamed("sum(receita)", "receita_dia")\n'
             '# 2) OBT (exploração): 1 linha = 1 venda com tudo achatado\n'
             'obt = fato.join(dim_cliente, "sk_cliente").join(dim_produto, "sk_produto")  # wide\n'
             '# 3) Feature (ML): 1 linha por cliente\n'
             'feat = fato.groupBy("sk_cliente").agg({"receita": "avg", "Quantity": "sum"})\n'
             'print("3 Ouros, 1 Prata — reuso sem duplicar regra")'),
        teoria(
            "38. Fluxo 4 — Ouro → Consumo (BI, Genie, ML, RAG, API)",
            "```\n"
            "  workspace.ouro.* ──┬──► Dashboard (SQL Warehouse, 2X-Small)\n"
            "                     ├──► Genie (NL → SQL sobre Ouro + COMMENT)\n"
            "                     ├──► Feature Store → Modelo → Endpoint (Mosaic AI)\n"
            "                     ├──► Vector Search (dim_produto.Description → chunks)\n"
            "                     └──► API / DLT downstream (Delta Sharing)\n"
            "```\n\n"
            "O Ouro **nunca** é editado à mão. Ele é **derivado e recalculável**. Se apagar, `REFRESH` recria. "
            "Por isso o catálogo marca `COMMENT ON TABLE workspace.ouro.* IS 'MART — derivado de prata.fato_vendas'` "
            "e a linhagem UC mostra Bronze → Prata → Ouro automaticamente.",
        ),
        teoria(
            "39. Matriz de decisão — qual arquitetura escolher?",
            "| Pergunta | Se SIM → | Se NÃO → |\n"
            "|---|---|---|\n"
            "| Precisa auditoria total de cada ingestão? | Data Vault no Bronze/Prata | Kimball direto |\n"
            "| BI quer 1 tabela sem joins? | OBT no Ouro (além dos marts) | Só marts |\n"
            "| ML precisa de features frescas? | Feature Store Gold (com `event_timestamp`) | Features na Prata bastam |\n"
            "| Latência < 1 min? | Streaming Medallion (DLT streaming) | Batch (Auto Loader horário) |\n"
            "| Dimensão tem 50+ atributos voláteis? | Mini-dim + outrigger | Tudo na dim principal |\n"
            "| Fato tem N:N (venda→vendedores)? | Bridge + weight | Fato simples |\n\n"
            "**Resposta de arquiteto em entrevista**: 'Depende do caso de uso — para o varejo do curso, Kimball + OBT + batch é o melhor custo/benefício; "
            "se fosse fraude em tempo real, eu usaria Streaming Medallion com Feature Store.'",
        ),
        teoria(
            "40. Performance e qualidade em cada camada — o checklist do arquiteto",
            "| Camada | Performance | Qualidade | Governança |\n"
            "|---|---|---|---|\n"
            "| **Bronze** | `OPTIMIZE` semanal (append-only gera many small files) | `expect_or_drop` (Quantity>0), `quarantine` | Tag `pii=true`, RLS não (ainda cru) |\n"
            "| **Prata** | `CLUSTER BY (sk_tempo, sk_produto)` na fato; `ZORDER` em dims SCD2 | `CHECK (sk_cliente IS NOT NULL)`, `NOT NULL`, `APPLY CHANGES` | `is_current` indexado, CDF ligado |\n"
            "| **Ouro** | `OPTIMIZE` + `VACUUM` (Ouro é recriado, retenção curta) | `CHECK (receita >= 0)` nos marts | `GRANT SELECT ON ouro.* TO bi_team` |\n\n"
            "**Regra de ouro**: Bronze otimiza **escrita** (append rápido); Prata otimiza **join** (SK); Ouro otimiza **leitura** (agregado, poucas linhas).",
        ),
        pratica(
            "Cluster e constraints — onde cada um mora",
            "Decore este mapa para a prova e para o design review:",
        ),
        code('# Onde cada otimização vive (arquiteto decide na criação da tabela)\n'
             'print("Bronze: TBLPROPERTIES (delta.enableChangeDataFeed=true) — para SCD2 futuro")\n'
             'print("Prata: CLUSTER BY (sk_tempo) na fato; CONSTRAINT CHECK (sk_cliente IS NOT NULL)")\n'
             'print("Ouro:   CLUSTER BY (Country) em receita_por_pais; VACUUM retain 0 HOURS (recalculável)")\n'
             'print("\\nPrata = join rápido; Ouro = scan rápido; Bronze = ingestão rápida")'),
        teoria(
            "41. Governança e observabilidade — o que o arquiteto não esquece",
            "- **Unity Catalog**: 1 catálogo por ambiente (`workspace` na Free, `prod`/`dev` em conta paga); `GRANT` no Ouro, não no Bronze.\n"
            "- **Linhagem**: `LINEAGE` mostra `vendas_bronze → fato_vendas → w_vendas` automaticamente (Delta CDF).\n"
            "- **Expectations (DLT)**: `expect_or_fail` no Bronze (trava pipeline se dado cru vier quebrado), `expect_or_drop` na Prata.\n"
            "- **Observabilidade**: `DESCRIBE HISTORY` + `AUDIT LOG` + métricas de DLT (linhas in/out/quarantine).\n\n"
            "Arquiteto que não desenha governança junto com modelagem entrega um castelo sem portas.",
        ),
        pratica(
            "O pipeline completo em 1 diagrama — cole no README",
            "Este é o diagrama que um arquiteto apresenta no design review:",
        ),
        md("```mermaid\n"
           "flowchart LR\n"
           "  A[Fontes: OLTP, SaaS, CSV] --> B[LANDING S3]\n"
           "  B -->|Auto Loader| C[BRONZE Delta]\n"
           "  C -->|DLT + Expectations| D[PRATA Star]\n"
           "  D --> E1[OURO Mart Dia]\n"
           "  D --> E2[OURO OBT w_vendas]\n"
           "  D --> E3[OURO Feature Store]\n"
           "  E1 & E2 & E3 --> F[Consumo: BI / Genie / ML / RAG]\n"
           "  C -.->|quarantine| G[Dead Letter]\n"
           "```\n\n"
           "> 💡 No Databricks: **DLT** orquestra `LANDING → BRONZE → PRATA → OURO` com `APPLY CHANGES` para SCD2 "
           "e `expectations` para quarantine — tudo declarativo."),

        # =======================================================================
        # BLOCO 11 — FECHAMENTO ATUALIZADO
        # =======================================================================
        dica_prova(
            "A DEA cobra: grain, fato vs dimensão, Star vs Snowflake, SCD1 vs SCD2. "
            "A DEP cobra: APPLY CHANGES (SCD2), bridge com weight, late-arriving, e Medallion × modelagem. "
            "Decore: 'Prata = Star com SCD, Ouro = mart agregado; SCD1 corrige, SCD2 historia; bridge precisa weight; late dimension = inferred member.'"
        ),
        exercicios([
            "Declare o grain de `fato_vendas` e de `foto_estoque_diaria` em 1 frase cada.",
            "Classifique: `dim_cliente`, `fato_vendas`, `dim_produto`, `foto_estoque` — quais são fatos e por quê?",
            "Crie uma junk dimension `dim_transacao` com 3 flags do varejo (ex.: é_presente, canal, tipo_pagamento). Quantas linhas ela teria?",
            "Desenhe o Star do varejo com `fato_vendas` no centro e 4 dimensões. Depois estenda para Galaxy adicionando `foto_estoque`.",
            "Cliente 17850 muda de 'United Kingdom' para 'France' em 2024-06-15. Escreva as 2 linhas SCD2 (sk, nk, país, valid_from, valid_to, is_current).",
            "Venda NF001 tem 2 vendedores (60%/40%) e receita 100. Sem weight, qual o total por vendedor? Com weight?",
            "Onde na Medallion vivem: (a) SCD2, (b) agregados por país, (c) dado cru com `_ingested_at`? Justifique.",
            "Preencha a Bus Matrix: linhas = fato_vendas, foto_estoque, fato_atendimento; colunas = dim_cliente, dim_produto, dim_tempo, dim_loja, dim_vendedor.",
        ]),
        gabarito([
            ("Grain",
             "`fato_vendas`: 1 linha = 1 item de 1 nota (atômico). `foto_estoque_diaria`: 1 linha = 1 produto × 1 dia (snapshot)."),
            ("Fato vs Dimensão",
             "Fatos: `fato_vendas` e `foto_estoque` (eventos/estados mensuráveis, muitas linhas, medidas). Dimensões: `dim_cliente` e `dim_produto` (contexto, poucas linhas, atributos). `foto_estoque` é fato mesmo com 1 linha por produto/dia — mede estoque."),
            ("Junk",
             "Ex.: `dim_transacao(is_presente, canal, tipo_pagamento)` — 2×3×3=18 combinações possíveis, mas só as que ocorrem viram linhas (ex.: 8). A fato referencia `sk_transacao` em vez de 3 colunas booleanas."),
            ("Star → Galaxy",
             "Star: fato_vendas no centro, dim_cliente/produto/tempo/loja ao redor. Galaxy: adicione foto_estoque compartilhando dim_produto e dim_tempo (conformed). Desenhe os dois fatos ligados às mesmas dimensões."),
            ("SCD2",
             "Antes: (1, 17850, UK, 2010-12-01, 2024-06-14, false). Depois: (2, 17850, France, 2024-06-15, NULL, true). Fatos antigos → sk=1; novos → sk=2."),
            ("Bridge weight",
             "Sem weight: cada vendedor = 100 (total 200, errado). Com weight: A=60, B=40 (total 100, correto). Weight evita dupla contagem."),
            ("Medallion",
             "(a) Prata — Star com SCD (dimensões versionadas). (b) Ouro — mart agregado denormalizado. (c) Bronze — append-only, sem modelagem. Fluxo sempre Bronze→Prata→Ouro."),
            ("Bus Matrix",
             "fato_vendas: X em cliente/produto/tempo/loja. foto_estoque: X em produto/tempo/loja. fato_atendimento: X em cliente/tempo/loja/vendedor. Produto e tempo são conformed (X em 2+ linhas)."),
        ]),
        footer([
            "Expliquei OLTP vs OLAP e Kimball vs Inmon em 2 minutos cada.",
            "Declarei o grain do projeto e validei com as 3 perguntas.",
            "Domino os 5 tipos de fato, 9 tipos de dimensão e 20 boas práticas.",
            "Implemento SCD1/2/3 e entendo SCD4/6/7 para entrevistas sênior.",
            "Mapeei Bronze (raw) → Prata (Star SCD) → Ouro (mart) na Medallion.",
            "Preenchi a Bus Matrix e sei evitar os 7 antipatterns.",
            "Pronto para materializar a Prata na Semana 4 e o SCD2 na Semana 8.",
        ]),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana2_dia5_databricks_sql_dashboards_alerts",
    [
        header(
            "2", "5", "Databricks SQL: dashboards, alertas e queries agendadas",
            "Publicar relatórios profissionais com o SQL Warehouse: visualizações, dashboards, "
            "queries agendadas e alertas.",
            "DAA, DEA (BI)", "Relatório SQL publicado com alerta",
            "✅ Free Edition",
        ),
        teoria(
            "Databricks SQL — a camada de BI",
            "Tudo o que você construiu em SQL pode virar **visualização → dashboard → alerta → "
            "query agendada**, direto sobre o Unity Catalog, sem cópia para outra ferramenta.\n\n"
            "Componentes:\n"
            "- **SQL Warehouse**: compute de BI (1 na Free, 2X-Small)\n"
            "- **Queries**: editor SQL com histórico\n"
            "- **Dashboards**: painéis com visualizações interativas\n"
            "- **Alerts**: gatilhos em condições (ex.: receita caiu 20%)\n"
            "- **Schedules**: queries rodando em horários (ex.: 8h diário)",
        ),
        pratica("Criando as queries de negócio",
            "Construa as visualizações de BI sobre o Ouro que será criado na Semana 4 — por ora "
            "usamos o Bronze para o dashboard de treino."),
        sql('-- KPI 1: receita por mês\n'
            'SELECT DATE_TRUNC("month", InvoiceDate) AS mes,\n'
            '       ROUND(SUM(Quantity * UnitPrice), 2) AS receita\n'
            'FROM workspace.bronze.vendas_bronze\n'
            'GROUP BY mes ORDER BY mes'),
        sql('-- KPI 2: top produtos\n'
            'SELECT StockCode, ROUND(SUM(Quantity * UnitPrice), 2) AS receita\n'
            'FROM workspace.bronze.vendas_bronze\n'
            'GROUP BY StockCode ORDER BY receita DESC LIMIT 10'),
        pratica("Montando o dashboard",
            "1. Em **Queries**, salve as 2 queries acima.\n"
            "2. Abra **Dashboards → Create Dashboard**.\n"
            "3. Adicione as queries; ajuste os tipos de visualização (line para série temporal, "
            "bar para ranking).\n"
            "4. **Publish** para ter um link compartilhável.",
        ),
        pratica("Alertas",
            "Crie um alerta que dispara quando a receita do mês cair."),
        sql('-- Query do alerta: receita do mês corrente vs mês anterior\n'
            'WITH rec AS (\n'
            '  SELECT DATE_TRUNC("month", InvoiceDate) mes, SUM(Quantity*UnitPrice) receita\n'
            '  FROM workspace.bronze.vendas_bronze GROUP BY mes)\n'
            'SELECT (receita - LAG(receita) OVER (ORDER BY mes)) / LAG(receita) OVER (ORDER BY mes) * 100\n'
            '       AS variacao_pct\n'
            'FROM rec ORDER BY mes DESC LIMIT 1'),
        pratica("Queries agendadas",
            "1. Na query salva, clique em **Schedule**.\n"
            "2. Frequência: diária às 08:00.\n"
            "3. **Send to**: e-mail (opcional; se o e-mail estiver configurado).\n"
            "4. Salve. A query rodará no warehouse quando ele estiver ativo.",
        ),
        dica_prova("A prova DAA cobra: tipos de visualização adequados ao dado (linha para "
                   "tempo, barra para ranking), alertas, e a diferença entre query agendada e "
                   "dashboard. No DEA, saber que BI consulta o catálogo via SQL Warehouse."),
        exercicios([
            "Qual visualização usar para série temporal? E para ranking?",
            "Crie um alerta que dispare quando vendas do dia < 1.000.",
            "Por que dashboards devem consultar o Ouro (e não o Bronze)?",
        ]),
        gabarito([
            ("Visualizações",
             "Série temporal = line chart; ranking = bar chart; distribuição = histogram; "
             "composição = stacked bar/pie."),
            ("Alerta de vendas",
             "Query: `SELECT COUNT(*) FROM workspace.bronze.vendas_bronze WHERE InvoiceDate >= current_date()` — "
             "Alerta condição `< 1000`."),
            ("Ouro vs Bronze",
             "Ouro é limpo, modelado e estável; Bronze é cru e append-only (pode conter "
             "duplicatas/erros). BI sobre Bronze gera números errados."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana2_dia6_simulado_parcial_dea_sql_uc",
    [
        header(
            "2", "6", "Simulado parcial DEA (domínio SQL + Unity Catalog) e fechamento",
            "Validar o aprendizado das Semanas 1–2 com 20 questões no formato da prova oficial "
            "DEA 2026 e fechar o ciclo da Semana 2.",
            "DEA (simulado)", "Resultado ≥ 70% no simulado",
            "✅ Free Edition",
        ),
        teoria(
            "Como funciona a prova real DEA",
            "A **Databricks Certified Data Engineer Associate** (2026):\n"
            "- ~45 questões, 120 min, Pearson VUE (online ou centro).\n"
            "- Domínios 2026: ELT with Spark SQL and Python · Unity Catalog (~30%) · Delta "
            "Lake · Lakeflow (pipelines e jobs) · qualidade de dados · medallion.\n"
            "- Validade: 2 anos (recertificação obrigatória).\n"
            "- Formato: múltipla escolha e múltiplas respostas. Cuidado com 'select all that apply'.",
        ),
        teoria(
            "Simulado 1 — SQL e Unity Catalog (20 questões)",
            "Responda **sem consultar** o material. Cada questão marca o domínio. "
            "Use uma folha para marcar A/B/C/D e depois compare com o gabarito no fim.",
        ),
        md("""### Questões (marque antes de olhar o gabarito)

**1.** Qual comando cria uma tabela gerenciada (managed) no Unity Catalog?
- A) `CREATE MANAGED TABLE t ...`
- B) `CREATE TABLE workspace.bronze.t ...` (USING DELTA)
- C) `CREATE EXTERNAL TABLE t ...`
- D) `CREATE TABLE t LOCATION '/mnt/x'`

**2.** O que acontece se uma escrita viola uma constraint CHECK?
- A) A linha é descartada e a escrita segue
- B) A transação inteira falha
- C) A constraint é removida automaticamente
- D) A escrita é redirecionada para outra tabela

**3.** Qual comando registra um DataFrame para consulta em SQL na mesma sessão?
- A) `df.saveAsTable()`
- B) `df.registerTempView()`
- C) `df.createOrReplaceTempView()`
- D) `spark.sql(df)`

**4.** Em `workspace.bronze.vendas`, qual é o nível intermediário?
- A) catálogo  B) schema  C) tabela  D) metastore

**5.** Qual dimensão de qualidade é violada por um CPF inválido?
- A) completude  B) unicidade  C) validade  D) consistência

**6.** O que `LAG(receita) OVER (ORDER BY mes)` retorna?
- A) a receita do mês seguinte  B) a receita do mês anterior
- C) o total acumulado  D) o ranking da receita

**7.** Para qual cenário o SCD2 é obrigatório?
- A) corrigir preço errado  B) manter histórico de endereço de cliente
- C) flag de ativo/inativo  D) agregar vendas por mês

**8.** Qual é a diferença entre `WHERE` e `HAVING`?
- A) iguais; WHERE é sinônimo
- B) WHERE filtra linhas antes da agregação; HAVING filtra o resultado da agregação
- C) HAVING filtra linhas antes; WHERE depois
- D) nenhuma

**9.** Onde ficam os dados de uma **managed table**?
- A) num external location apontando para o seu bucket
- B) no storage gerenciado pelo Unity Catalog
- C) no DBFS sempre  D) na memória do cluster

**10.** Qual formato NÃO tem ACID/Time Travel?
- A) Delta  B) Parquet puro  C) Delta com TBLPROPERTIES  D) Delta table

**11.** Qual comando lista as versões históricas de uma tabela Delta?
- A) `DESCRIBE HISTORY t`  B) `SELECT * FROM t HISTORY`
- C) `SHOW VERSIONS t`  D) `TIME TRAVEL t`

**12.** O que `%fs ls` faz?
- A) lista arquivos do Unity Catalog  B) lista arquivos do sistema de arquivos
- C) lista as tabelas do schema  D) executa SQL

**13.** Uma view que oculta colunas com base no usuário é melhor implementada com:
- A) tabela externa  B) dynamic view  C) CTE  D) temp view

**14.** Qual comando importa dados do arquivo para uma tabela mantendo ACID?
- A) `LOAD DATA`  B) `COPY INTO`  C) `INSERT FROM FILE`  D) `READ`

**15.** `ROW_NUMBER() OVER (PARTITION BY p ORDER BY v DESC)` — o que faz?
- A) numera linhas por partição sem empates  B) agrega v por p
- C) remove duplicatas  D) ordena a tabela inteira

**16.** Qual camada da Medallion é append-only e preserva o dado cru?
- A) Bronze  B) Prata  C) Ouro  D) Todas

**17.** Em qual compute as **queries SQL/dashboards** rodam?
- A) SQL Warehouse  B) job clusters  C) notebook serverless  D) MLflow

**18.** O que `QUALIFY` faz?
- A) filtra antes do GROUP BY  B) filtra o resultado de uma window function
- C) valida constraints  D) otimiza o plano

**19.** Qual é a nomenclatura oficial de 3 níveis do UC?
- A) metastore.database.table  B) catalog.schema.table
- C) schema.table.column  D) workspace.catalog.table

**20.** Para publicar BI sobre o Ouro, o melhor compute é:
- A) SQL Warehouse  B) notebook com display()  C) MLflow  D) DABs
"""),
        teoria(
            "Gabarito comentado",
            "**1-B** · **2-B** (ACID: transação falha inteira) · **3-C** · **4-B** · "
            "**5-C** (validade = domínio) · **6-B** · **7-B** · **8-B** · **9-B** (managed = "
            "storage gerenciado pelo UC) · **10-B** (Parquet não tem ACID; Delta sim) · "
            "**11-A** · **12-B** · **13-B** (dynamic view mascara por usuário) · "
            "**14-B** (`COPY INTO` mantém ACID e é idempotente) · **15-A** · "
            "**16-A** (Bronze é append-only; Prata/Ouro são transformados) · **17-A** · "
            "**18-B** · **19-B** · **20-A**.\n\n"
            "**Autoavaliação**: ≥ 14 acertos (70%) = pronto para seguir. < 14 = revise os "
            "notebooks das Semanas 1–2 antes da Semana 3.",
        ),
        dica_prova("O erro #1 em provas Databricks: esquecer que managed tables são apagadas no "
                   "DROP (storage gerenciado pelo UC), enquanto external tables preservam os "
                   "arquivos. Revise isso antes de agendar."),
        exercicios([
            "Refaça o simulado cronometrado (45 min) e registre sua nota.",
            "Liste os 3 tópicos em que você errou e associe ao notebook correspondente.",
        ]),
        gabarito([
            ("Nota",
             "≥ 14/20 (70%) para avançar. Anote a nota e os tópicos errados para revisar na "
             "Semana 9 antes do simulado completo."),
            ("Revisão",
             "Ex.: errou dynamic views → revise notebook do Dia 2 (UC/Volumes) e o da Semana 7. "
             "Revisar o erro agora é o que evita lacuna no futuro."),
        ]),
        footer([
            "Rodei todos os 6 notebooks da Semana 2.",
            "Domino CTE, window functions, PIVOT e QUALIFY.",
            "Classifico problemas nas 6 dimensões de qualidade.",
            "Tenho repo Git com meu primeiro commit e branch.",
            "Fiz o simulado parcial e revisei os erros.",
        ]),
    ],
))
