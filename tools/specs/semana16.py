"""Semana 16 — Databricks Apps: fundamentos (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana16_dia1_apps_arquitetura_app_yaml",
    [
        header(
            "16", "1", "Databricks Apps: arquitetura e app.yaml",
            "Entender a arquitetura de Apps (web apps gerenciados) e publicar o primeiro "
            "app com autenticação nativa.",
            "GenAI Assoc (deploy), portfólio", "Primeiro app publicado",
            "✅ Free Edition (até 3 apps, auto-stop 24h)",
        ),
        teoria(
            "O que são Databricks Apps",
            "**Databricks Apps** publica aplicações web (Streamlit, Flask, FastAPI, "
            "Next.js...) rodando na infraestrutura gerenciada — SEM Kubernetes, com "
            "**autenticação e governança nativas** (Unity Catalog).\n\n"
            "Na Free Edition: **até 3 apps**; apps param sozinhos após 24h (restart manual).",
        ),
        teoria(
            "Estrutura de um app",
            "```\napp/\n ├── app.yaml        # declaração do app (comando, ambiente)\n ├── requirements.txt\n └── app.py          # código (Streamlit/FastAPI)\n```\n\n"
            "`app.yaml` mínimo:\n"
            "```yaml\nenv:\n  - name: APP_ENV\n    value: production\ncommand:\n  - streamlit\n  - run\n  - app.py\n```",
        ),
        pratica("Primeiro app Streamlit",
            "Crie o app de BI de vendas."),
        code('# app.py (Streamlit) — dashboard de vendas\n'
             'import streamlit as st\n'
             'import pyspark.sql.functions as F\n'
             'from pyspark.sql import SparkSession\n'
             '\n'
             'spark = SparkSession.builder.getOrCreate()\n'
             'st.set_page_config(page_title="Vendas", layout="wide")\n'
             'st.title("📊 Painel de Vendas")\n'
             '\n'
             'df = spark.table("workspace.ouro.vendas_por_dia").toPandas()\n'
             'st.line_chart(df.set_index("data_venda")["receita_total"])\n'
             'st.dataframe(df.tail(30))\n'
             'print("Código do app Streamlit (app.py).")'),
        code('# app.yaml\n'
             'yaml_app = """\n'
             'env:\n'
             '  - name: APP_ENV\n'
             '    value: production\n'
             'command:\n'
             '  - streamlit\n'
             '  - run\n'
             '  - app.py\n'
             '"""\n'
             'print(yaml_app)\n'
             'print("Coloque app.py + app.yaml + requirements.txt na pasta do app.")'),
        pratica("Publicando",
            "1. **Apps → Create App** → nomeie e selecione a pasta.\n"
            "2. Escolha o runtime (Python).\n"
            "3. **Start**. O Databricks builda e publica.\n"
            "4. Acesse o URL gerado (auth nativa com sua conta).\n"
            "5. Na Free, o app para após 24h — reinicie quando precisar.",
        ),
        dica_prova("Apps: `app.yaml` declara o comando; a plataforma gerencia build/deploy/"
                   "auth. Pergunta: 'como publicar uma UI sem Kubernetes?' → Databricks "
                   "Apps."),
        exercicios([
            "O que o app.yaml declara?",
            "Por que Apps têm auth nativa?",
            "Publique o app e compartilhe o link (2 pessoas).",
        ]),
        gabarito([
            ("app.yaml",
             "O comando de execução e variáveis de ambiente — o Databricks gerencia o "
             "resto (build, escala, auth)."),
            ("Auth nativa",
             "Quem acessa o URL passa pelo login do workspace — sem implementar "
             "autenticação você mesmo."),
            ("Compartilhar",
             "Qualquer usuário do workspace (ou público, se permitido) acessa com a "
             "permissão configurada."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana16_dia2_app_dashboard_streamlit_ouro",
    [
        header(
            "16", "2", "Dashboard Streamlit com o Ouro",
            "Construir o app de BI profissional: KPIs, gráficos interativos e filtros "
            "sobre a camada Ouro.",
            "Portfólio (BI)", "App de BI com KPIs publicado",
            "✅ Free Edition",
        ),
        teoria(
            "BI em app vs dashboard SQL",
            "O **dashboard do Databricks SQL** é rápido e sem código. O **app Streamlit** "
            "dá liberdade total (filtros custom, layout, interação). Use os dois: SQL "
            "para consumo rápido, app para produto.",
        ),
        pratica("App de BI completo",
            "KPIs + gráficos + filtro."),
        code('# app.py — BI completo\n'
             'import streamlit as st\n'
             'from pyspark.sql import SparkSession\n'
             'import pandas as pd\n'
             'spark = SparkSession.builder.getOrCreate()\n'
             '\n'
             'st.set_page_config(page_title="BI Vendas", layout="wide")\n'
             'st.title("📊 BI Vendas")\n'
             '\n'
             '@st.cache_data\n'
             'def carregar():\n'
             '    return spark.table("workspace.ouro.vendas_por_dia").toPandas()\n'
             '\n'
             'df = carregar()\n'
             'receita_total = df["receita_total"].sum()\n'
             'c1, c2, c3 = st.columns(3)\n'
             'c1.metric("Receita total", f"R$ {receita_total:,.0f}")\n'
             'c2.metric("Dias com dados", len(df))\n'
             'c3.metric("Ticket médio", f"R$ {df[\'n_notas\'].mean():,.0f}")\n'
             '\n'
             'st.line_chart(df.set_index("data_venda")["receita_total"])\n'
             'st.bar_chart(df.set_index("data_venda")["n_vendas"])\n'
             'print("App de BI com KPIs e gráficos pronto.")'),
        pratica("Filtro de período",
            "Adicione seleção de mês."),
        code('# Filtro de mês no app\n'
             'import streamlit as st\n'
             'from pyspark.sql import SparkSession\n'
             'spark = SparkSession.builder.getOrCreate()\n'
             'df = spark.table("workspace.ouro.vendas_por_dia").toPandas()\n'
             'df["mes"] = pd.to_datetime(df["data_venda"]).dt.month\n'
             'mes = st.selectbox("Mês", sorted(df["mes"].unique()))\n'
             'st.write(df[df["mes"] == mes].tail(10))\n'
             'print("Filtro de mês adicionado.")'),
        pratica("Publicar v2",
            "Atualize o app e re-deploy (o Databricks rebuilda)."),
        dica_prova("Streamlit: `st.metric` (KPI), `st.line_chart`, `st.selectbox` (filtro) "
                   "e `@st.cache_data` (evita reler a tabela a cada interação) — o "
                   "vocabulário dos apps de dados."),
        exercicios([
            "Adicione um gráfico de receita por país.",
            "O que `@st.cache_data` faz?",
            "Por que o app lê o Ouro e não o Bronze?",
        ]),
        gabarito([
            ("Por país",
             "Carregue `receita_por_pais` e use `st.bar_chart` — as tabelas Ouro já estão "
             "prontas."),
            ("cache_data",
             "Guarda o resultado da função (dataframe) em cache — interações rápidas sem "
             "reconsultar o lakehouse."),
            ("Ouro",
             "Dados limpos, modelados e estáveis — o app é consumidor final, não "
             "engenheiro de dados."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana16_dia3_app_rag_ui_chat",
    [
        header(
            "16", "3", "App RAG com UI de chat",
            "Publicar o RAG como app de chat com citações, feedback e estados.",
            "GenAI Assoc (deploy)", "App de chat RAG publicado",
            "✅ Free Edition",
        ),
        teoria(
            "Chat RAG em produção",
            "O app de chat precisa de: histórico de mensagens, streaming (ou resposta "
            "rápida), **citações de fonte** e **feedback** (👍/👎) — o feedback alimenta "
            "o golden set.",
        ),
        pratica("App de chat",
            "Streamlit com histórico e citações."),
        code('# app.py — chat RAG\n'
             'import streamlit as st\n'
             'from databricks.vector_search.client import VectorSearchClient\n'
             'from langchain_community.chat_models import ChatDatabricks\n'
             '\n'
             'st.set_page_config(page_title="RAG Produtos", layout="wide")\n'
             'st.title("🔍 Assistente de Produtos (RAG)")\n'
             '\n'
             'vsc = VectorSearchClient()\n'
             'idx = vsc.get_index("workspace.prata.produtos_rag_index")\n'
             'llm = ChatDatabricks(endpoint="databricks-llama-3-1-70b", temperature=0.1)\n'
             '\n'
             'if "historico" not in st.session_state:\n'
             '    st.session_state.historico = []\n'
             '\n'
             'pergunta = st.chat_input("Pergunte sobre os produtos...")\n'
             'if pergunta:\n'
             '    resultados = idx.similarity_search(query_text=pergunta, columns=["StockCode", "texto"], num_results=3)\n'
             '    contexto = "\\n".join(r[1] for r in resultados["result"]["data_array"])\n'
             '    resposta = llm.invoke(f"Contexto:\\n{contexto}\\n\\nPergunta: {pergunta}").content\n'
             '    st.session_state.historico.append((pergunta, resposta, resultados))\n'
             '\n'
             'for pergunta, resposta, resultados in st.session_state.historico:\n'
             '    st.chat_message("user").write(pergunta)\n'
             '    st.chat_message("assistant").write(resposta)\n'
             '    with st.expander("Fontes"):\n'
             '        for r in resultados["result"]["data_array"]:\n'
             '            st.write(f"• {r[0]}: {r[1][:100]}")\n'
             'print("App de chat RAG com fontes pronto.")'),
        pratica("Feedback",
            "Adicione botões 👍/👎 que gravam o feedback numa tabela."),
        code('# Feedback gravado em Delta\n'
             'import streamlit as st\n'
             'from pyspark.sql import SparkSession\n'
             'spark = SparkSession.builder.getOrCreate()\n'
             'def salvar_feedback(pergunta, resposta, nota):\n'
             '    spark.createDataFrame([(pergunta, resposta, nota)], ["pergunta", "resposta", "nota"])\\\n'
             '        .write.mode("append").saveAsTable("workspace.audit.feedback_rag")\n'
             'if st.button("👍 Útil"):\n'
             '    salvar_feedback(pergunta, resposta, 1)\n'
             'if st.button("👎 Não útil"):\n'
             '    salvar_feedback(pergunta, resposta, 0)\n'
             'print("Feedback gravado em workspace.audit.feedback_rag.")'),
        dica_prova("GenAI/portfólio: chat com citações + feedback é o padrão de produto "
                   "RAG. O feedback alimenta o golden set e a melhoria contínua."),
        exercicios([
            "Publique o chat RAG e teste com 5 perguntas.",
            "O que o feedback 👍/👎 permite melhorar?",
            "Como as citações aumentam a confiança do usuário?",
        ]),
        gabarito([
            ("Teste",
             "Verifique se as respostas usam o contexto e se as fontes correspondem."),
            ("Feedback",
             "Identifica perguntas que falham → vira golden set → avaliação → melhoria do "
             "retrieval."),
            ("Citações",
             "O usuário confere a fonte — transparência que reduz 'achismo' e aumenta "
             "adoção."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana16_dia4_app_fastapi_agente",
    [
        header(
            "16", "4", "Backend FastAPI + integração com o agente",
            "Criar uma API FastAPI que expõe o agente de vendas (e o RAG) como endpoints "
            "REST — o backend dos apps.",
            "GenAI Assoc (deploy)", "API FastAPI publicada",
            "✅ Free Edition",
        ),
        teoria(
            "Arquitetura app + API",
            "Em produção, separa-se UI (Streamlit/React) de **backend (API)** — o app "
            "chama a API, que chama o agente/lakehouse. Isso permite: reuso da API, "
            "escala independente e segurança centralizada.\n\n"
            "O **FastAPI** é o padrão Python para isso (async, OpenAPI automático).",
        ),
        pratica("API FastAPI do agente",
            "Crie o backend que chama o agente de vendas."),
        code('# main.py (FastAPI) — API do agente\n'
             'from fastapi import FastAPI\n'
             'from pydantic import BaseModel\n'
             'from langchain_community.chat_models import ChatDatabricks\n'
             '\n'
             'app = FastAPI(title="API de Vendas")\n'
             '\n'
             'class Pergunta(BaseModel):\n'
             '    texto: str\n'
             '\n'
             '@app.get("/health")\n'
             'def health():\n'
             '    return {"status": "ok"}\n'
             '\n'
             '@app.post("/perguntar")\n'
             'def perguntar(p: Pergunta):\n'
             '    llm = ChatDatabricks(endpoint="databricks-llama-3-1-70b")\n'
             '    return {"resposta": llm.invoke(p.texto).content}\n'
             'print("API FastAPI com /health e /perguntar.")'),
        code('# requirements.txt do app\n'
             'print("""\n'
             'fastapi\n'
             'uvicorn\n'
             'pyspark\n'
             'langchain\n'
             'langchain-community\n'
             'databricks-vector-search\n'
             '""")'),
        pratica("Publicando",
            "1. Pasta do app com `main.py` + `app.yaml` (comando: `uvicorn main:app --host "
            "0.0.0.0 --port 8080`).\n"
            "2. **Apps → Create App**.\n"
            "3. Teste: `https://<app>.cloud.databricks.com/health`.",
        ),
        code('# app.yaml para FastAPI\n'
             'yaml = """\n'
             'command:\n'
             '  - uvicorn\n'
             '  - main:app\n'
             '  - --host\n'
             '  - 0.0.0.0\n'
             '  - --port\n'
             '  - "8080"\n'
             '"""\n'
             'print(yaml)'),
        dica_prova("Apps/API: FastAPI + app.yaml + endpoint público = backend de "
                   "produção. Pergunta: 'como expor o agente como API?' → FastAPI "
                   "publicado como Databricks App (ou Model Serving)."),
        exercicios([
            "Adicione um endpoint /produtos que retorna o top-10 do Ouro.",
            "Por que separar UI de API?",
            "Qual a diferença entre publicar via Apps vs Model Serving?",
        ]),
        gabarito([
            ("/produtos",
             "Endpoint que lê `workspace.ouro.top_produtos` e retorna JSON."),
            ("Separar",
             "Reuso, escala independente, testes e segurança — a UI pode mudar sem tocar "
             "a API."),
            ("Apps vs Serving",
             "Apps: web app completo (UI+API) gerenciado. Serving: endpoint de inferência "
             "de modelo/agente (mais barato p/ só API)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana16_dia5_ci_cd_apps_observabilidade",
    [
        header(
            "16", "5", "CI/CD para Apps e observabilidade",
            "Versionar e implantar apps com DABs + GitHub Actions, e monitorar apps "
            "(logs, métricas, escala).",
            "DEP (CI/CD), portfólio", "Pipeline de deploy do app",
            "✅ Free Edition (CI) + 🔑 deploy via API (trial)",
        ),
        teoria(
            "Deploy de apps como código",
            "Apps podem ser deployados via **DABs** (`resources.apps`) e CI/CD — o mesmo "
            "fluxo de pipelines: PR valida, merge deploya.",
        ),
        pratica("App no DABs",
            "Adicione o app ao bundle."),
        code('# databricks.yml com app\n'
             'yaml = """\n'
             'bundle:\n'
             '  name: vendas_apps\n'
             'resources:\n'
             '  apps:\n'
             '    app_vendas:\n'
             '      name: app-vendas\n'
             '      source:\n'
             '        path: ./apps/dashboard\n'
             'targets:\n'
             '  dev:\n'
             '    mode: development\n'
             '  prod:\n'
             '    mode: production\n'
             '"""\n'
             'print(yaml)'),
        code('# Deploy do app (trial/CLI)\n'
             'print("""\n'
             'databricks bundle deploy -t dev\n'
             'databricks apps get --name app-vendas\n'
             '""")\n'
             'print("O app vira recurso do bundle — versionado e replicável.")'),
        pratica("CI/CD para apps",
            "GitHub Actions: no PR roda `bundle validate`; no merge, `bundle deploy -t "
            "prod` (mesmo padrão da Semana 6)."),
        code('# Observabilidade do app\n'
             'print("""\n'
             '1. Logs do app: Apps > app > Logs\n'
             '2. Métricas: requests, erros, latência (abas do app)\n'
             '3. Alerte: >5% de erros → notificar\n'
             '4. Scale-to-zero: app para sozinho após inatividade (Free: 24h)\n'
             '""")\n'
             'print("Monitorar apps = saber se o produto está no ar e saudável.")'),
        dica_prova("Apps/DABs: `resources.apps` no bundle + CI/CD — o deploy de apps é "
                   "código. Pergunta: 'como versionar o deploy de um app?' → DABs."),
        exercicios([
            "Adicione o app RAG ao bundle com target dev.",
            "Por que monitorar erros/latência do app?",
            "O que scale-to-zero significa para custo?",
        ]),
        gabarito([
            ("App no bundle",
             "Adicione `resources.apps.app_rag` apontando para a pasta do app e rode "
             "`bundle deploy`."),
            ("Monitorar",
             "Erros altos = usuário insatisfeito; latência alta = UX ruim — sem métricas "
             "você descobre pelo cliente."),
            ("Scale-to-zero",
             "Sem uso, o app desliga e para de custar — paga só quando tem tráfego."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana16_dia6_entregavel_2_apps",
    [
        header(
            "16", "6", "Entregável: 2 apps publicados e monitorados",
            "Fechar a Semana 16: app de BI + app de chat RAG publicados, com observabilidade "
            "e documentação.",
            "Portfólio", "2 apps no ar + README",
            "✅ Free Edition",
        ),
        teoria(
            "O que a Semana 16 entregou",
            "- Arquitetura de Apps (app.yaml, auth, scale)\n"
            "- App de BI (Streamlit + Ouro)\n"
            "- App de chat RAG (citações + feedback)\n"
            "- Backend FastAPI\n"
            "- CI/CD via DABs + observabilidade",
        ),
        pratica("Entregável final",
            "1. Publique o app de BI.\n"
            "2. Publique o app de chat RAG.\n"
            "3. Adicione ambos ao bundle.\n"
            "4. Documente no README (links, arquitetura)."),
        code('# Checklist dos apps\n'
             'print("""\n'
             '- [x] App BI publicado (KPIs + gráficos)\n'
             '- [x] App RAG publicado (chat + fontes + feedback)\n'
             '- [x] API FastAPI funcional\n'
             '- [x] Apps no DABs (dev/prod)\n'
             '- [x] Logs e métricas conferidos\n'
             '- [x] Links no README\n'
             '""")\n'
             'print("Na Free: 3 apps no máximo — planeje os próximos (Semanas 17-18).")'),
        dica_prova("Portfólio: ter 2 apps no ar (BI + RAG) com README e arquitetura "
                   "documentada é prova concreta de habilidade — vale mais que certificado "
                   "sozinho."),
        exercicios([
            "Compartilhe os links dos apps com alguém e peça feedback.",
            "Qual app você melhoraria com base no feedback?",
        ]),
        gabarito([
            ("Feedback",
             "Use os 👍/👎 e os comentários para priorizar a próxima versão."),
            ("Melhoria",
             "Ex.: adicionar filtro por país no RAG, mais KPIs no BI, ou streaming de "
             "resposta."),
        ]),
        footer([
            "Publiquei 2 apps (BI + RAG).",
            "Entendo app.yaml e o fluxo de deploy.",
            "Configurei CI/CD via DABs.",
            "Monitorei logs e métricas.",
        ]),
    ],
))
