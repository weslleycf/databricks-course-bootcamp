"""Semana 20 — Bônus: App Admin com YAML (Fundações + Editor) (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana20_dia1_arquitetura_app_yaml_6_tabelas",
    [
        header(
            "20", "1", "App DataFlow Admin: arquitetura e modelo de 6 tabelas",
            "Desenhar o app empresarial de parametrização por YAML e criar o modelo de "
            "dados (6 tabelas Lakebase).",
            "Portfólio empresarial", "Arquitetura + 6 tabelas criadas",
            "✅ Free Edition (1 projeto Lakebase)",
        ),
        teoria(
            "O app DataFlow Admin",
            "O **DataFlow Admin** permite que usuários de negócio enviem dados (CSV ou "
            "formulário) com **validações 100% configuráveis via YAML por fluxo**, e uma "
            "seção admin para gerenciar os fluxos.\n\n"
            "Arquitetura:\n"
            "```\nAdmin (editor YAML) → Fluxos (YAML) → Motor de validação\n   → aprovação → Bronze → DLT → Prata/Ouro\n```",
        ),
        teoria(
            "O modelo de 6 tabelas (Lakebase)",
            "| Tabela | Papel |\n|---|---|\n"
            "| `fluxos` | definição dos fluxos (nome, campos, YAML) |\n"
            "| `campos` | campos de cada fluxo (nome, tipo, regras) |\n"
            "| `submissoes` | envios de dados (CSV/formulário) |\n"
            "| `itens_submissao` | linhas de cada submissão |\n"
            "| `validacoes` | resultados de validação por item |\n"
            "| `aprovacoes` | workflow de aprovação |",
        ),
        pratica("Criando as tabelas",
            "Crie as 6 tabelas no Lakebase (ou Delta, na Free)."),
        sql('CREATE SCHEMA IF NOT EXISTS workspace.app;\n'
            'CREATE TABLE IF NOT EXISTS workspace.app.fluxos (\n'
            '  fluxo_id STRING, nome STRING, yaml_def STRING, ativo BOOLEAN, criado_em TIMESTAMP\n'
            ') USING DELTA;\n'
            'CREATE TABLE IF NOT EXISTS workspace.app.campos (\n'
            '  fluxo_id STRING, campo STRING, tipo STRING, obrigatorio BOOLEAN\n'
            ') USING DELTA;\n'
            'CREATE TABLE IF NOT EXISTS workspace.app.submissoes (\n'
            '  submissao_id STRING, fluxo_id STRING, origem STRING,\n'
            '  status STRING, criado_em TIMESTAMP, criado_por STRING\n'
            ') USING DELTA;\n'
            'CREATE TABLE IF NOT EXISTS workspace.app.itens_submissao (\n'
            '  submissao_id STRING, linha INT, dados STRING\n'
            ') USING DELTA;\n'
            'CREATE TABLE IF NOT EXISTS workspace.app.validacoes (\n'
            '  submissao_id STRING, linha INT, campo STRING, regra STRING, ok BOOLEAN, msg STRING\n'
            ') USING DELTA;\n'
            'CREATE TABLE IF NOT EXISTS workspace.app.aprovacoes (\n'
            '  submissao_id STRING, aprovado_por STRING, aprovado_em TIMESTAMP, status STRING\n'
            ') USING DELTA;\n'
            'SHOW TABLES IN workspace.app;'),
        pratica("Documentando",
            "Registre no README do app: caso de uso, fluxo e as 6 tabelas."),
        dica_prova("Portfólio: um app com modelo transacional (Lakebase) + motor de "
                   "validação + aprovação é exatamente o que empresas pedem — o "
                   "'último 1%' que diferencia."),
        exercicios([
            "Explique o papel de cada uma das 6 tabelas.",
            "Por que separar submissoes de itens_submissao?",
            "Onde o YAML entra nesse modelo?",
        ]),
        gabarito([
            ("6 tabelas",
             "fluxos/campos = definição; submissoes/itens = dados; validacoes = "
             "resultados; aprovacoes = workflow."),
            ("Separar",
             "1 submissão tem N linhas — normalizar permite validar e aprovar por linha."),
            ("YAML",
             "O YAML define os campos/regras do fluxo; o motor lê o YAML e valida os "
             "itens."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana20_dia2_json_schema_validador_yaml",
    [
        header(
            "20", "2", "JSON Schema: validando o YAML dos fluxos",
            "Definir o esquema do YAML de fluxo e validar com JSON Schema — o YAML "
            "inválido não entra.",
            "Portfólio empresarial", "Validador de YAML funcionando",
            "✅ Free Edition",
        ),
        teoria(
            "YAML de fluxo + JSON Schema",
            "Cada fluxo é definido por um YAML:\n\n"
            "```yaml\nfluxo: metas\nnome: Metas de Vendas\ncampos:\n  - nome: vendedor\n    tipo: string\n    obrigatorio: true\n  - nome: meta\n    tipo: numero\n    min: 0\n  - nome: mes\n    tipo: mes\n```\n\n"
            "O **JSON Schema** valida a ESTRUTURA do YAML (campos obrigatórios, tipos "
            "permitidos) antes de processar — evita config quebrada.",
        ),
        pratica("JSON Schema do YAML",
            "Defina o schema que todo YAML de fluxo deve respeitar."),
        code('# JSON Schema do YAML de fluxo\n'
             'json_schema = {\n'
             '  "type": "object",\n'
             '  "required": ["fluxo", "nome", "campos"],\n'
             '  "properties": {\n'
             '    "fluxo": {"type": "string"},\n'
             '    "nome": {"type": "string"},\n'
             '    "campos": {\n'
             '      "type": "array",\n'
             '      "items": {\n'
             '        "type": "object",\n'
             '        "required": ["nome", "tipo"],\n'
             '        "properties": {\n'
             '          "nome": {"type": "string"},\n'
             '          "tipo": {"enum": ["string", "numero", "data", "mes", "bool"]},\n'
             '          "obrigatorio": {"type": "boolean"},\n'
             '          "min": {"type": "number"},\n'
             '          "max": {"type": "number"}\n'
             '        }\n'
             '      }\n'
             '    }\n'
             '  }\n'
             '}\n'
             'print(json.dumps(json_schema, indent=2))'),
        code('# Validar o YAML contra o schema (jsonschema)\n'
             'import yaml, json\n'
             'from jsonschema import validate, ValidationError\n'
             'yaml_fluxo = """\n'
             'fluxo: metas\n'
             'nome: Metas de Vendas\n'
             'campos:\n'
             '  - nome: vendedor\n'
             '    tipo: string\n'
             '    obrigatorio: true\n'
             '"""\n'
             'dados = yaml.safe_load(yaml_fluxo)\n'
             'try:\n'
             '    validate(instance=dados, schema=json_schema)\n'
             '    print("YAML válido!")\n'
             'except ValidationError as e:\n'
             '    print("YAML inválido:", e.message)'),
        pratica("Teste com YAML inválido",
            "Um YAML sem o campo obrigatório deve falhar."),
        code('# YAML inválido (sem nome)\n'
             'yaml_ruim = "fluxo: metas\\n"  # falta nome e campos\n'
             'try:\n'
             '    validate(instance=yaml.safe_load(yaml_ruim), schema=json_schema)\n'
             '    print("ERRO: deveria falhar")\n'
             'except ValidationError as e:\n'
             '    print("Corretamente bloqueado:", e.message)'),
        dica_prova("Portfólio: JSON Schema valida a configuração ANTES de processar — "
                   "mesma filosofia de expectations no DLT: falha cedo, falha claro."),
        exercicios([
            "Adicione um campo de enum ao schema (ex.: categoria).",
            "Por que validar o YAML antes de salvar?",
            "Crie o YAML do fluxo 'descontos' e valide.",
        ]),
        gabarito([
            ("Enum",
             'Adicione `"categoria": {"enum": ["venda", "meta", "preco"]}` nas properties.'),
            ("Validar antes",
             "Config inválida quebra o motor e o app — validação na entrada evita isso."),
            ("Descontos",
             "Campos: produto (string), percentual (numero, 0–100), validade (data)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana20_dia3_editor_yaml_admin",
    [
        header(
            "20", "3", "Editor YAML admin com diff e rollback",
            "Construir a seção admin: editor YAML com validação ao vivo, diff de "
            "alterações e rollback de versões.",
            "Portfólio empresarial", "Editor com diff/rollback funcional",
            "✅ Free Edition (app Streamlit)",
        ),
        teoria(
            "A seção admin",
            "O admin gerencia os fluxos: cria/edita YAML, vê o **diff** da alteração e "
            "faz **rollback** para uma versão anterior. Cada salvar vira uma **versão** "
            "do fluxo (versionado em tabela).",
        ),
        pratica("Versionando fluxos",
            "Toda alteração salva uma nova versão."),
        code('# Salvar versão do fluxo\n'
             'from pyspark.sql.functions import current_timestamp\n'
             'spark.sql("CREATE TABLE IF NOT EXISTS workspace.app.fluxo_versoes (\n'
             '  fluxo_id STRING, versao INT, yaml_def STRING, editado_por STRING,\n'
             '  editado_em TIMESTAMP) USING DELTA")\n'
             'def salvar_versao(fluxo_id, yaml_def, usuario):\n'
             '    v = spark.sql(f"SELECT COALESCE(MAX(versao),0)+1 AS v FROM workspace.app.fluxo_versoes WHERE fluxo_id = \'{fluxo_id}\'").collect()[0][0]\n'
             '    spark.createDataFrame([(fluxo_id, v, yaml_def, usuario, "now")],\n'
             '                          ["fluxo_id", "versao", "yaml_def", "editado_por", "editado_em"])\\\n'
             '        .withColumn("editado_em", current_timestamp())\\\n'
             '        .write.mode("append").saveAsTable("workspace.app.fluxo_versoes")\n'
             '    return v\n'
             'print("salvar_versao pronto — cada edição vira versão.")'),
        code('# Diff entre versões (didático)\n'
             'import difflib\n'
             'def diff_yaml(v_antiga, v_nova):\n'
             '    return "\\n".join(difflib.unified_diff(\n'
             '        v_antiga.splitlines(), v_nova.splitlines(), lineterm=""))\n'
             'print(diff_yaml("fluxo: metas\\nnome: Metas", "fluxo: metas\\nnome: Metas 2026"))'),
        pratica("Rollback",
            "Restaurar uma versão anterior = salvar o YAML antigo como nova versão "
            "(nunca apagar o histórico)."),
        code('# Rollback (nova versão com o YAML antigo)\n'
             'def rollback(fluxo_id, versao_alvo, usuario):\n'
             '    yaml_antigo = spark.sql(f"SELECT yaml_def FROM workspace.app.fluxo_versoes WHERE fluxo_id=\'{fluxo_id}\' AND versao={versao_alvo}").collect()[0][0]\n'
             '    salvar_versao(fluxo_id, yaml_antigo, usuario)\n'
             '    print(f"Rollback para v{versao_alvo} feito (nova versão criada).")\n'
             'print("Rollback sem perder histórico — auditoria completa.")'),
        dica_prova("Portfólio: versionar configuração (YAML) com diff/rollback é o "
                   "padrão de produto admin — mesmos princípios de Git aplicados a "
                   "configuração de negócio."),
        exercicios([
            "Adicione a listagem de versões no app admin.",
            "Por que rollback cria versão nova em vez de apagar?",
            "Monte o editor com text_area + botão salvar (Streamlit).",
        ]),
        gabarito([
            ("Listagem",
             "SELECT versao, editado_em, editado_por FROM fluxo_versoes ORDER BY versao DESC."),
            ("Nova versão",
             "Histórico íntegro e auditável — apagar versão destruiria a trilha de "
             "auditoria."),
            ("Editor",
             "st.text_area (YAML) → validar (JSON Schema) → salvar_versao → mostrar diff."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana20_dia4_permissoes_por_fluxo",
    [
        header(
            "20", "4", "Permissões por fluxo e perfis de acesso",
            "Controlar quem vê/edita cada fluxo e aplicar o RBAC do UC ao app.",
            "Portfólio empresarial", "RBAC por fluxo aplicado",
            "✅ Free Edition",
        ),
        teoria(
            "RBAC por fluxo",
            "Nem todo usuário edita todos os fluxos: o admin define **quem pode ver, "
            "editar ou aprovar** cada fluxo — armazenado em tabela de permissões e "
            "reforçado pelas permissões do UC.",
        ),
        pratica("Permissões por fluxo",
            "Crie a tabela de permissões e as funções de checagem."),
        sql('CREATE TABLE IF NOT EXISTS workspace.app.permissoes_fluxo (\n'
            '  fluxo_id STRING, usuario STRING, permissao STRING\n'
            ') USING DELTA;\n'
            'INSERT INTO workspace.app.permissoes_fluxo VALUES\n'
            '  (\'metas\', \'ana\', \'editar\'),\n'
            '  (\'metas\', \'joao\', \'ver\'),\n'
            '  (\'descontos\', \'ana\', \'aprovar\');'),
        code('# Função de autorização (app)\n'
             'def pode(usuario, fluxo_id, acao):\n'
             '    r = spark.sql(f"""\n'
             '      SELECT permissao FROM workspace.app.permissoes_fluxo\n'
             '      WHERE fluxo_id = \'{fluxo_id}\' AND usuario = \'{usuario}\'\n'
             '    """).collect()\n'
             '    hierarquia = {"ver": 1, "editar": 2, "aprovar": 3}\n'
             '    return any(hierarquia.get(p.permissao, 0) >= hierarquia[acao] for p in r)\n'
             'print("ana edita metas:", pode("ana", "metas", "editar"))\n'
             'print("joao edita metas:", pode("joao", "metas", "editar"))\n'
             'print("ana aprova descontos:", pode("ana", "descontos", "aprovar"))'),
        pratica("Integrando ao app",
            "No Streamlit: o usuário logado (current_user) define as opções visíveis."),
        code('# UI com RBAC\n'
             'print("""\n'
             '1. Obtenha o usuário (auth do workspace)\n'
             '2. Liste só os fluxos onde pode(usuario, fluxo, "ver")\n'
             '3. Editor YAML: só com permissão "editar"\n'
             '4. Botão aprovar: só com "aprovar"\n'
             '""")\n'
             'print("RBAC no app + RBAC do UC (dynamic views) = dupla camada.")'),
        dica_prova("Portfólio: RBAC por fluxo (tabela de permissões) + UC (dynamic "
                   "views) — o app respeita as duas camadas. Pergunta: 'como controlar "
                   "acesso por fluxo?' → tabela de permissões + checagem no app."),
        exercicios([
            "Adicione o perfil 'admin' com acesso total.",
            "Por que o UC (dynamic views) também protege os dados?",
            "O que acontece se o usuário não tem permissão?",
        ]),
        gabarito([
            ("Admin",
             "Crie regra: se usuario == admin → todas as ações em todos os fluxos."),
            ("UC protege",
             "Mesmo que o app tenha bug, o UC limita os dados visíveis (defesa em "
             "profundidade)."),
            ("Sem permissão",
             "A UI esconde e a API bloqueia (403) — nunca confiar só na UI."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana20_dia5_4_fluxos_yaml",
    [
        header(
            "20", "5", "Criando os 4 fluxos YAML do projeto",
            "Criar e validar os fluxos de Metas, Descontos, Preços e Clientes — com "
            "campos, regras e permissões.",
            "Portfólio empresarial", "4 fluxos YAML funcionando",
            "✅ Free Edition",
        ),
        teoria(
            "Os 4 fluxos do varejo",
            "| Fluxo | Campos | Regras |\n|---|---|---|\n"
            "| **Metas** | vendedor, meta, mês | meta ≥ 0, mês válido |\n"
            "| **Descontos** | produto, percentual, validade | 0–100%, data futura |\n"
            "| **Preços** | produto, preço_novo, vigência | preço > 0 |\n"
            "| **Clientes** | nome, email, cidade | email válido |",
        ),
        pratica("Criando os fluxos",
            "Salve cada fluxo como YAML versionado."),
        code('# Fluxo: Metas\n'
             'metas_yaml = """\n'
             'fluxo: metas\n'
             'nome: Metas de Vendas\n'
             'campos:\n'
             '  - nome: vendedor\n'
             '    tipo: string\n'
             '    obrigatorio: true\n'
             '  - nome: meta\n'
             '    tipo: numero\n'
             '    min: 0\n'
             '  - nome: mes\n'
             '    tipo: mes\n'
             '"""\n'
             'salvar_versao("metas", metas_yaml, "admin")\n'
             'print("Fluxo metas salvo.")'),
        code('# Fluxo: Descontos\n'
             'descontos_yaml = """\n'
             'fluxo: descontos\n'
             'nome: Descontos Promocionais\n'
             'campos:\n'
             '  - nome: produto\n'
             '    tipo: string\n'
             '    obrigatorio: true\n'
             '  - nome: percentual\n'
             '    tipo: numero\n'
             '    min: 0\n'
             '    max: 100\n'
             '  - nome: validade\n'
             '    tipo: data\n'
             '"""\n'
             'salvar_versao("descontos", descontos_yaml, "admin")\n'
             'print("Fluxo descontos salvo.")'),
        code('# Fluxos: Preços e Clientes\n'
             'precos_yaml = """\n'
             'fluxo: precos\n'
             'nome: Atualização de Preços\n'
             'campos:\n'
             '  - nome: produto\n'
             '    tipo: string\n'
             '    obrigatorio: true\n'
             '  - nome: preco_novo\n'
             '    tipo: numero\n'
             '    min: 0.01\n'
             '"""\n'
             'clientes_yaml = """\n'
             'fluxo: clientes\n'
             'nome: Cadastro de Clientes\n'
             'campos:\n'
             '  - nome: nome\n'
             '    tipo: string\n'
             '    obrigatorio: true\n'
             '  - nome: email\n'
             '    tipo: string\n'
             '  - nome: cidade\n'
             '    tipo: string\n'
             '"""\n'
             'salvar_versao("precos", precos_yaml, "admin")\n'
             'salvar_versao("clientes", clientes_yaml, "admin")\n'
             'print("4 fluxos salvos e versionados.")'),
        pratica("Validando todos",
            "Rode o JSON Schema em cada fluxo salvo."),
        code('# Validar os 4 fluxos\n'
             'for fid in ["metas", "descontos", "precos", "clientes"]:\n'
             '    y = spark.sql(f"SELECT yaml_def FROM workspace.app.fluxo_versoes WHERE fluxo_id=\'{fid}\' ORDER BY versao DESC LIMIT 1").collect()[0][0]\n'
             '    try:\n'
             '        validate(instance=yaml.safe_load(y), schema=json_schema)\n'
             '        print(f"{fid}: válido")\n'
             '    except Exception as e:\n'
             '        print(f"{fid}: INVÁLIDO -> {e.message}")'),
        dica_prova("Portfólio: 4 fluxos reais com regras variadas provam o motor — "
                   "cada tipo de regra (min/max, enum, data) é um caso de teste."),
        exercicios([
            "Adicione regra de e-mail válido ao fluxo clientes (regex no motor).",
            "Crie um 5º fluxo (ex.: estoque).",
            "Documente os 4 fluxos no README.",
        ]),
        gabarito([
            ("Email",
             "Regra regex `^[\\w.+-]+@[\\w-]+\\.[\\w.]+$` no campo email — validação na "
             "camada de consistência."),
            ("Estoque",
             "Campos: produto, quantidade (min 0), armazém."),
            ("README",
             "Tabela dos fluxos com campos e regras — a documentação do produto."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana20_dia6_entregavel_admin_funcional",
    [
        header(
            "20", "6", "Entregável: seção Admin 100% funcional",
            "Integrar o editor, o validador, as permissões e os 4 fluxos no app admin — "
            "o entregável da Semana 20.",
            "Portfólio empresarial", "App admin com 4 fluxos no ar",
            "✅ Free Edition (app Streamlit)",
        ),
        teoria(
            "O que a Semana 20 entregou",
            "- Arquitetura + modelo de 6 tabelas\n"
            "- JSON Schema validador de YAML\n"
            "- Editor com diff/rollback\n"
            "- RBAC por fluxo\n"
            "- 4 fluxos YAML (Metas, Descontos, Preços, Clientes)",
        ),
        pratica("App admin integrado",
            "Monte o app Streamlit da seção admin."),
        code('# app_admin.py (Streamlit) — esqueleto completo\n'
             'import streamlit as st\n'
             'st.set_page_config(page_title="DataFlow Admin", layout="wide")\n'
             'st.title("⚙️ DataFlow Admin")\n'
             '\n'
             'usuario = "admin"  # na prática: auth do workspace\n'
             'st.sidebar.write(f"Usuário: {usuario}")\n'
             '\n'
             'aba = st.sidebar.radio("Seção", ["Fluxos", "Editor YAML", "Versões"])\n'
             '\n'
             'if aba == "Fluxos":\n'
             '    st.dataframe(spark.table("workspace.app.fluxos").toPandas())\n'
             'elif aba == "Editor YAML":\n'
             '    fluxo = st.selectbox("Fluxo", ["metas", "descontos", "precos", "clientes"])\n'
             '    yaml_atual = st.text_area("YAML", value=metas_yaml, height=300)\n'
             '    if st.button("Validar e salvar"):\n'
             '        try:\n'
             '            validate(instance=yaml.safe_load(yaml_atual), schema=json_schema)\n'
             '            salvar_versao(fluxo, yaml_atual, usuario)\n'
             '            st.success("Salvo!")\n'
             '        except Exception as e:\n'
             '            st.error(f"Inválido: {e.message}")\n'
             'elif aba == "Versões":\n'
             '    st.dataframe(spark.table("workspace.app.fluxo_versoes").toPandas())\n'
             'print("App admin integrado (edite, valide, salve, veja versões).")'),
        pratica("Validação final",
            "1. Publique o app admin.\n"
            "2. Edite um YAML inválido → erro claro.\n"
            "3. Edite válido → nova versão + diff.\n"
            "4. Teste permissões (usuário sem editar não vê o botão)."),
        code('# Checklist da Semana 20\n'
             'print("""\n'
             '- [x] 6 tabelas criadas\n'
             '- [x] JSON Schema validando\n'
             '- [x] Editor com diff/rollback\n'
             '- [x] RBAC por fluxo\n'
             '- [x] 4 fluxos YAML funcionando\n'
             '- [x] App admin publicado\n'
             '""")\n'
             'print("Próximo: Motor de Validações (Semana 21).")'),
        dica_prova("O app admin é o 'produto' que entrevistadores adoram: configuração "
                   "por YAML + validação + aprovação — mostra maturidade de produto, "
                   "não só de código."),
        exercicios([
            "Publique e compartilhe o app admin.",
            "Escreva o README do app (arquitetura, fluxos, permissões).",
        ]),
        gabarito([
            ("Compartilhar",
             "Peça para alguém testar o editor — feedback real melhora o produto."),
            ("README",
             "Diagrama (admin → YAML → validação → versões) + tabela de fluxos + "
             "permissões."),
        ]),
        footer([
            "App admin publicado.",
            "Editor + validação + diff/rollback funcionando.",
            "RBAC por fluxo aplicado.",
            "4 fluxos YAML versionados.",
        ]),
    ],
))
