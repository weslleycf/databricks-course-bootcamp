"""Semana 6 — Produção: Repos, DABs e CI/CD (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana6_dia1_databricks_repos_git_integracao",
    [
        header(
            "6", "1", "Databricks Repos: Git integrado ao workspace",
            "Conectar o repositório Git ao workspace com Repos — o fluxo de trabalho "
            "moderno de desenvolvimento de pipelines.",
            "DEP (IaC), carreira", "Repos conectado + branch workflow",
            "✅ Free Edition",
            dais="Repos é a base do fluxo Git no Databricks (dev → PR → main).",
        ),
        teoria(
            "O que são Repos",
            "**Databricks Repos** integra o seu repositório Git (GitHub/GitLab/Bitbucket) ao "
            "workspace: os notebooks viram arquivos versionados, editáveis no branch certo, "
            "com PR e merge pelo Git. É o padrão para times.\n\n"
            "Sem Repos, você tem notebooks soltos no workspace — sem versionamento real.",
        ),
        pratica("Conectando o Repo",
            "1. **Workspace → Add → Repo**.\n"
            "2. URL do seu repositório GitHub (o criado na Semana 2).\n"
            "3. Autentique (Personal Access Token com escopo `repo`).\n"
            "4. O repositório aparece no workspace como uma pasta com `workspace`.\n"
            "5. Navegue: os `.ipynb` deste curso podem ser importados para dentro do repo.",
        ),
        pratica("Branch workflow no Repos",
            "Trabalhe sempre em branch e integre via PR — o padrão de produção."),
        code('# Via UI do Repos\n'
             'print("""\n'
             '1. No repo, botão branch > criar branch: feature/semana6\n'
             '2. Edite notebooks nessa branch\n'
             '3. Commit + Push (botões no topo do repo)\n'
             '4. No GitHub: crie o PR e faça merge\n'
             '5. No Repos: pull para atualizar main\n'
             '""")\n'
             'print("Repos sincroniza com Git — commits e pushes direto do workspace.")'),
        teoria(
            "Workspace files vs notebooks",
            "**Workspace files** são arquivos de código puros (`.py`, `.yml`) versionáveis — "
            "o DLT e os DABs usam workspace files. Notebooks têm formato `.ipynb` e também "
            "ficam no Git via Repos.",
        ),
        dica_prova("A DEP cobra o fluxo Git: branch, PR, integração com CI/CD e o papel dos "
                   "Repos. Memorize os passos e a diferença para workspace files."),
        exercicios([
            "Conecte seu repo e crie a branch feature/semana6.",
            "Importe um notebook do curso para o repo e faça commit+push.",
            "O que acontece se você editar um notebook sem branch no Repos?",
        ]),
        gabarito([
            ("Conexão",
             "Workspace → Add → Repo → URL do GitHub → token → branch feature/semana6."),
            ("Importar + commit",
             "Botão Import no repo → escolha o .ipynb → botão 'Commit & Push' com mensagem "
             "conventional (ex.: feat: adiciona notebook semana 6)."),
            ("Sem branch",
             "Você edita direto em main — arriscado: sem PR/review e com conflitos. Em times, "
             "sempre branch + PR."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana6_dia2_dabs_fundamentos_bundle",
    [
        header(
            "6", "2", "DABs: Databricks Asset Bundles (IaC)",
            "Entender e configurar Databricks Asset Bundles: databricks.yml, recursos, "
            "ambientes (dev/staging/prod) e o fluxo validate/plan.",
            "DEP (IaC)", "Bundle validado localmente",
            "✅ Free Edition (validate/plan local) | 🔑 Versão paga (deploy)",
        ),
        teoria(
            "O que são DABs",
            "**Databricks Asset Bundles (DABs)** é o formato de **Infraestrutura como Código** "
            "(IaC) do Databricks: você define jobs, pipelines, notebooks e apps em YAML, e o "
            "Databricks **implantar** tudo com `bundle deploy`.\n\n"
            "Vantagens: versionado no Git, replicável em N ambientes, revisável em PR, e "
            "padrão oficial de produção (DEP).",
        ),
        teoria(
            "Estrutura de um bundle",
            "```\nmeu_bundle/\n ├── databricks.yml        # definição principal (recursos, targets)\n ├── resources/\n │   ├── jobs/             # jobs do bundle\n │   └── pipelines/        # pipelines DLT\n └── src/                  # código-fonte (notebooks, .py)\n```\n\n"
            "`databricks.yml` tem 3 blocos-chave: `bundle` (nome), `resources` (o que "
            "implantar), `targets` (ambientes dev/staging/prod com variáveis).",
        ),
        pratica("Criando o bundle",
            "Com o **Databricks CLI** instalado (`brew install databricks` / `pip install "
            "databricks-cli` — use o novo `databricks` CLI):"),
        code('# Terminal local — iniciar bundle\n'
             '!mkdir -p ~/bundle_vendas && cd ~/bundle_vendas\n'
             '!databricks bundle init default-python\n'
             'print("Bundle criado: databricks.yml + src/ + resources/")'),
        code('# databricks.yml mínimo (referência — crie/edit no seu projeto)\n'
             'yaml = """\n'
             'bundle:\n'
             '  name: vendas_bundle\n'
             'resources:\n'
             '  jobs:\n'
             '    job_ingestao:\n'
             '      name: job_ingestao\n'
             '      tasks:\n'
             '        - task_key: t1\n'
             '          notebook_task:\n'
             '            notebook_path: ./src/ingestao.ipynb\n'
             'targets:\n'
             '  dev:\n'
             '    mode: development\n'
             '  prod:\n'
             '    mode: production\n'
             '"""\n'
             'print(yaml)'),
        pratica("Validate e plan",
            "Valide o bundle localmente (sem deploy) — isso roda na Free Edition."),
        code('# Terminal local\n'
             '!databricks bundle validate -t dev\n'
             '!databricks bundle plan -t dev\n'
             'print("Validate/plan checam sintaxe, recursos e variáveis sem deploy.")'),
        dica_prova("DABs é tema central da DEP 2026: estrutura (databricks.yml, resources, "
                   "targets), comandos (validate, plan, deploy, run) e o papel no CI/CD. "
                   "Decore os 4 comandos."),
        exercicios([
            "Descreva a estrutura mínima de um bundle.",
            "Qual a diferença entre validate e plan? E deploy?",
            "O que `targets` define?",
        ]),
        gabarito([
            ("Estrutura",
             "databricks.yml + resources/ (jobs, pipelines) + src/ (código)."),
            ("Comandos",
             "validate = checa sintaxe/config local; plan = mostra o que seria implantado; "
             "deploy = aplica no workspace; run = executa o recurso."),
            ("targets",
             "Ambientes (dev/staging/prod) com modos, variáveis e configurações específicas "
             "de cada um."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana6_dia3_dabs_deploy_3_ambientes",
    [
        header(
            "6", "3", "Deploy real de DABs (trial pago) em 3 ambientes",
            "Implantar o bundle no workspace com `bundle deploy`, usando targets "
            "dev/staging/prod e variáveis por ambiente.",
            "DEP (IaC)", "Deploy dev/staging/prod concluído",
            "🔑 Versão paga (trial) — deploy exige workspace completo",
        ),
        teoria(
            "Por que o deploy exige a conta paga",
            "O `bundle deploy` cria recursos reais (jobs, pipelines) no workspace via API. A "
            "Free Edition limita jobs concorrentes e não expõe a mesma API de deploy — por "
            "isso, **este dia usa o trial pago** (14 dias) ou uma conta corporativa.\n\n"
            "> ⚠️ **Estratégia de trial**: concentre seus dias de trial nas Semanas 6, 7, 9, "
            "13, 15 e 19 — assim os 14 dias rendem o máximo.",
        ),
        pratica("Autenticando o CLI",
            "1. Crie um **PAT** (User Settings → Developer → Access Tokens) no workspace pago.\n"
            "2. Configure o profile:\n"
            "```\nexport DATABRICKS_HOST=https://dbc-xxxx.cloud.databricks.com\nexport DATABRICKS_TOKEN=dapi...\n```",
        ),
        code('# Terminal local — configurar e validar no trial\n'
             '!databricks auth login --host https://dbc-xxxx.cloud.databricks.com\n'
             '!databricks bundle validate -t dev\n'
             'print("Autenticado no workspace pago.")'),
        pratica("Deploy por ambiente",
            "Implante em dev, depois staging e prod — cada target tem sua configuração."),
        code('# Terminal local\n'
             '!databricks bundle deploy -t dev\n'
             '!databricks bundle run -t dev job_ingestao\n'
             'print("Deploy + run no ambiente dev concluídos.")'),
        code('# Staging e prod\n'
             '!databricks bundle deploy -t staging\n'
             '!databricks bundle deploy -t prod\n'
             'print("Staging e prod implantados.")'),
        teoria(
            "Boas práticas de produção",
            "- `mode: development` (dev) permite overwrite de recursos; `mode: production` "
            "protege (exige confirmação).\n"
            "- Use **variáveis** (`${var.nome}`) para diferenças por ambiente (ex.: catálogo "
            "`workspace_dev` vs `workspace_prod`).\n"
            "- Nunca rode `bundle destroy` sem revisar — remove recursos.",
        ),
        dica_prova("Pergunta DEP típica: 'como implantar o mesmo job em 3 ambientes?' → "
                   "targets + variáveis no databricks.yml + bundle deploy por target."),
        exercicios([
            "Implante um job com nome diferente por ambiente usando variável.",
            "O que `mode: production` protege?",
            "Rode `bundle plan -t prod` antes do deploy — o que ele mostra?",
        ]),
        gabarito([
            ("Variável por ambiente",
             "`targets: prod: variables: { catalog: workspace_prod }` e usar "
             "`${var.catalog}` no notebook — cada ambiente aponta para seu catálogo."),
            ("mode production",
             "Impede overwrite acidental de recursos existentes (exige confirmação) e "
             "registra a implantação como produção."),
            ("plan",
             "Mostra o diff do que seria criado/atualizado (recursos, nomes, configs) sem "
             "aplicar — o check final antes do deploy."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana6_dia4_ci_cd_github_actions_dabs",
    [
        header(
            "6", "4", "CI/CD com GitHub Actions + DABs",
            "Automatizar a implantação: pipeline de CI (testes/validate) e CD (deploy) com "
            "GitHub Actions e os blueprints oficiais do Databricks.",
            "DEP (CI/CD)", "Pipeline CI/CD rodando no GitHub",
            "🔑 Versão paga (deploy) — CI parcial na Free",
        ),
        teoria(
            "CI vs CD",
            "**CI (Continuous Integration)**: ao fazer push/PR, roda validação — `bundle "
            "validate`, testes, lint. Pega erro cedo.\n"
            "**CD (Continuous Deployment)**: após o merge na main, faz `bundle deploy -t "
            "prod` automaticamente.\n\n"
            "Os **blueprints oficiais** do Databricks (GitHub Actions) já trazem esse "
            "padrão pronto.",
        ),
        pratica("GitHub Actions para CI (roda localmente/validate — funciona na Free)",
            "Crie `.github/workflows/ci.yml` no repositório:"),
        code('# .github/workflows/ci.yml\n'
             'yaml_ci = """\n'
             'name: CI\n'
             'on:\n'
             '  pull_request:\n'
             '  push:\n'
             '    branches: [main]\n'
             'jobs:\n'
             '  validate:\n'
             '    runs-on: ubuntu-latest\n'
             '    steps:\n'
             '      - uses: actions/checkout@v4\n'
             '      - uses: databricks/setup-cli@main\n'
             '      - name: Validate bundle\n'
             '        run: databricks bundle validate -t dev\n'
             '"""\n'
             'print(yaml_ci)\n'
             'print("Coloque em .github/workflows/ci.yml e faça push.")'),
        pratica("CD no merge",
            "O workflow de CD roda o deploy no ambiente prod após merge na main."),
        code('# .github/workflows/cd.yml (usar secrets DATABRICKS_HOST/TOKEN no repo)\n'
             'yaml_cd = """\n'
             'name: CD\n'
             'on:\n'
             '  push:\n'
             '    branches: [main]\n'
             'jobs:\n'
             '  deploy:\n'
             '    runs-on: ubuntu-latest\n'
             '    env:\n'
             '      DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}\n'
             '      DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}\n'
             '    steps:\n'
             '      - uses: actions/checkout@v4\n'
             '      - uses: databricks/setup-cli@main\n'
             '      - name: Deploy to prod\n'
             '        run: databricks bundle deploy -t prod\n'
             '"""\n'
             'print(yaml_cd)'),
        pratica("Testes no CI",
            "Adicione um step que roda o notebook como teste (ex.: pytest sobre funções "
            "de transformação extraídas em `.py`)."),
        code('# Boa prática: extrair lógica para .py e testar com pytest\n'
             'codigo = """\n'
             'def filtra_e_enriquece(df):\n'
             '    return df.filter(col("Quantity") > 0).withColumn("receita", col("Quantity") * col("UnitPrice"))\n'
             '\n'
             'def test_filtra_e_enriquece(spark):\n'
             '    df = spark.createDataFrame([(1, 10.0), (-1, 5.0)], ["Quantity", "UnitPrice"])\n'
             '    out = filtra_e_enriquece(df)\n'
             '    assert out.count() == 1\n'
             '    assert out.collect()[0]["receita"] == 10.0\n'
             '"""\n'
             'print(codigo)'),
        dica_prova("A DEP cobra o papel do CI/CD e os blueprints oficiais. Memorize: CI "
                   "valida em PR; CD deploya em merge; secrets via GitHub Secrets."),
        exercicios([
            "Crie o workflow de CI no seu repo e rode um PR de teste.",
            "O que é um secret no GitHub Actions e onde configurá-lo?",
            "Por que CI roda validate e não deploy direto?",
        ]),
        gabarito([
            ("CI no repo",
             "Push do .github/workflows/ci.yml → abrir PR → ver o check 'validate' verde → "
             "merge."),
            ("Secrets",
             "Settings → Secrets and variables → Actions: DATABRICKS_HOST e DATABRICKS_TOKEN "
             "ficam criptografados; o workflow usa ${{ secrets.X }}."),
            ("validate não deploy",
             "Deploy em PR criaria recursos de staging/prod a cada commit — caro e arriscado. "
             "CI valida (rápido, sem efeito); CD deploya só no merge."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana6_dia5_cli_rest_api_secrets",
    [
        header(
            "6", "5", "Databricks CLI, REST API e secrets",
            "Operar o workspace via Databricks CLI e REST API 2.0, e gerenciar segredos "
            "(secrets) com boas práticas.",
            "DEP (plataforma)", "Scripts CLI + secrets criados",
            "✅ Free Edition (CLI/API) + 🔑 secrets avançados",
        ),
        teoria(
            "Databricks CLI",
            "O CLI (`databricks`) permite tudo o que a UI faz, via terminal: jobs, clusters, "
            "pipelines, bundles, tokens, secrets. É a base de automação e CI/CD.\n\n"
            "**REST API 2.0**: os mesmos recursos via HTTP (jobs, catalogs, warehouses...). "
            "CLI é um cliente da API.",
        ),
        pratica("Comandos essenciais",
            "Rode localmente (ou em %sh no notebook, se o domínio estiver liberado)."),
        code('# Terminal local\n'
             '!databricks auth login\n'
             '!databricks jobs list\n'
             '!databricks pipelines list\n'
             '!databricks catalogs list\n'
             'print("CLI conectado: jobs, pipelines, catálogos listados.")'),
        code('# REST API (exemplo com curl)\n'
             '!curl -H "Authorization: Bearer $DATABRICKS_TOKEN" \\\n'
             '  "$DATABRICKS_HOST/api/2.1/jobs/list"\n'
             'print("A API de jobs retorna JSON — usada por SDKs e scripts.")'),
        teoria(
            "Secrets — nunca credenciais em código",
            "Credenciais (senhas, tokens, chaves de API) **nunca** devem ficar em notebooks "
            "ou código. Use **Secret Scopes**: cofre gerenciado (Databricks-backed) ou "
            "integrado (Vault/Key Vault em produção).\n\n"
            "Acesso no notebook: `dbutils.secrets.get(scope='meu_scope', key='senha')`.",
        ),
        pratica("Criando e usando secrets",
            "No terminal (local) com o CLI conectado ao workspace."),
        code('# Terminal local\n'
             '!databricks secrets create-scope curso\n'
             '!databricks secrets put-secret curso senha_api --string-value "abc123"\n'
             'print("Scope curso criado com a secret senha_api.")'),
        code('# Uso no notebook — NUNCA imprima o valor em produção\n'
             'senha = dbutils.secrets.get(scope="curso", key="senha_api")\n'
             'print("Secret lida com sucesso (tamanho:", len(senha), "caracteres)")'),
        dica_prova("A DEP cobra: secrets scopes (Databricks-backed vs Key Vault), "
                   "dbutils.secrets.get, e a regra de nunca expor credenciais. "
                   "Na Free, scopes avançados (Key Vault) exigem conta paga."),
        exercicios([
            "Crie um scope e uma secret; leia no notebook sem imprimir o valor.",
            "Qual a diferença entre secrets Databricks-backed e Key Vault?",
            "Por que nunca colocar credenciais em variável de ambiente do notebook?",
        ]),
        gabarito([
            ("Prática",
             "`databricks secrets create-scope curso; put-secret ...` + "
             "`dbutils.secrets.get(...)` no notebook."),
            ("Tipos",
             "Databricks-backed: armazenado no cofre gerenciado pelo Databricks (bom para "
             "começar). Key Vault: integração com o cofre da nuvem (produção, rotação e "
             "auditoria centralizadas)."),
            ("Credenciais no notebook",
             "Ficam versionadas no Git (vazamento), sem rotação e sem auditoria. Secrets "
             "scopes centralizam e protegem."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana6_dia6_revisao_simulado_lakeflow_delta",
    [
        header(
            "6", "6", "Revisão + simulado parcial (Lakeflow/Delta)",
            "Consolidar Semanas 5–6 com um simulado no formato da prova, cobrindo DLT, Jobs, "
            "DABs e Delta.",
            "DEA, DEP (simulado)", "Simulado ≥ 70% + checklist",
            "✅ Free Edition",
        ),
        teoria(
            "O que a Semana 6 entregou",
            "Repos (Git no workspace), DABs (IaC com targets e variáveis), deploy em 3 "
            "ambientes (trial), CI/CD com GitHub Actions, e CLI/API/secrets. Esse é o "
            "diferencial que separa 'quem mexe em notebook' de 'engenheiro de dados'.",
        ),
        pratica("Simulado — Lakeflow, Delta e IaC (12 questões)",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** O que o `bundle validate` faz?
- A) implanta recursos  B) valida a config sem aplicar
- C) roda o job  D) apaga recursos

**2.** Em qual cenário usar `databricks bundle deploy -t prod`?
- A) em todo push  B) após merge na main (CD)
- C) só manual  D) nunca

**3.** Qual comando roda um recurso do bundle?
- A) `bundle plan`  B) `bundle run <nome>`  C) `bundle validate`  D) `bundle init`

**4.** Para um job rodar só após outro terminar:
- A) mesmo task_key  B) `depends_on`  C) `retry`  D) `schedule`

**5.** Secrets devem ser armazenados:
- A) no código  B) em secret scope  C) em .env versionado  D) no README

**6.** O DLT `@dlt.expect_or_fail`:
- A) descarta e continua  B) falha o pipeline se violar  C) só conta  D) nada

**7.** `cloudFiles` é usado para:
- A) ler streaming de arquivos novos  B) escrever Parquet  C) criar jobs  D) versionar

**8.** `checkpointLocation` garante:
- A) schema fixo  B) retomada sem reprocessar  C) mais velocidade  D) nada

**9.** Qual nomenclatura é a correta 2026 para orquestração?
- A) Databricks Workflows  B) Lakeflow Jobs  C) DLT Jobs  D) Jobs 2.0

**10.** `mode: development` no target dev:
- A) protege contra overwrite  B) permite overwrite livre
- C) desabilita jobs  D) nada

**11.** Um pipeline DLT pode ter:
- A) apenas notebooks  B) materialized + streaming tables  C) apenas R  D) apenas SQL

**12.** Para integrar Git ao workspace:
- A) DABs  B) Repos  C) Jobs  D) MLflow
"""),
        teoria(
            "Gabarito",
            "**1-B** · **2-B** · **3-B** · **4-B** · **5-B** · **6-B** · **7-A** · "
            "**8-B** · **9-B** · **10-B** · **11-B** · **12-B**.\n\n"
            "≥ 9/12 = pronto. Se errou DLT/DABs, revise os notebooks da semana.",
        ),
        dica_prova("'Qual comando/ferramenta para X' é o formato #1 da DEP. Revise a tabela "
                   "de ferramentas: Repos (Git), DABs (IaC), CLI (automação), Jobs "
                   "(orquestração), DLT (pipelines), Secrets (segredos)."),
        exercicios([
            "Escreva, do zero, um databricks.yml com 1 job e 2 targets.",
            "Explique o ciclo Git → CI → CD do seu projeto em 5 frases.",
        ]),
        gabarito([
            ("databricks.yml",
             "```yaml\nbundle:\n  name: vendas\nresources:\n  jobs:\n    j1:\n      name: j1\n      tasks:\n        - task_key: t\n          notebook_task: {notebook_path: ./src/n.ipynb}\ntargets:\n  dev: {mode: development}\n  prod: {mode: production}\n```"),
            ("Ciclo",
             "Edita na branch → PR → CI valida (validate) → merge na main → CD deploya "
             "(prod) → job roda no agendamento. Tudo versionado."),
        ]),
        footer([
            "Conectei meu repo com Repos.",
            "Criei bundle e validei localmente (validate/plan).",
            "Fiz deploy no trial em dev/staging/prod.",
            "Configurei CI/CD no GitHub Actions.",
            "Fiz o simulado e revisei os erros.",
        ]),
    ],
))
