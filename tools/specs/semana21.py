"""Semana 21 — Bônus: Motor de Validações + CSV + Formulário (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana21_dia1_motor_validacoes_4_camadas",
    [
        header(
            "21", "1", "Motor de validações em 4 camadas",
            "Construir o motor que valida os dados em 4 camadas: estrutura → tipo/"
            "formato → consistência SQL → regra de negócio Python.",
            "Portfólio empresarial", "Motor de validação rodando",
            "✅ Free Edition",
        ),
        teoria(
            "As 4 camadas do motor",
            "| Camada | Valida | Exemplo |\n|---|---|---|\n"
            "| **1. Estrutura** | colunas/linhas existem | coluna obrigatória presente |\n"
            "| **2. Tipo/formato** | valores convertem | data válida, número |\n"
            "| **3. Consistência SQL** | coerência com o Lakehouse | produto existe, mês válido |\n"
            "| **4. Regra de negócio** | regras Python do YAML | meta ≥ 0, desconto ≤ 100 |",
        ),
        pratica("Motor — camadas 1 e 2",
            "Estrutura e tipo/formato."),
        code('# Camada 1: estrutura\n'
             'def valida_estrutura(dados, yaml_def):\n'
             '    erros = []\n'
             '    campos = {c["nome"]: c for c in yaml_def["campos"]}\n'
             '    for campo, cfg in campos.items():\n'
             '        if cfg.get("obrigatorio") and campo not in dados.columns:\n'
             '            erros.append(f"Coluna obrigatória ausente: {campo}")\n'
             '    return erros\n'
             'print("Camada 1 pronta.")'),
        code('# Camada 2: tipo/formato\n'
             'from datetime import datetime\n'
             'def valida_tipo(valor, cfg):\n'
             '    tipo = cfg["tipo"]\n'
             '    if tipo == "numero":\n'
             '        try:\n'
             '            v = float(valor)\n'
             '            if "min" in cfg and v < cfg["min"]:\n'
             '                return f"menor que min {cfg[\'min\']}"\n'
             '            if "max" in cfg and v > cfg["max"]:\n'
             '                return f"maior que max {cfg[\'max\']}"\n'
             '        except ValueError:\n'
             '            return "não é número"\n'
             '    if tipo == "data":\n'
             '        try:\n'
             '            datetime.strptime(str(valor), "%Y-%m-%d")\n'
             '        except ValueError:\n'
             '            return "data inválida (YYYY-MM-DD)"\n'
             '    if tipo == "mes":\n'
             '        if str(valor) not in [f"{m:02d}" for m in range(1, 13)]:\n'
             '            return "mês inválido (01-12)"\n'
             '    return None\n'
             'print("Camada 2 pronta.")'),
        pratica("Motor — camadas 3 e 4",
            "Consistência com o Lakehouse e regras de negócio."),
        code('# Camada 3: consistência SQL (produto existe?)\n'
             'def valida_consistencia(produto):\n'
             '    if produto is None: return None\n'
             '    r = spark.sql(f"SELECT 1 FROM workspace.prata.dim_produto WHERE StockCode = \'{produto}\'").count()\n'
             '    return None if r > 0 else f"produto {produto} não existe"\n'
             'print("Camada 3 pronta (produto existe no catálogo).")'),
        code('# Camada 4: regras Python do YAML\n'
             'def valida_regra_negocio(row, yaml_def):\n'
             '    erros = []\n'
             '    for campo, cfg in yaml_def["campos"].items():\n'
             '        if cfg.get("obrigatorio") and (row.get(campo) in (None, "")):\n'
             '            erros.append(f"{campo} obrigatório")\n'
             '    return erros\n'
             'print("Camada 4 pronta (estenda com regras custom do YAML).")'),
        dica_prova("Portfólio: explicar o motor em 4 camadas (estrutura → tipo → "
                   "consistência → negócio) mostra design sólido — o entrevistador "
                   "adora essa separação."),
        exercicios([
            "Adicione uma regra custom no YAML (ex.: desconto só para produto ativo).",
            "Por que separar consistência SQL de regra Python?",
            "Onde cada camada roda (Spark/engine)?",
        ]),
        gabarito([
            ("Regra custom",
             'Adicione `regra: "produto_ativo"` no campo e trate na camada 4.'),
            ("Separar",
             "Consistência (SQL) é genérica e reutilizável; regra de negócio é específica "
             "do fluxo — separar facilita manutenção."),
            ("Onde roda",
             "1–2: pandas/engine; 3: Spark SQL (Lakehouse); 4: Python."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana21_dia2_upload_csv_relatorio_erros",
    [
        header(
            "21", "2", "Upload de CSV com relatório de erros",
            "Permitir o upload de CSV, rodar o motor de validação por linha e exibir um "
            "relatório claro de erros (quem errou, onde, por quê).",
            "Portfólio empresarial", "Upload + relatório de erros",
            "✅ Free Edition (app Streamlit)",
        ),
        teoria(
            "O fluxo de upload",
            "1. Usuário envia CSV\n"
            "2. Parse e leitura (pandas)\n"
            "3. Motor valida linha a linha (4 camadas)\n"
            "4. Relatório: linhas OK/erro com mensagem clara\n"
            "5. Salvar submissão + itens + validações\n"
            "6. (Se tudo OK → fluxo de aprovação, Semana 23)",
        ),
        pratica("Upload + validação",
            "Leia o CSV e valide por linha."),
        code('# Upload e validação (pandas)\n'
             'import pandas as pd\n'
             'from io import StringIO\n'
             'def processar_csv(conteudo, yaml_def):\n'
             '    df = pd.read_csv(StringIO(conteudo))\n'
             '    erros = valida_estrutura(df, yaml_def)\n'
             '    if erros:\n'
             '        return None, erros\n'
             '    relatorio = []\n'
             '    for i, row in df.iterrows():\n'
             '        linha_erros = []\n'
             '        for campo, cfg in {c["nome"]: c for c in yaml_def["campos"]}.items():\n'
             '            if campo in df.columns:\n'
             '                e = valida_tipo(row.get(campo), cfg)\n'
             '                if e:\n'
             '                    linha_erros.append(f"{campo}: {e}")\n'
             '        if linha_erros:\n'
             '            relatorio.append({"linha": i+2, "erros": linha_erros})  # +2 (header)\n'
             '    return df, relatorio\n'
             'print("processar_csv pronto (retorna df + relatório).")'),
        code('# Exemplo de relatório\n'
             'relatorio_exemplo = [\n'
             '    {"linha": 3, "erros": ["meta: não é número"]},\n'
             '    {"linha": 5, "erros": ["mes: mês inválido (01-12)", "vendedor obrigatório"]},\n'
             ']\n'
             'for r in relatorio_exemplo:\n'
             '    print(f"Linha {r[\'linha\']}: " + "; ".join(r["erros"]))'),
        pratica("Salvando a submissão",
            "Persista submissão + itens + validações."),
        code('# Salvar submissão\n'
             'import uuid\n'
             'def salvar_submissao(fluxo_id, df, relatorio, origem="csv"):\n'
             '    sid = str(uuid.uuid4())\n'
             '    spark.createDataFrame([(sid, fluxo_id, origem, "pendente", "now", "ana")],\n'
             '        ["submissao_id", "fluxo_id", "origem", "status", "criado_em", "criado_por"])\\\n'
             '        .withColumn("criado_em", current_timestamp())\\\n'
             '        .write.mode("append").saveAsTable("workspace.app.submissoes")\n'
             '    print(f"Submissão {sid} salva com {len(relatorio)} linhas com erro.")\n'
             'salvar_submissao("metas", None, relatorio_exemplo)'),
        dica_prova("UX de validação: relatório por LINHA com mensagem clara (não "
                   "'erro genérico') — é o que faz o app ser adotado pelo negócio."),
        exercicios([
            "Teste o upload com um CSV de 10 linhas (2 com erro).",
            "Mostre no app: contagem OK/erro + tabela dos erros.",
            "O que fazer com linhas OK quando há erros? (decisão de produto)",
        ]),
        gabarito([
            ("Teste",
             "Relatório deve apontar exatamente as linhas/campos."),
            ("App",
             "st.file_uploader + st.dataframe do relatório + métricas OK/erro."),
            ("Decisão",
             "Política: ou bloquear tudo, ou processar só as OK (configurável por fluxo "
             "no YAML)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana21_dia3_formulario_dinamico_yaml",
    [
        header(
            "21", "3", "Formulário dinâmico gerado do YAML",
            "Gerar o formulário de entrada AUTOMATICAMENTE a partir do YAML do fluxo — "
            "com combos carregados do Lakehouse.",
            "Portfólio empresarial", "Formulário dinâmico funcionando",
            "✅ Free Edition (app Streamlit)",
        ),
        teoria(
            "Formulário dirigido por configuração",
            "O YAML define os campos → o app **gera o formulário** (text, number, date, "
            "select). Novo fluxo = novo formulário **sem código** — a mágica da "
            "parametrização por YAML.",
        ),
        pratica("Gerador de formulário",
            "Renderize os campos do YAML como widgets Streamlit."),
        code('# Gerador de formulário a partir do YAML\n'
             'import streamlit as st\n'
             'def renderizar_formulario(yaml_def):\n'
             '    valores = {}\n'
             '    for campo in yaml_def["campos"]:\n'
             '        nome, tipo = campo["nome"], campo["tipo"]\n'
             '        rotulo = nome + (" *" if campo.get("obrigatorio") else "")\n'
             '        if tipo == "numero":\n'
             '            valores[nome] = st.number_input(rotulo, min_value=float(campo.get("min", 0)),\n'
             '                                             max_value=float(campo.get("max", 1e9)))\n'
             '        elif tipo == "data":\n'
             '            valores[nome] = str(st.date_input(rotulo))\n'
             '        elif tipo == "mes":\n'
             '            valores[nome] = st.selectbox(rotulo, [f"{m:02d}" for m in range(1, 13)])\n'
             '        else:\n'
             '            valores[nome] = st.text_input(rotulo)\n'
             '    return valores\n'
             'print("Formulário gerado do YAML (text/number/date/select).")'),
        code('# Combo carregado do Lakehouse (ex.: lista de produtos)\n'
             'def combo_produtos():\n'
             '    return [r[0] for r in spark.sql("SELECT StockCode FROM workspace.prata.dim_produto LIMIT 20").collect()]\n'
             'print("produtos:", combo_produtos())\n'
             'print("No formulário: st.selectbox(rotulo, combo_produtos())")'),
        pratica("Submissão pelo formulário",
            "O formulário gera uma submissão igual à do CSV — mesma validação."),
        code('# Submeter formulário\n'
             'def submeter_formulario(fluxo_id, valores):\n'
             '    df = pd.DataFrame([valores])\n'
             '    # mesma validação do CSV (4 camadas)\n'
             '    return processar_csv(df.to_csv(index=False), yaml_def)\n'
             'print("Formulário e CSV usam o MESMO motor — consistência total.")'),
        dica_prova("Portfólio: 'novo fluxo sem código' é o pitch do app — o YAML vira "
                   "formulário, validação e relatório automaticamente."),
        exercicios([
            "Adicione o campo 'select com opções' ao YAML (enum).",
            "Por que formulário e CSV usam o mesmo motor?",
            "Renderize o formulário do fluxo descontos.",
        ]),
        gabarito([
            ("Enum",
             "Adicione `opcoes: [a, b, c]` no YAML; o gerador usa st.selectbox com elas."),
            ("Mesmo motor",
             "Uma única lógica de validação — sem divergência entre canais."),
            ("Descontos",
             "produto (select do Lakehouse), percentual (number 0–100), validade (date)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana21_dia4_motor_camada3_consistencia_sql",
    [
        header(
            "21", "4", "Consistência SQL: validando contra o Lakehouse",
            "Aprofundar a camada 3: validações que consultam o Lakehouse (produto existe, "
            "preço dentro da faixa histórica, cliente duplicado).",
            "Portfólio empresarial", "Validações SQL no motor",
            "✅ Free Edition",
        ),
        teoria(
            "Validações com contexto do Lakehouse",
            "A camada 3 usa o próprio Lakehouse como fonte da verdade:\n"
            "- produto existe? (dim_produto)\n"
            "- cliente já cadastrado? (duplicidade)\n"
            "- preço dentro da faixa histórica? (ouro)\n\n"
            "É o que torna a validação 'inteligente' — não só sintática, mas semântica.",
        ),
        pratica("Validações SQL",
            "Implemente as regras de consistência."),
        code('# Produto existe?\n'
             'def produto_existe(codigo):\n'
             '    n = spark.sql(f"SELECT COUNT(*) FROM workspace.prata.dim_produto WHERE StockCode = \'{codigo}\'").collect()[0][0]\n'
             '    return n > 0\n'
             'print("85123A existe:", produto_existe("85123A"))\n'
             'print("ZZZZZ existe:", produto_existe("ZZZZZ"))'),
        code('# Cliente duplicado?\n'
             'def cliente_duplicado(email):\n'
             '    n = spark.sql(f"SELECT COUNT(*) FROM workspace.bronze.clientes_bronze WHERE lower(Email) = lower(\'{email}\')").count()\n'
             '    return n > 0\n'
             'print("Cliente duplicado? (use um email do seu dataset)")'),
        code('# Preço dentro da faixa histórica (Ouro)\n'
             'def preco_fora_faixa(codigo, preco):\n'
             '    faixa = spark.sql(f"""\n'
             '        SELECT MIN(UnitPrice) AS mn, MAX(UnitPrice) AS mx\n'
             '        FROM workspace.bronze.vendas_bronze WHERE StockCode = \'{codigo}\'\n'
             '    """).collect()[0]\n'
             '    if faixa.mn is None: return False\n'
             '    return not (faixa.mn * 0.5 <= preco <= faixa.mx * 2.0)\n'
             'print("preco_fora_faixa implementado (50%–200% do histórico).")'),
        pratica("Integrando ao motor",
            "A camada 3 roda em lote (join com as dimensões) para eficiência."),
        code('# Lote eficiente: join em vez de N queries\n'
             'print("""\n'
             'Em vez de validar linha a linha (N queries), faça:\n'
             'df_submissao.join(dim_produto, on="produto", how="left_anti")\n'
             '  -> linhas cujo produto NÃO existe (validação em 1 scan)\n'
             '""")\n'
             'print("Consistência SQL em lote: rápido e escalável.")'),
        dica_prova("Portfólio: validação com o Lakehouse (anti-join, faixas históricas) "
                   "é o diferencial — mostra que o app não valida 'no vácuo'."),
        exercicios([
            "Valide duplicidade de produto no fluxo preços (anti-join).",
            "Por que validar em lote (join) e não linha a linha?",
            "Adicione uma regra de faixa ao YAML (min/max dinâmicos do histórico).",
        ]),
        gabarito([
            ("Anti-join",
             "`df.join(dim_produto, 'produto', 'left_anti')` → linhas com produto "
             "inexistente."),
            ("Lote",
             "N queries = N scans; join = 1 scan — ordem de grandeza mais rápido."),
            ("Faixa dinâmica",
             "Adicione `regra: faixa_historica` no YAML; a camada 3 resolve com o Ouro."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana21_dia5_regras_negocio_python",
    [
        header(
            "21", "5", "Regras de negócio Python no YAML",
            "Permitir regras de negócio customizadas por fluxo, definidas no YAML e "
            "executadas pela camada 4 do motor.",
            "Portfólio empresarial", "Regras custom rodando",
            "✅ Free Edition",
        ),
        teoria(
            "Regras declaradas no YAML",
            "O YAML declara regras de negócio que o motor executa:\n\n"
            "```yaml\nregras:\n"
            "  - campo: percentual\n"
            "    op: lte\n"
            "    valor: 100\n"
            "  - campo: meta\n"
            "    op: gte\n"
            "    valor: 0\n"
            "```\n\n"
            "Assim, o negócio muda regras **sem deploy de código**.",
        ),
        pratica("Motor de regras",
            "Implemente um mini-avaliador de regras."),
        code('# Avaliador de regras do YAML\n'
             'def aplicar_regras(row, regras):\n'
             '    erros = []\n'
             '    ops = {"eq": lambda a, b: a == b, "neq": lambda a, b: a != b,\n'
             '           "gt": lambda a, b: a > b, "gte": lambda a, b: a >= b,\n'
             '           "lt": lambda a, b: a < b, "lte": lambda a, b: a <= b}\n'
             '    for regra in regras:\n'
             '        campo = regra["campo"]\n'
             '        valor = row.get(campo)\n'
             '        try:\n'
             '            ok = ops[regra["op"]](float(valor), float(regra["valor"]))\n'
             '            if not ok:\n'
             '                erros.append(f"{campo} falhou {regra[\'op\']} {regra[\'valor\']}")\n'
             '        except (TypeError, ValueError):\n'
             '            erros.append(f"{campo} incomparável")\n'
             '    return erros\n'
             'print("Avaliador de regras pronto.")'),
        code('# Regras do fluxo descontos (do YAML)\n'
             'regras_descontos = [\n'
             '    {"campo": "percentual", "op": "lte", "valor": 100},\n'
             '    {"campo": "percentual", "op": "gte", "valor": 0},\n'
             ']\n'
             'print("regras:", aplicar_regras({"percentual": 150}, regras_descontos))\n'
             'print("regras:", aplicar_regras({"percentual": 15}, regras_descontos))'),
        pratica("Expressões livres",
            "Suporte a expressões simples (eval seguro em sandbox)."),
        code('# Expressão (sandbox: sem builtins perigosos)\n'
             'import ast\n'
             'def avaliar_expr(expr, row):\n'
             '    arvore = ast.parse(expr, mode="eval")\n'
             '    nomes = {n.id: row.get(n.id) for n in ast.walk(arvore) if isinstance(n, ast.Name)}\n'
             '    return eval(compile(arvore, "<expr>", "eval"), {"__builtins__": {}}, nomes)\n'
             'print(avaliar_expr("percentual <= 100 and percentual >= 0", {"percentual": 15}))\n'
             'print("Expressões avaliadas sem builtins (sandbox).")'),
        dica_prova("Portfólio: regras declarativas no YAML (op/valor) + expressões "
                   "sandbox = negócio configura sem código. Pergunta: 'como o negócio "
                   "muda regras sem deploy?' → YAML + motor."),
        exercicios([
            "Adicione regra de data futura (validade > hoje).",
            "Por que o eval é sandboxed?",
            "Documente as regras dos 4 fluxos.",
        ]),
        gabarito([
            ("Data futura",
             "Regra especial `data_futura: true` no campo — tratada na camada 4."),
            ("Sandbox",
             "Eval com `__builtins__={}` evita execução de código arbitrário (segurança)."),
            ("Documentar",
             "Tabela fluxo × regras no README do app."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana21_dia6_entregavel_motor_csv_formulario",
    [
        header(
            "21", "6", "Entregável: motor completo + CSV + formulário",
            "Integrar o motor de 4 camadas, o upload de CSV e o formulário dinâmico no "
            "app — o entregável da Semana 21.",
            "Portfólio empresarial", "Motor + CSV + formulário integrados",
            "✅ Free Edition (app Streamlit)",
        ),
        teoria(
            "O que a Semana 21 entregou",
            "- Motor em 4 camadas (estrutura → tipo → consistência SQL → regra Python)\n"
            "- Upload de CSV com relatório de erros por linha\n"
            "- Formulário dinâmico gerado do YAML (combos do Lakehouse)\n"
            "- Regras de negócio declarativas no YAML",
        ),
        pratica("App integrado",
            "Monte o app com as duas entradas (CSV e formulário) e o relatório."),
        code('# app_submissao.py (Streamlit)\n'
             'import streamlit as st\n'
             'st.title("📥 DataFlow — Submissão")\n'
             'fluxo = st.selectbox("Fluxo", ["metas", "descontos", "precos", "clientes"])\n'
             'modo = st.radio("Entrada", ["CSV", "Formulário"])\n'
             '\n'
             'if modo == "CSV":\n'
             '    arquivo = st.file_uploader("Envie o CSV", type=["csv"])\n'
             '    if arquivo:\n'
             '        conteudo = arquivo.read().decode("utf-8")\n'
             '        df, relatorio = processar_csv(conteudo, yaml_defs[fluxo])\n'
             '        st.metric("Linhas com erro", len(relatorio))\n'
             '        st.dataframe(pd.DataFrame(relatorio))\n'
             'else:\n'
             '    valores = renderizar_formulario(yaml_defs[fluxo])\n'
             '    if st.button("Submeter"):\n'
             '        df, relatorio = submeter_formulario(fluxo, valores)\n'
             '        st.success("Submetido! Aguardando aprovação.")\n'
             'print("App de submissão integrado (CSV + formulário + relatório).")'),
        pratica("Validação final",
            "1. Submeta via CSV com erros → relatório correto.\n"
            "2. Submeta via formulário → mesmo motor.\n"
            "3. Confira as tabelas submissoes/validacoes.\n"
            "4. Publique."),
        code('# Conferir as tabelas\n'
             'display(spark.sql("SELECT * FROM workspace.app.submissoes ORDER BY criado_em DESC LIMIT 5"))\n'
             'display(spark.sql("SELECT * FROM workspace.app.validacoes LIMIT 10"))'),
        dica_prova("O motor de validação com relatório por linha + formulário dinâmico "
                   "é um case forte de entrevista: mostre o app rodando (30s de demo)."),
        exercicios([
            "Teste os 4 fluxos (CSV e formulário).",
            "Escreva o README do motor (4 camadas + regras).",
        ]),
        gabarito([
            ("Teste",
             "Cada fluxo deve validar conforme suas regras — e o relatório apontar "
             "exatamente os erros."),
            ("README",
             "Diagrama do motor + exemplos de regras YAML + prints do relatório."),
        ]),
        footer([
            "Motor de 4 camadas completo.",
            "Upload CSV com relatório de erros.",
            "Formulário dinâmico (combos do Lakehouse).",
            "Regras de negócio via YAML.",
        ]),
    ],
))
