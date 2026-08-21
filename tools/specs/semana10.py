"""Semana 10 — MLflow, ML lifecycle e Feature Engineering (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana10_dia1_mlflow_tracking_experimentos",
    [
        header(
            "10", "1", "MLflow: experiments, runs e tracking",
            "Dominar o MLflow Tracking: experiments, runs, autologging, params, metrics e "
            "artifacts — a base de todo MLOps no Databricks.",
            "MLP, MLA", "Primeiro experimento com autologging",
            "✅ Free Edition",
        ),
        teoria(
            "O que é o MLflow",
            "O **MLflow** é a plataforma open-source de ciclo de vida de ML — e está embutido "
            "no Databricks. Quatro componentes:\n\n"
            "1. **Tracking**: registrar params, metrics, artifacts e código de cada run\n"
            "2. **Models**: empacotar e versionar modelos (registry)\n"
            "3. **Model Registry**: governança de modelos (aliases, stages)\n"
            "4. **Evaluate/Tracing**: avaliar e debugar (LLMs também)\n\n"
            "**Experiment** = projeto (coleção de runs). **Run** = uma execução de treino "
            "com params/métricas/artifacts. Sem MLflow, você perde rastreabilidade.",
        ),
        teoria(
            "Autologging",
            "O `mlflow.autolog()` captura **automaticamente** params, métricas e modelos de "
            "frameworks (sklearn, xgboost, pytorch...) — sem instrumentação manual. "
            "É o padrão recomendado.",
        ),
        pratica("Primeiro experimento",
            "Treine um modelo simples de previsão de receita com autologging."),
        code('# Preparar dados de treino a partir do Ouro\n'
             'from pyspark.sql.functions import dayofweek, month, year\n'
             'df = (spark.table("workspace.ouro.vendas_por_dia")\n'
             '    .withColumn("dia_semana", dayofweek("data_venda"))\n'
             '    .withColumn("mes", month("data_venda"))\n'
             '    .withColumn("ano", year("data_venda"))\n'
             '    .toPandas())\n'
             'df.head()'),
        code('# Treino com autologging\n'
             'import mlflow\n'
             'import mlflow.sklearn\n'
             'from sklearn.ensemble import RandomForestRegressor\n'
             'from sklearn.model_selection import train_test_split\n'
             '\n'
             'mlflow.autolog()\n'
             'X = df[["dia_semana", "mes", "ano"]]\n'
             'y = df["receita_total"]\n'
             'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n'
             '\n'
             'with mlflow.start_run(run_name="rf_vendas_v1"):\n'
             '    modelo = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)\n'
             '    modelo.fit(X_train, y_train)\n'
             '    print("Run registrado no experimento!")'),
        code('# Ver os runs registrados\n'
             'experiments = mlflow.search_experiments()\n'
             'for e in experiments:\n'
             '    print(f"Experiment: {e.name} (id={e.experiment_id})")'),
        pratica("Explorando na UI",
            "1. **Experiments** (sidebar) → experimento do notebook.\n"
            "2. Veja: params (n_estimators, max_depth), métricas (rmse, r2), artifacts "
            "(model, requirements).\n"
            "3. Compare 2 runs com **Compare**.",
        ),
        dica_prova("MLP/MLA cobram: experimento vs run, autolog, e como registrar params/"
                   "métricas/artifacts. Pergunta clássica: 'o que o autolog registra?' → "
                   "params, métricas, modelo e código da run."),
        exercicios([
            "Rode o treino 2x com n_estimators diferentes e compare na UI.",
            "Registre uma métrica manual com mlflow.log_metric.",
            "O que é um artifact? Dê 3 exemplos.",
        ]),
        gabarito([
            ("Comparar runs",
             "Rode v1 e v2; em Experiments, selecione as duas e Compare: veja rmse/r2 lado a lado."),
            ("Métrica manual",
             "```python\nwith mlflow.start_run():\n    mlflow.log_metric('meu_rmse', 0.42)\n```"),
            ("Artifacts",
             "Arquivos anexados à run: modelo serializado, gráficos, dataset de amostra, "
             "requirements.txt."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana10_dia2_mlflow_registry_modelos_uc",
    [
        header(
            "10", "2", "MLflow Models e Model Registry no Unity Catalog",
            "Registrar modelos no UC (Unity Catalog models), versionar, usar aliases e "
            "governar o ciclo de vida do modelo.",
            "MLP (model governance)", "Modelo registrado no UC com alias",
            "✅ Free Edition",
        ),
        teoria(
            "Model Registry e UC models",
            "O **Model Registry** (2026: **MLflow Model Registry in Unity Catalog**) é o "
            "catálogo de modelos governados:\n\n"
            "- **UC models**: modelos registrados como objetos do UC (catalog.schema.model) "
            "— com permissões, linhagem e versionamento\n"
            "- **Aliases/stages**: `alias = 'champion'` (produção) vs `'challenger'` (candidato)\n"
            "- **Versionamento**: cada registro vira `Version 1, 2, 3...`\n\n"
            "> 🎯 **Dica de prova (MLP 2026)**: a migração do registry de workspace para "
            "UC é tema recorrente. Memorize: modelo no UC = `catalog.schema.model`.",
        ),
        pratica("Registrando o modelo",
            "Registre o modelo treinado como UC model com alias."),
        code('# Registrar o modelo treinado (continue da célula anterior)\n'
             'import mlflow\n'
             '# O autolog já registrou o modelo; promova para o UC:\n'
             'modelo_uri = "runs:/" + mlflow.last_active_run().info.run_id + "/model"\n'
             'mlflow.register_model(model_uri, "workspace.prata.modelo_previsao_receita")\n'
             'print("Modelo registrado no UC: workspace.prata.modelo_previsao_receita")'),
        code('# Definir alias (champion = produção)\n'
             'from mlflow.tracking import MlflowClient\n'
             'client = MlflowClient()\n'
             'client.set_registered_model_alias("workspace.prata.modelo_previsao_receita", "champion", "1")\n'
             'print("Alias champion apontando para a versão 1.")'),
        code('# Carregar o modelo pelo alias\n'
             'modelo = mlflow.sklearn.load_model(\n'
             '    "models:/workspace.prata.modelo_previsao_receita@champion")\n'
             'pred = modelo.predict(X_test[:5])\n'
             'print("Predições (5 primeiras):", pred)'),
        pratica("Governança na UI",
            "**Catalog → workspace.prata → modelo_previsao_receita**: veja versões, alias, "
            "permissões (GRANT) e linhagem do modelo.",
        ),
        dica_prova("MLP: pergunta típica 'qual alias indica produção?' → `champion`. "
                   "'Onde fica um modelo governado?' → Unity Catalog "
                   "(catalog.schema.model)."),
        exercicios([
            "Registre uma versão 2 do modelo e troque o alias champion para ela.",
            "Conceda permissão de leitura do modelo a um grupo.",
            "Qual a vantagem de modelo no UC vs registry de workspace?",
        ]),
        gabarito([
            ("Versão 2 + alias",
             "Treine de novo, `mlflow.register_model(...)` vira v2, "
             "`client.set_registered_model_alias(..., 'champion', '2')`."),
            ("Permissão",
             "`GRANT READ ON MODEL workspace.prata.modelo_previsao_receita TO analistas;`"),
            ("UC vs workspace",
             "UC: governança unificada (permissões, linhagem, auditoria) com todo o resto — "
             "padrão 2026. Workspace registry é legado."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana10_dia3_modelo_previsao_vendas_mlflow",
    [
        header(
            "10", "3", "ML lifecycle: modelo de previsão de vendas",
            "Construir o modelo completo de previsão de receita do projeto com MLflow: "
            "features, treino, avaliação e baseline.",
            "MLP, MLA", "Modelo treinado e avaliado no MLflow",
            "✅ Free Edition",
        ),
        teoria(
            "O modelo do projeto",
            "Vamos prever a **receita diária** com base em features temporais (dia da semana, "
            "mês, ano, feriado). Isso exercita o fluxo real de ML: features → treino → "
            "avaliação → registro.",
        ),
        pratica("Features + treino",
            "Prepare features e treine o modelo com busca simples de hiperparâmetros."),
        code('# Features de calendário a partir do Ouro\n'
             'from pyspark.sql.functions import dayofweek, month, year, dayofmonth, lag as lagf\n'
             'from pyspark.sql.window import Window\n'
             'df = (spark.table("workspace.ouro.vendas_por_dia")\n'
             '    .withColumn("dia_semana", dayofweek("data_venda"))\n'
             '    .withColumn("dia_mes", dayofmonth("data_venda"))\n'
             '    .withColumn("mes", month("data_venda"))\n'
             '    .withColumn("ano", year("data_venda"))\n'
             '    .toPandas())\n'
             'print(df.shape)'),
        code('# Treino com busca de hiperparâmetros (2 runs)\n'
             'import mlflow\n'
             'from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n'
             'from sklearn.model_selection import train_test_split\n'
             'from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error\n'
             '\n'
             'X = df[["dia_semana", "dia_mes", "mes", "ano"]]\n'
             'y = df["receita_total"]\n'
             'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)\n'
             '\n'
             'mlflow.autolog()\n'
             'with mlflow.start_run(run_name="gbm_vendas"):\n'
             '    modelo = GradientBoostingRegressor(n_estimators=150, max_depth=5, learning_rate=0.1)\n'
             '    modelo.fit(X_train, y_train)\n'
             '    pred = modelo.predict(X_test)\n'
             '    mlflow.log_metrics({"rmse": mean_squared_error(y_test, pred)**0.5,\n'
             '                        "mae": mean_absolute_error(y_test, pred),\n'
             '                        "r2": r2_score(y_test, pred)})\n'
             '    print("Run GBM registrada.")'),
        pratica("Comparação e baseline",
            "Na UI: compare as runs; uma métrica de baseline (ex.: prever sempre a média) "
            "mostra se o modelo agrega valor."),
        code('# Baseline: prever a média (regra simples)\n'
             'from sklearn.metrics import r2_score, mean_squared_error\n'
             'import numpy as np\n'
             'baseline = np.full_like(y_test, y_train.mean())\n'
             'print("Baseline RMSE:", mean_squared_error(y_test, baseline)**0.5)\n'
             'print("R2 do baseline (deve ser <= 0):", r2_score(y_test, baseline))\n'
             'print("Se o modelo ML tiver R2 > 0 e RMSE < baseline, ele agrega valor.")'),
        dica_prova("MLP: saber ler métricas (RMSE/MAE/R2) e comparar com baseline é "
                   "pergunta garantida. R2 > 0 já indica ganho sobre a média."),
        exercicios([
            "Registre o melhor modelo com alias champion.",
            "O que significaria um R2 negativo?",
            "Treine com uma feature extra (ex.: lag da receita) e compare.",
        ]),
        gabarito([
            ("Registrar champion",
             "`mlflow.register_model('runs:/<run_id>/model', 'workspace.prata.modelo_previsao_receita')` "
             "+ set alias champion na versão nova."),
            ("R2 negativo",
             "O modelo prevê PIOR que a média — sinal de features ruins ou overfit. Volte às "
             "features."),
            ("Lag feature",
             "Adicione `lag(receita, 7)` (janela de 7 dias) via Window no Spark; se o R2 "
             "subir, a sazonalidade semanal explica parte da receita."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana10_dia4_feature_engineering_uc",
    [
        header(
            "10", "4", "Feature Engineering in Unity Catalog",
            "Criar feature tables governadas no UC, servir features online/offline e "
            "entender o papel no MLP 2026 (antigo Feature Store).",
            "MLP (2026)", "Feature table criada + consumida",
            "✅ Free Edition (offline) + 🔑 serving online (trial)",
        ),
        teoria(
            "Feature Engineering in UC (2026)",
            "Antes chamado **Feature Store**, agora é **Feature Engineering in Unity "
            "Catalog**: feature tables governadas no UC (catalog.schema.table), com "
            "linhagem, versionamento e reuso entre equipes.\n\n"
            "- **Feature table**: tabela com `primary_keys` e colunas de features\n"
            "- **Offline**: features usadas no treino (batch)\n"
            "- **Online (Feature Serving)**: features servidas em tempo real na inferência "
            "(🔑 pago)\n\n"
            "> 🎯 **Dica de prova (MLP 2026)**: 'qual recurso gerencia features?' → Feature "
            "Engineering in UC; a nomenclatura nova é cobrada.",
        ),
        pratica("Criando a feature table",
            "Crie a feature table de calendário com o pacote `databricks-feature-engineering`."),
        code('# Criar feature table no UC\n'
             'from databricks.feature_engineering import FeatureEngineeringClient, FeatureLookup\n'
             'from pyspark.sql.functions import dayofweek, month, year, dayofmonth\n'
             'fe = FeatureEngineeringClient()\n'
             '\n'
             'features_df = (spark.table("workspace.ouro.vendas_por_dia")\n'
             '    .select("data_venda")\n'
             '    .withColumn("dia_semana", dayofweek("data_venda"))\n'
             '    .withColumn("dia_mes", dayofmonth("data_venda"))\n'
             '    .withColumn("mes", month("data_venda"))\n'
             '    .withColumn("ano", year("data_venda")))\n'
             'fe.create_table(\n'
             '    name="workspace.prata.features_calendario",\n'
             '    primary_keys=["data_venda"],\n'
             '    df=features_df,\n'
             '    description="Features de calendário para previsão de receita")\n'
             'print("Feature table criada: workspace.prata.features_calendario")'),
        code('# Reutilizar features no treino (point-in-time correto)\n'
             'treino = fe.create_training_set(\n'
             '    df=spark.table("workspace.ouro.vendas_por_dia").select("data_venda", "receita_total"),\n'
             '    label="receita_total",\n'
             '    feature_lookups=[\n'
             '        FeatureLookup(table_name="workspace.prata.features_calendario",\n'
             '                      lookup_key="data_venda")])\n'
             'df_treino = treino.load_df().toPandas()\n'
             'print("Treino com features do UC pronto:", df_treino.shape)'),
        pratica("Servindo features online (trial)",
            "No workspace pago: **Catalog → workspace.prata.features_calendario → Feature "
            "Serving → Create endpoint** — a tabela vira endpoint de baixa latência para "
            "inferência em tempo real."),
        code('# Consumo online em produção (🔑)\n'
             'print("""\n'
             '1. Catalog > features_calendario > Feature Serving\n'
             '2. Create endpoint (serverless)\n'
             '3. O endpoint recebe primary_keys e retorna features:\n'
             '   POST /serving-endpoints/features_calendario/invocations\n'
             '   {"dataframe_records": [{"data_venda": "2024-11-20"}]}\n'
             '""")\n'
             'print("Feature Serving: inferência em tempo real com as mesmas features do treino.")'),
        dica_prova("MLP: feature table = tabela com primary_keys; training set com "
                   "FeatureLookup evita data leakage; online serving é para inferência "
                   "em tempo real."),
        exercicios([
            "Crie uma feature table com 2 colunas novas (ex.: media_receita_7d).",
            "Por que usar FeatureLookup em vez de join manual?",
            "O que é data leakage e como o training set evita?",
        ]),
        gabarito([
            ("Feature nova",
             "Calcule a média móvel de 7 dias no Spark e `fe.create_table(...)` com a nova "
             "coluna."),
            ("FeatureLookup",
             "Garante point-in-time correctness (features do momento certo, sem vazar "
             "futuro) e versionamento/linhagem — join manual não faz isso."),
            ("Data leakage",
             "Usar informação futura no treino (ex.: receita de amanhã). O training set "
             "alinha features ao timestamp da label — sem vazar."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana10_dia5_mlflow_evaluate_modelos",
    [
        header(
            "10", "5", "mlflow.evaluate: avaliação de modelos",
            "Avaliar modelos de forma padronizada com mlflow.evaluate (métricas clássicas e "
            "LLM-as-judge) — base da avaliação de RAG na Semana 12.",
            "MLP, GenAI", "Avaliação registrada no MLflow",
            "✅ Free Edition",
        ),
        teoria(
            "mlflow.evaluate",
            "O `mlflow.evaluate` roda **avaliações padronizadas** e registra no MLflow:\n\n"
            "- Modelos clássicos: RMSE, MAE, R2, precisão/recall, curvas\n"
            "- LLMs (LLM-as-judge): faithfulness, answer relevance, ... (Semana 12)\n"
            "- Modelos de texto: perplexity, toxicity\n\n"
            "Vantagem: métricas comparáveis entre runs e auditáveis.",
        ),
        pratica("Avaliação clássica",
            "Avalie o modelo de vendas com mlflow.evaluate."),
        code('# Avaliação padronizada\n'
             'import mlflow\n'
             'with mlflow.start_run(run_name="avaliacao_vendas"):\n'
             '    results = mlflow.evaluate(\n'
             '        model="models:/workspace.prata.modelo_previsao_receita@champion",\n'
             '        data=X_test.assign(receita_total=y_test),\n'
             '        targets="receita_total",\n'
             '        model_type="regressor")\n'
             '    print("Métricas:", {k: round(v, 3) for k, v in results.metrics.items() if isinstance(v, float)})'),
        code('# Ver a avaliação na UI\n'
             'print("Experiments > run avaliacao_vendas > Metrics: veja rmse, mae, r2.")'),
        pratica("Avaliação com baseline",
            "Compare o modelo vs baseline dentro do próprio evaluate."),
        code('# Com baseline (mlflow guarda a comparação)\n'
             'import pandas as pd\n'
             'import numpy as np\n'
             'baseline_predictions = pd.Series(np.full(len(X_test), y_train.mean()))\n'
             'with mlflow.start_run(run_name="avaliacao_com_baseline"):\n'
             '    mlflow.evaluate(\n'
             '        model="models:/workspace.prata.modelo_previsao_receita@champion",\n'
             '        data=X_test.assign(receita_total=y_test),\n'
             '        targets="receita_total",\n'
             '        model_type="regressor",\n'
             '        baseline_model=baseline_predictions)\n'
             '    print("Comparação vs baseline registrada.")'),
        dica_prova("MLP/GenAI: `mlflow.evaluate` aceita `model_type` (regressor/classifier/"
                   "llm) e `baseline_model`. É o padrão para comparar modelos."),
        exercicios([
            "Avalie o modelo com model_type='regressor' e anote o RMSE.",
            "O que o baseline_model faz na avaliação?",
            "Por que a avaliação padronizada importa em produção?",
        ]),
        gabarito([
            ("RMSE",
             "Veja na run avaliacao_vendas a métrica rmse (~milhar de unidades de receita)."),
            ("Baseline",
             "Compara o modelo a uma regra simples — se o modelo não vence o baseline, não "
             "agrega valor."),
            ("Produção",
             "Padroniza a medição entre versões, audita decisões e permite rejeitar "
             "regressões ao atualizar o modelo."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana10_dia6_entregavel_mlflow_simulado_mlp",
    [
        header(
            "10", "6", "Entregável: MLflow completo + simulado MLP",
            "Fechar a Semana 10: modelo de ponta a ponta no MLflow (tracking → registry → "
            "evaluate) e um simulado parcial de ML.",
            "MLP, MLA", "Modelo versionado + simulado ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "O ciclo completo que você dominou",
            "```\nfeatures (Ouro + Feature Engineering)\n   → treino (autolog)\n   → registro (UC model + alias champion)\n   → avaliação (mlflow.evaluate vs baseline)\n   → decisão de deploy (Semana 13: Model Serving)\n```\n"
            "Esse é o **MLOps** — o que separa ML de brinquedo de ML em produção.",
        ),
        pratica("Entregável integrado",
            "Rode o fluxo completo do zero."),
        code('# 1) Treinar e registrar (autolog)\n'
             'import mlflow\n'
             'from sklearn.ensemble import RandomForestRegressor\n'
             'from sklearn.model_selection import train_test_split\n'
             'mlflow.autolog()\n'
             'X = df[["dia_semana", "dia_mes", "mes", "ano"]]\n'
             'y = df["receita_total"]\n'
             'X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)\n'
             'with mlflow.start_run(run_name="entrega_final"):\n'
             '    m = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)\n'
             '    m.fit(X_train, y_train)\n'
             '    mlflow.sklearn.log_model(m, "model")\n'
             'print("Modelo treinado.")'),
        code('# 2) Registrar no UC com alias champion\n'
             'from mlflow.tracking import MlflowClient\n'
             'client = MlflowClient()\n'
             'uri = "runs:/" + mlflow.last_active_run().info.run_id + "/model"\n'
             'v = mlflow.register_model(uri, "workspace.prata.modelo_previsao_receita")\n'
             'client.set_registered_model_alias("workspace.prata.modelo_previsao_receita", "champion", str(v.version))\n'
             'print(f"Versão {v.version} promovida a champion.")'),
        code('# 3) Avaliar\n'
             'with mlflow.start_run(run_name="avaliacao_final"):\n'
             '    mlflow.evaluate(\n'
             '        model="models:/workspace.prata.modelo_previsao_receita@champion",\n'
             '        data=X_test.assign(receita_total=y_test),\n'
             '        targets="receita_total",\n'
             '        model_type="regressor")\n'
             'print("Avaliação final registrada.")'),
        pratica("Simulado MLP parcial (10 questões)",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** O `mlflow.autolog()` registra:
- A) apenas o modelo  B) params, métricas, modelo e código  C) nada  D) só datasets

**2.** Alias para modelo em produção:
- A) "dev"  B) "champion"  C) "latest"  D) "prod_v1"

**3.** Feature table no UC é criada com:
- A) CREATE TABLE normal  B) FeatureEngineeringClient.create_table  C) dlt.table  D) AutoML

**4.** `FeatureLookup` serve para:
- A) lookup SQL  B) point-in-time correctness  C) cache  D) nada

**5.** `mlflow.evaluate` com model_type="regressor" mede:
- A) precisão  B) RMSE/MAE/R2  C) tokens  D) latência

**6.** Baseline em avaliação:
- A) apaga o modelo  B) compara com regra simples  C) treina de novo  D) nada

**7.** Modelo no UC (2026):
- A) registry de workspace  B) catalog.schema.model  C) artifact store  D) notebook

**8.** Data leakage é:
- A) vazar informação futura no treino  B) bug de rede  C) cache  D) nada

**9.** Para servir features em tempo real:
- A) Feature Serving (🔑)  B) cache  C) DABs  D) MLflow UI

**10.** MLflow Tracking guarda:
- A) experiments e runs  B) apenas logs  C) só modelos  D) jobs
"""),
        teoria(
            "Gabarito",
            "**1-B** · **2-B** · **3-B** · **4-B** · **5-B** · **6-B** · **7-B** · "
            "**8-A** · **9-A** · **10-A**. ≥ 7/10 = pronto para a fase GenAI.",
        ),
        dica_prova("MLP 2026: nomenclatura 'Feature Engineering in UC' e 'MLflow Model "
                   "Registry in UC' caem direto. Memorize os dois renames."),
        exercicios([
            "Documente o ciclo MLflow do seu projeto no README.",
            "O que muda entre a versão 1 e a versão 2 do modelo? (consulte a UI)",
        ]),
        gabarito([
            ("README",
             "Descreva: features (Ouro + FE) → treino (autolog) → registro (UC) → alias "
             "champion → avaliação (evaluate vs baseline)."),
            ("Versões",
             "Compare params e métricas das versões na UI do modelo — documente qual venceu "
             "e por quê (RMSE)."),
        ]),
        footer([
            "Treinei, registrei e avaliei o modelo no MLflow.",
            "Criei feature table no UC.",
            "Entendo alias champion/challenger e baseline.",
            "Fiz o simulado MLP e revisei erros.",
        ]),
    ],
))
