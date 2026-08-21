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

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana2_dia4_modelagem_dimensional_star_schema",
    [
        header(
            "2", "4", "Modelagem dimensional e Star Schema",
            "Entender fato vs dimensão, o padrão Star Schema, os tipos de SCD (Slowly Changing "
            "Dimensions) e as convenções de nomenclatura do projeto.",
            "DEA (modelagem), DEP (SCD)", "Modelo conceitual do projeto documentado",
            "✅ Free Edition",
        ),
        teoria(
            "Por que modelar?",
            "Dados não modelados = consultas lentas e números divergentes. O padrão da indústria "
            "para análise é a **modelagem dimensional** (Kimball): separar o que é **fato** "
            "(medidas, eventos que acontecem — vendas) do que é **dimensão** (entidades de "
            "contexto — cliente, produto, tempo, loja).",
        ),
        teoria(
            "Fato vs Dimensão",
            "**Tabela fato**: registra eventos/medidas. Alta cardinalidade (muitas linhas), "
            "colunas numéricas aditivas, chaves estrangeiras para dimensões.\n"
            "**Tabela dimensão**: contexto descritivo. Poucas linhas, colunas textuais, "
            "chave primária (surrogate key).\n\n"
            "**Star Schema**: 1 fato no centro + dimensões ao redor (forma de estrela). "
            "É o padrão de consumo para BI e para a camada **Ouro** da Medallion.\n\n"
            "```\n         dim_cliente\n             │\ndim_tempo ──fato_vendas── dim_produto\n             │\n         dim_loja\n```",
        ),
        teoria(
            "SCD — Slowly Changing Dimensions",
            "Dimensões mudam lentamente (cliente muda de cidade). Como registrar a história?\n\n"
            "- **SCD1**: sobrescreve o valor antigo (perde histórico). Simples; usado quando o "
            "histórico não importa.\n"
            "- **SCD2**: mantém histórico com versões (linhas com `valid_from`, `valid_to`, "
            "`is_current`). Complexo; usado em auditoria e análise histórica.\n"
            "- **SCD3**: guarda só o valor anterior em coluna separada (`cidade_atual`, "
            "`cidade_anterior`). Raramente usado.\n\n"
            "> 🎯 **Dica de prova**: a DEA/DEP cobra **quando usar SCD1 vs SCD2**: "
            "correção de dados = SCD1; histórico obrigatório = SCD2; quantidade de versões "
            "pequena e fixa = SCD3. Na Semana 8 implementamos SCD2 real com `APPLY CHANGES INTO`.",
        ),
        pratica("Desenhando o modelo do projeto",
            "Vamos definir o modelo conceitual do nosso varejo (vamos materializar na Semana 4)."),
        code('# Modelo conceitual documentado em células markdown (abaixo) e validado aqui\n'
             'modelo = """\n'
             'FATO:  fato_vendas (data, dim_cliente, dim_produto, dim_loja, qtd, valor)\n'
             'DIMS:  dim_cliente, dim_produto, dim_tempo, dim_loja\n'
             'SCD:   dim_cliente -> SCD2 (cidade muda; precisamos histórico)\n'
             '       dim_produto -> SCD1 (correção de descrição)\n'
             '"""\n'
             'print(modelo)'),
        teoria(
            "Convenções de nomenclatura do projeto",
            "Adotamos as convenções padrão do mercado (usadas no Databricks e em entrevistas):\n"
            "- Tabelas de camada: `workspace.bronze.*`, `workspace.prata.*`, `workspace.ouro.*`\n"
            "- Dimensões: `dim_*` · Fatos: `fato_*` · Agregados de negócio: `nome_do_kpi`\n"
            "- Views: sufixo `_vw` · Tabelas com `_ingested_at` no Bronze\n"
            "- Chaves: `sk_*` (surrogate key) nas dimensões, `*_id` nas chaves naturais",
        ),
        dica_prova("A DEA cobra identificar qual tabela é fato vs dimensão e qual esquema é "
                   "Star vs Snowflake (normalizado). Star = denormalizado, mais rápido para BI."),
        exercicios([
            "Classifique: `dim_cliente`, `fato_vendas`, `dim_produto`, `dim_tempo` — qual é fato?",
            "Por que o Ouro costuma ser denormalizado (star schema) em vez de normalizado?",
            "Se o endereço de um cliente muda e você precisa do histórico de endereços, qual SCD usar?",
            "Desenhe o star schema do projeto com pelo menos 3 dimensões.",
        ]),
        gabarito([
            ("Fato",
             "`fato_vendas` — registra o evento (venda) com medidas numéricas; as demais são "
             "dimensões de contexto."),
            ("Denormalizado",
             "BI consulta por agregação — joins com dimensões pequenas e diretas são mais rápidos "
             "e simples para o usuário final. Snowflake (normalizado) economiza espaço, mas "
             "complexifica a consulta."),
            ("SCD2",
             "SCD2 preserva o histórico completo de versões do endereço — necessário para "
             "auditoria e análise temporal."),
            ("Star schema",
             "Desenhe `fato_vendas` no centro, ligado a `dim_cliente`, `dim_produto`, `dim_tempo`, "
             "`dim_loja`. Cada dim com chave surrogate (sk_) ligada ao fato."),
        ]),
        footer(),
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
