"""Semana 18 — Apps full-stack (React/Next.js) + MCP (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana18_dia1_react_nextjs_apps",
    [
        header(
            "18", "1", "Frontend React/Next.js nos Databricks Apps",
            "Entender como rodar um frontend moderno (Next.js/React) como Databricks App "
            "— o padrão para produtos de dados profissionais.",
            "Portfólio (full-stack)", "App Next.js inicial publicado",
            "✅ Free Edition (até 3 apps)",
        ),
        teoria(
            "Full-stack nos Apps",
            "Os Databricks Apps suportam **qualquer stack**: além de Streamlit, você pode "
            "rodar **Next.js/React** (frontend) + **FastAPI** (backend) — o padrão "
            "moderno de produto de dados.\n\n"
            "Estrutura:\n"
            "```\napp/\n ├── app.yaml          # comando: next start (ou uvicorn)\n ├── frontend/         # Next.js (React)\n ├── backend/          # FastAPI\n └── requirements.txt / package.json\n```",
        ),
        pratica("App Next.js mínimo",
            "Estrutura de um app React que chama a API."),
        code('# frontend/app/page.tsx (conceito Next.js)\n'
             'tsx = """\n'
             '\'use client\';\n'
             'import { useEffect, useState } from \'react\';\n'
             '\n'
             'export default function Home() {\n'
             '  const [resposta, setResposta] = useState("");\n'
             '  useEffect(() => {\n'
             '    fetch("/api/health")\n'
             '      .then(r => r.json())\n'
             '      .then(d => setResposta(d.status));\n'
             '  }, []);\n'
             '  return <h1>App de Vendas — API: {resposta}</h1>;\n'
             '}\n'
             '"""\n'
             'print(tsx)\n'
             'print("Componente React que consulta o backend.")'),
        code('# app.yaml (Next.js)\n'
             'yaml = """\n'
             'command:\n'
             '  - next\n'
             '  - start\n'
             '  - -p\n'
             '  - "8080"\n'
             '"""\n'
             'print(yaml)'),
        pratica("Publicando",
            "1. Suba a pasta com package.json + app.yaml.\n"
            "2. **Apps → Create App**.\n"
            "3. O build (npm install + next build) roda na plataforma.",
        ),
        dica_prova("Apps full-stack: o Databricks builda e roda Next.js/FastAPI — sem "
                   "Docker/K8s. Pergunta: 'que stacks os Apps suportam?' → Python e "
                   "Node.js (Streamlit, Flask, FastAPI, Next.js...)."),
        exercicios([
            "Por que usar Next.js em vez de Streamlit?",
            "O que o app.yaml muda para um app Node?",
            "Publique o app Next.js mínimo.",
        ]),
        gabarito([
            ("Next.js vs Streamlit",
             "Next.js: controle total de UI/UX, componentes, SEO; Streamlit: BI rápido "
             "sem frontend."),
            ("app.yaml Node",
             "O comando vira `next start` (ou `npm run start`) com a porta 8080."),
            ("Publicar",
             "Pasta + app.yaml + Create App → o build gerencia npm."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana18_dia2_fullstack_next_fastapi_lakehouse",
    [
        header(
            "18", "2", "Full-stack: Next.js ↔ FastAPI ↔ Lakehouse",
            "Integrar a arquitetura completa: frontend React → backend FastAPI → Lakehouse "
            "(dados) e agente.",
            "Portfólio (full-stack)", "App full-stack com dados reais",
            "✅ Free Edition",
        ),
        teoria(
            "A arquitetura de 3 camadas",
            "```\nNext.js (UI) → FastAPI (backend) → Lakehouse (dados) / Agente\n```\n\n"
            "O frontend nunca fala com o Spark diretamente — passa pelo backend, que "
            "centraliza segurança e regras.",
        ),
        pratica("Backend que consulta o Ouro",
            "API com endpoints de dados."),
        code('# backend/main.py — endpoints de dados\n'
             'from fastapi import FastAPI\n'
             'from pyspark.sql import SparkSession\n'
             'spark = SparkSession.builder.getOrCreate()\n'
             'app = FastAPI()\n'
             '\n'
             '@app.get("/api/kpis")\n'
             'def kpis():\n'
             '    df = spark.table("workspace.ouro.vendas_por_dia").toPandas()\n'
             '    return {"receita_total": float(df["receita_total"].sum()),\n'
             '            "dias": len(df)}\n'
             '\n'
             '@app.get("/api/top_produtos")\n'
             'def top_produtos():\n'
             '    return spark.table("workspace.ouro.top_produtos").limit(10).toPandas().to_dict("records")\n'
             'print("Backend com /api/kpis e /api/top_produtos.")'),
        code('# Frontend consome os endpoints\n'
             'tsx = """\n'
             'const [kpis, setKpis] = useState(null);\n'
             'useEffect(() => {\n'
             '  fetch("/api/kpis").then(r => r.json()).then(setKpis);\n'
             '}, []);\n'
             'return <div>{kpis && `Receita total: ${kpis.receita_total}`}</div>;\n'
             '"""\n'
             'print(tsx)'),
        pratica("Proxy e rotas",
            "No app.yaml, o frontend Next.js usa rotas de API (rewrite) para o backend — "
            "ou o backend roda na mesma porta via proxy."),
        dica_prova("Full-stack: frontend → backend → lakehouse é o padrão; nunca expor "
                   "Spark direto no frontend. Pergunta: 'onde ficam as regras de "
                   "negócio?' → backend/API."),
        exercicios([
            "Adicione um endpoint /api/receita_por_pais.",
            "Por que o frontend não chama o Spark?",
            "Como autenticar as chamadas frontend→backend?",
        ]),
        gabarito([
            ("Endpoint",
             "Leia `workspace.ouro.receita_por_pais` e retorne records."),
            ("Não chama Spark",
             "Segurança (credenciais), controle de regras e acoplamento — o backend "
             "centraliza."),
            ("Auth",
             "Os Apps usam a auth do workspace por padrão; o backend valida o usuário e "
             "aplica permissões do UC."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana18_dia3_agente_ui_streaming",
    [
        header(
            "18", "3", "Agente com UI profissional: streaming e estados",
            "Construir a UI do agente: streaming de resposta, estados de carregamento e "
            "feedback — a experiência de produto.",
            "GenAI Assoc (deploy), portfólio", "Chat com streaming publicado",
            "✅ Free Edition",
        ),
        teoria(
            "UX de chat de agente",
            "Um chat de agente profissional tem:\n"
            "- **Streaming**: a resposta aparece token a token (percepção de velocidade)\n"
            "- **Estados**: 'pensando', 'consultando dados', 'respondendo'\n"
            "- **Ferramentas visíveis**: 'usou a tool X' (transparência)\n"
            "- **Feedback**: 👍/👎 gravado",
        ),
        pratica("Backend com streaming",
            "O endpoint do agente retorna resposta em streaming (SSE)."),
        code('# Backend: streaming do agente\n'
             'from fastapi import FastAPI\n'
             'from fastapi.responses import StreamingResponse\n'
             'app = FastAPI()\n'
             '\n'
             '@app.post("/api/agente/stream")\n'
             'def agente_stream(p: dict):\n'
             '    def gerar():\n'
             '        resposta = agente_final.invoke({"input": p["pergunta"]})["output"]\n'
             '        for i in range(0, len(resposta), 20):\n'
             '            yield resposta[i:i+20]\n'
             '    return StreamingResponse(gerar(), media_type="text/plain")\n'
             'print("Endpoint com streaming (SSE) pronto.")'),
        code('# Frontend: streaming + estados\n'
             'tsx = """\n'
             'const [resposta, setResposta] = useState("");\n'
             'const [estado, setEstado] = useState("idle"); // idle|pensando|respondendo\n'
             '\n'
             'async function perguntar(texto) {\n'
             '  setEstado("pensando"); setResposta("");\n'
             '  const r = await fetch("/api/agente/stream", {method: "POST",\n'
             '    body: JSON.stringify({pergunta: texto})});\n'
             '  const reader = r.body.getReader();\n'
             '  setEstado("respondendo");\n'
             '  while (true) {\n'
             '    const {done, value} = await reader.read();\n'
             '    if (done) break;\n'
             '    setResposta(prev => prev + new TextDecoder().decode(value));\n'
             '  }\n'
             '  setEstado("idle");\n'
             '}\n'
             '"""\n'
             'print(tsx)'),
        pratica("Feedback integrado",
            "Gravando 👍/👎 no backend (tabela audit.feedback_agente)."),
        dica_prova("Produto de agente: streaming + estados + transparência de tools + "
                   "feedback — é isso que separa demo de produto. Pergunta: 'como "
                   "melhorar a percepção de velocidade?' → streaming."),
        exercicios([
            "Adicione o indicador 'usando tool X' na UI.",
            "Por que streaming melhora a UX?",
            "Publique o chat com streaming.",
        ]),
        gabarito([
            ("Tool visível",
             "O backend emite eventos de tool (SSE) e a UI mostra o nome."),
            ("Streaming",
             "Percepção de velocidade + feedback parcial — usuário não fica olhando "
             "tela parada."),
            ("Publicar",
             "App com backend (SSE) + frontend (reader) — teste com 3 perguntas."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana18_dia4_mcp_servidores_ferramentas",
    [
        header(
            "18", "4", "MCP: servidores e ferramentas no agente",
            "Conectar o agente a servidores MCP (Model Context Protocol) — o padrão "
            "aberto de integração de ferramentas (2026).",
            "GenAI Assoc", "Servidor MCP conectado ao agente",
            "✅ Free Edition (conceito) + 🔑 (trial)",
        ),
        teoria(
            "MCP na prática",
            "O **MCP** (Model Context Protocol, aberto em 2024) padroniza como LLMs "
            "acessam ferramentas e dados: um servidor MCP expõe **tools** via JSON-RPC, e "
            "qualquer cliente MCP (incluindo agentes Databricks) as consome.\n\n"
            "Em 2026 é o padrão de integração: CRM, calendário, bancos, APIs internas — "
            "tudo vira tool MCP.",
        ),
        pratica("Servidor MCP mínimo",
            "Estrutura de um servidor MCP que expõe tools."),
        code('# servidor_mcp.py (conceito — usa a lib mcp)\n'
             'print("""\n'
             'from mcp.server.fastmcp import FastMCP\n'
             'mcp = FastMCP("vendas")\n'
             '\n'
             '@mcp.tool()\n'
             'def receita_por_pais(pais: str) -> str:\n'
             '    """Receita de um país (Ouro)."""\n'
             '    ...\n'
             '\n'
             'mcp.run()\n'
             '""")\n'
             'print("Servidor MCP expõe receita_por_pais como tool.")'),
        code('# Conectar o agente ao servidor MCP\n'
             'print("""\n'
             '1. Rode o servidor MCP (URL/SSE)\n'
             '2. No Databricks: AI > Agents > Add MCP server\n'
             '3. O agente lista as tools do servidor e as chama\n'
             '4. Ex.: MCP do CRM -> agente consulta clientes reais\n'
             '""")\n'
             'print("MCP = ferramentas interoperáveis entre qualquer LLM.")'),
        pratica("MCP no seu projeto",
            "Exponha as ferramentas do agente de vendas como servidor MCP — elas ficam "
            "reutilizáveis por outros agentes/apps."),
        code('# Ferramentas do agente via MCP\n'
             'print("""\n'
             'MCP tools do projeto:\n'
             '- receita_por_pais(pais)\n'
             '- top_produtos(n)\n'
             '- vendas_por_periodo(de, ate)\n'
             '- estado_sessao(sessao_id)  -> via Lakebase\n'
             '""")\n'
             'print("O agente ganha interoperabilidade — qualquer LLM pode usá-las.")'),
        dica_prova("MCP: protocolo aberto (JSON-RPC) para tools — 'USB-C dos agentes'. "
                   "Pergunta: 'como integrar um agente a sistemas externos em 2026?' → "
                   "servidores MCP."),
        exercicios([
            "Quais tools do seu agente virariam MCP?",
            "Por que MCP é melhor que integração custom?",
            "Conecte 1 servidor MCP ao seu agente (trial).",
        ]),
        gabarito([
            ("Tools MCP",
             "Todas as de consulta (receita, top produtos, vendas por período) + estado "
             "de sessão via Lakebase."),
            ("MCP vs custom",
             "Padrão aberto: qualquer LLM/cliente usa; sem código de integração por "
             "sistema."),
            ("Conectar",
             "AI > Agents > Add MCP server → URL do servidor → tools disponíveis."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana18_dia5_seguranca_testes_observabilidade_apps",
    [
        header(
            "18", "5", "Segurança, testes e observabilidade de apps",
            "Endurecer o app: RBAC, testes, rate limiting e observabilidade completa "
            "(logs, métricas, alertas).",
            "Portfólio", "App testado e monitorado",
            "✅ Free Edition",
        ),
        teoria(
            "Segurança de apps em produção",
            "- **RBAC**: o app respeita as permissões do UC (usuário vê só o que pode)\n"
            "- **Rate limiting**: protege contra abuso de API\n"
            "- **Secrets**: credenciais via secret scope (nunca no código)\n"
            "- **Input validation**: sanitizar entradas (SQL injection no Text-to-SQL!)",
        ),
        pratica("Rate limit e validação",
            "Proteja a API."),
        code('# Rate limit simples no FastAPI\n'
             'from fastapi import FastAPI, HTTPException\n'
             'import time\n'
             'app = FastAPI()\n'
             'ultima_chamada = {}\n'
             '\n'
             '@app.post("/api/perguntar")\n'
             'def perguntar(p: dict):\n'
             '    agora = time.time()\n'
             '    if agora - ultima_chamada.get("user", 0) < 2:\n'
             '        raise HTTPException(429, "Muitas requisições — aguarde 2s")\n'
             '    ultima_chamada["user"] = agora\n'
             '    if len(p.get("pergunta", "")) > 500:\n'
             '        raise HTTPException(400, "Pergunta muito longa")\n'
             '    return {"ok": True}\n'
             'print("Rate limit (2s) + validação de tamanho implementados.")'),
        code('# Testes do app (pytest)\n'
             'print("""\n'
             'def test_health():\n'
             '    r = client.get("/health")\n'
             '    assert r.status_code == 200\n'
             '\n'
             'def test_pergunta_longa():\n'
             '    r = client.post("/api/perguntar", json={"pergunta": "x"*600})\n'
             '    assert r.status_code == 400\n'
             '""")\n'
             'print("Testes básicos do app (rodam no CI).")'),
        pratica("Observabilidade",
            "Logs estruturados + métricas + alertas no app."),
        code('# Logs estruturados\n'
             'import logging\n'
             'logging.basicConfig(level=logging.INFO)\n'
             'logger = logging.getLogger("app")\n'
             'logger.info("pergunta_recebida", extra={"usuario": "ana", "tamanho": 120})\n'
             'print("Logs estruturados para o App Logs / Datadog.")'),
        dica_prova("Segurança de apps: RBAC (UC), rate limit, validação de entrada "
                   "(injection), secrets. Pergunta: 'como proteger uma API de dados?' → "
                   "essas 4 camadas."),
        exercicios([
            "Adicione validação contra SQL injection no endpoint do Text-to-SQL.",
            "Por que o RBAC do UC vale também para apps?",
            "Monte os alertas do app (erros > 5%, latência > 5s).",
        ]),
        gabarito([
            ("Injection",
             "Nunca aceite SQL do usuário direto — o agente gera, o validador (SELECT "
             "only) filtra e o RLS limita."),
            ("RBAC",
             "O app roda com a identidade do usuário — ele só vê o que a permissão do UC "
             "permite."),
            ("Alertas",
             "App Logs + métricas → alerta em erro/latência — mesmo padrão dos pipelines."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana18_dia6_entregavel_app_fullstack_agente",
    [
        header(
            "18", "6", "Entregável: app full-stack com agente",
            "Publicar o app full-stack final (Next.js ↔ FastAPI ↔ agente ↔ Lakebase) "
            "com segurança e observabilidade.",
            "Portfólio", "App full-stack publicado e monitorado",
            "✅ Free Edition (até 3 apps)",
        ),
        teoria(
            "A arquitetura final da Semana 18",
            "```\nNext.js (UI + streaming)\n   → FastAPI (backend + rate limit + validação)\n      → Agente (tools UC + MCP)\n      → Lakehouse (Ouro) / Lakebase (sessões)\n```",
        ),
        pratica("Entregável final",
            "1. Rode o app full-stack (frontend + backend).\n"
            "2. Teste: KPIs, chat com streaming, feedback.\n"
            "3. Confira logs e métricas.\n"
            "4. Documente a arquitetura no README."),
        code('# Checklist do app full-stack\n'
             'print("""\n'
             '- [x] Next.js publicado (UI + streaming)\n'
             '- [x] FastAPI publicado (endpoints + rate limit)\n'
             '- [x] Agente integrado (tools + MCP)\n'
             '- [x] Sessões no Lakebase\n'
             '- [x] RBAC do UC respeitado\n'
             '- [x] Logs/métricas/alertas\n'
             '""")\n'
             'print("Fase de apps concluída — próximo: Projeto Final (Semana 19).")'),
        dica_prova("Portfólio: um app full-stack com agente + Lakebase + segurança "
                   "documentada é o entregável mais forte do curso — mostre o diagrama "
                   "na entrevista."),
        exercicios([
            "Escreva o README do app (arquitetura, decisões, links).",
            "Prepare um demo de 5 minutos do app para entrevista.",
        ]),
        gabarito([
            ("README",
             "Diagrama 3 camadas + decisões (por que Next.js, FastAPI, Lakebase) + "
             "limitações Free."),
            ("Demo",
             "Pergunta de vendas → streaming → fonte/tool → feedback — o ciclo completo "
             "em 5 min."),
        ]),
        footer([
            "Publiquei app full-stack com agente.",
            "Streaming + estados + feedback implementados.",
            "Conectei MCP.",
            "Segurança e observabilidade completas.",
        ]),
    ],
))
