"""Semana 15 — Agentes avançados, Agent Framework e Genie (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana15_dia1_reflexion_multi_agente",
    [
        header(
            "15", "1", "Arquiteturas: ReAct, Reflexion e Multi-agente",
            "Comparar as arquiteturas de agentes e construir Reflexion (auto-melhoria) e "
            "Multi-agente (coordenador + especialistas).",
            "GenAI Engineer Associate", "Multi-agente com coordenador rodando",
            "✅ Free Edition",
        ),
        teoria(
            "As 3 arquiteturas",
            "| Arquitetura | Ideia | Quando |\n|---|---|---|\n"
            "| **ReAct** | raciocina → age → observa | tarefas com tools |\n"
            "| **Reflexion** | gera → **avalia** → corrige | qualidade crítica (código, SQL) |\n"
            "| **Multi-agente** | coordenador delega a especialistas | tarefas compostas |\n\n"
            "Reflexion = ReAct + feedback: o agente critica a própria resposta e refaz até "
            "passar nos critérios.",
        ),
        pratica("Reflexion (gera → avalia → corrige)",
            "Implemente o loop de auto-melhoria."),
        code('# Reflexion para SQL: gera, valida, corrige até 3x\n'
             'def reflexion_sql(pergunta, max_rounds=3):\n'
             '    criticas = ""\n'
             '    for ronda in range(max_rounds):\n'
             '        prompt = (dicionario + "\\nPergunta: " + pergunta\n'
             '                  + "\\nCríticas anteriores: " + criticas\n'
             '                  + "\\nGere o SQL:")\n'
             '        sql_gerado = llm.invoke(prompt).content.strip().strip("```")\n'
             '        try:\n'
             '            valida_sql(sql_gerado)\n'
             '            df = spark.sql(sql_gerado)\n'
             '            return sql_gerado, df.toPandas()\n'
             '        except Exception as e:\n'
             '            criticas += f"\\n- Falhou ({e}). Corrija o SQL."\n'
             '            print(f"Ronda {ronda+1}: corrigindo ({e})")\n'
             '    return None, "Não consegui gerar SQL válido."\n'
             'print("Reflexion implementado (gera → crítica → corrige).")'),
        pratica("Multi-agente",
            "Coordenador delega para agentes especialistas."),
        code('# Especialistas (cada um com sua tool)\n'
             'from langgraph.graph import StateGraph, END\n'
             'from typing import TypedDict\n'
             'class Estado(TypedDict):\n'
             '    pergunta: str\n'
             '    resposta: str\n'
             '    especialista: str\n'
             '\n'
             'def coordenador(estado):\n'
             '    p = estado["pergunta"].lower()\n'
             '    if "receita" in p or "venda" in p:\n'
             '        estado["especialista"] = "vendas"\n'
             '    elif "produto" in p or "estoque" in p:\n'
             '        estado["especialista"] = "produtos"\n'
             '    else:\n'
             '        estado["especialista"] = "geral"\n'
             '    return estado\n'
             '\n'
             'def agente_vendas(estado):\n'
             '    estado["resposta"] = agente_final.invoke({"input": estado["pergunta"]})["output"]\n'
             '    return estado\n'
             '\n'
             'def agente_produtos(estado):\n'
             '    estado["resposta"] = top_produtos(3)\n'
             '    return estado\n'
             '\n'
             'def agente_geral(estado):\n'
             '    estado["resposta"] = "Assistente geral: " + estado["pergunta"]\n'
             '    return estado\n'
             'print("Especialistas definidos.")'),
        code('# Grafo multi-agente\n'
             'g = StateGraph(Estado)\n'
             'g.add_node("coordenador", coordenador)\n'
             'g.add_node("vendas", agente_vendas)\n'
             'g.add_node("produtos", agente_produtos)\n'
             'g.add_node("geral", agente_geral)\n'
             'g.set_entry_point("coordenador")\n'
             'g.add_conditional_edges("coordenador",\n'
             '    lambda e: e["especialista"])\n'
             'for n in ["vendas", "produtos", "geral"]:\n'
             '    g.add_edge(n, END)\n'
             'multi = g.compile()\n'
             'print(multi.invoke({"pergunta": "Qual a receita de novembro?"})["resposta"][:100])'),
        dica_prova("Agentes: Reflexion = avaliar e corrigir; Multi-agente = delegar. "
                   "Pergunta: 'como melhorar a precisão de um agente de SQL?' → Reflexion "
                   "com crítica."),
        exercicios([
            "Adicione um especialista 'graficos' ao multi-agente.",
            "O que o Reflexion adiciona ao ReAct?",
            "Quando NÃO usar multi-agente?",
        ]),
        gabarito([
            ("Especialista",
             "Crie nó que gera código de gráfico (matplotlib) e rota no coordenador."),
            ("Reflexion",
             "Um passo de avaliação/crítica entre geração e entrega — qualidade sobre "
             "velocidade."),
            ("Sem multi-agente",
             "Tarefas simples: multi-agente adiciona latência e complexidade — use um "
             "agente único."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana15_dia2_mosaic_ai_agent_framework",
    [
        header(
            "15", "2", "Mosaic AI Agent Framework e Agent Bricks",
            "Conhecer o padrão oficial de agentes do Databricks: Agent Bricks (avaliação, "
            "guardrails, tracing) e o fluxo de deploy.",
            "GenAI Engineer Associate", "Agente avaliado com Agent Bricks",
            "✅ Free Edition (partes) + 🔑 (partes)",
            dais="Agent Bricks 2.0 + Omnigent (DAIS 2026).",
        ),
        teoria(
            "Mosaic AI Agent Framework",
            "O **Mosaic AI Agent Framework** é o conjunto oficial para construir, avaliar e "
            "deployar agentes:\n\n"
            "- **Agent Bricks**: biblioteca de avaliação (RAG/agent metrics), guardrails e "
            "tracing padronizados\n"
            "- **Agent Evaluation**: avaliação automatizada com golden sets\n"
            "- **Deploy**: serve o agente como endpoint (serving) com o `databricks-agents` SDK",
        ),
        teoria(
            "Agent Bricks (2026)",
            "O **Agent Bricks** é o 'framework de frameworks': avaliação (mlflow.evaluate "
            "com databricks-agent), guardrails prontos e review de qualidade — o padrão "
            "que empresas pedem. A DAIS 2026 anunciou o **Omnigent** (orquestração de "
            "múltiplos agentes) como evolução.",
        ),
        pratica("Avaliação com Agent Bricks",
            "Use o SDK de agentes para empacotar e avaliar."),
        code('# Empacotar o agente como código (estrutura padrão)\n'
             'print("""\n'
             'config.yaml (agent):\n'
             '  name: agente_vendas\n'
             '  model:\n'
             '    name: databricks-llama-3-1-70b\n'
             '  tools:\n'
             '    - unity_catalog_function: workspace.prata.receita_periodo\n'
             '    - unity_catalog_function: workspace.prata.top_pais\n'
             '  evaluation:\n'
             '    golden_set: workspace.prata.golden_set_agente\n'
             '""")\n'
             'print("config.yaml declara modelo, tools e avaliação — o padrão Agent Bricks.")'),
        code('# Registrar o agente (MLflow) e avaliar\n'
             'import mlflow\n'
             'with mlflow.start_run(run_name="agente_bricks_v1"):\n'
             '    # Em produção: mlflow.langchain.log_model + mlflow.evaluate\n'
             '    mlflow.log_param("framework", "agent_bricks")\n'
             '    mlflow.log_param("guardrails", "offensive, pii")\n'
             '    print("Agente registrado para avaliação (Agent Bricks).")'),
        pratica("Deploy (trial)",
            "No trial: **Agent Evaluation → Review → Deploy** — o agente vira endpoint "
            "servido com tracing e guardrails habilitados."),
        code('# Deploy do agente (🔑 trial)\n'
             'print("""\n'
             '1. Agent Evaluation: rode o golden set (nota do agente)\n'
             '2. Review: veja falhas por categoria (alucinação, tool errada)\n'
             '3. Deploy: cria serving endpoint do agente (REST)\n'
             '4. O endpoint aceita mensagens e retorna resposta + traces\n'
             '""")\n'
             'print("Na Free, avalie com mlflow.evaluate; o deploy gerenciado é 🔑.")'),
        dica_prova("GenAI Assoc: Agent Bricks = avaliação + guardrails + deploy "
                   "padronizados. Pergunta: 'qual o padrão oficial de agentes no "
                   "Databricks?' → Mosaic AI Agent Framework / Agent Bricks."),
        exercicios([
            "Por que o config.yaml (declarativo) é melhor que agente no notebook?",
            "O que a revisão do Agent Evaluation mostra?",
            "O que é o Omnigent (DAIS 2026)?",
        ]),
        gabarito([
            ("Declarativo",
             "Versionável, reutilizável e deployável em ambientes — igual DABs para "
             "pipelines."),
            ("Revisão",
             "As respostas classificadas por categoria de erro (alucinação, tool errada, "
             "off-topic) para priorizar correções."),
            ("Omnigent",
             "Orquestração de múltiplos agentes (DAIS 2026) — a camada que coordena "
             "agentes especialistas em produção."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana15_dia3_genie_ontology",
    [
        header(
            "15", "3", "Genie + Genie Ontology: métricas que nunca erram",
            "Usar o Genie e a Ontologia (DAIS 2026) para dar ao agente a definição "
            "oficial de métricas — o fim das contas erradas.",
            "GenAI Engineer Associate, DAA", "Ontologia com métricas definidas",
            "🔑 Versão paga (Genie Ontology) — conceito na Free",
            dais="Genie Ontology (DAIS 2026): camada semântica de métricas.",
        ),
        teoria(
            "O problema das contas erradas",
            "Assistentes de dados erram quando **inventam a fórmula** (ARPU = receita/"
            "clientes? receita/notas?). A **Genie Ontology** (DAIS 2026) resolve: você "
            "define as métricas e cálculos **uma vez** — o Genie/agente usam a definição "
            "oficial, sempre.\n\n"
            "Na prática: uma camada semântica com métricas, dimensões e regras de "
            "negócio — o assistente consulta a ontologia antes de calcular.",
        ),
        pratica("Ontologia conceitual",
            "Modele as métricas oficiais do projeto (mesmo conceito da ontologia)."),
        code('# Definição canônica das métricas (a "ontologia" do projeto)\n'
             'ontologia = {\n'
             '    "receita_total": "SUM(Quantity * UnitPrice) filtrado por Quantity > 0",\n'
             '    "ticket_medio": "receita_total / COUNT(DISTINCT InvoiceNo)",\n'
             '    "arpu": "receita_total / COUNT(DISTINCT CustomerID)",\n'
             '    "n_vendas": "COUNT(*)",\n'
             '}\n'
             'print("Métricas canônicas definidas — todo agente usa estas fórmulas.")'),
        code('# Prompt do agente com a ontologia embutida\n'
             'ontologia_prompt = """\n'
             'Métricas OFICIAIS (use SEMPRE estas definições):\n'
             '- receita_total = SUM(Quantity * UnitPrice) com Quantity > 0\n'
             '- ticket_medio = receita_total / COUNT(DISTINCT InvoiceNo)\n'
             '- arpu = receita_total / COUNT(DISTINCT CustomerID)\n'
             'Nunca invente outra fórmula para essas métricas.\n'
             '"""\n'
             'print(ontologia_prompt)'),
        pratica("Genie com Ontologia (trial)",
            "No trial: **AI/BI → Genie → space → Ontology** — crie as métricas na UI e o "
            "Genie passa a usá-las nas respostas."),
        code('# Fluxo da ontologia no Genie (🔑)\n'
             'print("""\n'
             '1. Genie space > Ontology\n'
             '2. Defina: receita_total, ticket_medio, arpu (nome + SQL)\n'
             '3. Associe dimensões (país, mês)\n'
             '4. Pergunte no Genie: "qual o ARPU?" -> usa a definição oficial\n'
             '5. O mesmo vale para o agente (via Genie Agents)\n'
             '""")\n'
             'print("Ontologia = a fonte única de verdade das métricas.")'),
        dica_prova("DAA/GenAI 2026: Ontologia é o antídoto para contas erradas — o "
                   "assistente usa a definição canônica. Pergunta: 'como garantir que o "
                   "Genie não erre cálculo?' → Ontologia."),
        exercicios([
            "Defina 3 métricas oficiais do seu projeto com SQL.",
            "Por que a ontologia é melhor que instruções no prompt?",
            "O que acontece sem ontologia quando a fórmula é ambígua?",
        ]),
        gabarito([
            ("3 métricas",
             "Ex.: receita_total, ticket_medio, taxa_devolucao = devoluções / total."),
            ("Ontologia vs prompt",
             "Ontologia é estruturada, versionada e reutilizável (Genie + agente + BI); "
             "prompt é frágil e repetido."),
            ("Sem ontologia",
             "Cada pergunta pode gerar fórmula diferente — números divergentes entre "
             "assistente, BI e relatório."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana15_dia4_deploy_agente_mcp_integracao",
    [
        header(
            "15", "4", "Deploy do agente: UI, API e MCP",
            "Servir o agente (UI Streamlit, API, Slack/Teams) e integrar com MCP (Model "
            "Context Protocol).",
            "GenAI Engineer Associate", "Agente servido via endpoint + MCP",
            "✅ Free Edition (partes) + 🔑 (serving)",
        ),
        teoria(
            "Canais de entrega de agentes",
            "- **UI**: Streamlit/Databricks App (Semana 16) — chat amigável\n"
            "- **API**: Model Serving endpoint — integração com qualquer sistema\n"
            "- **Mensageria**: Slack/Teams\n"
            "- **MCP (Model Context Protocol)**: padrão aberto (Anthropic, 2024) para "
            "expor ferramentas/dados a qualquer LLM — o 'USB-C' dos agentes",
        ),
        pratica("Servindo o agente via API",
            "O agente LangChain vira endpoint (🔑 trial) e é chamado via REST."),
        code('# Chamar agente servido via REST (padrão de produção)\n'
             'print("""\n'
             'POST /serving-endpoints/agente_vendas/invocations\n'
             '{\n'
             '  "messages": [{"role": "user", "content": "Qual a receita do UK?"}],\n'
             '  "databricks_options": {"return_traces": true}\n'
             '}\n'
             '-> resposta + traces (para auditoria)\n'
             '""")\n'
             'print("Qualquer app chama o agente como API — sem acoplar ao notebook.")'),
        pratica("MCP",
            "Conecte o agente a ferramentas MCP (ex.: calendário, CRM) — o padrão 2026."),
        code('# MCP (conceito — servidor expõe ferramentas)\n'
             'print("""\n'
             '1. Um servidor MCP expõe ferramentas (JSON-RPC):\n'
             '   - tools/list, tools/call\n'
             '2. O agente Databricks adiciona o servidor MCP como fonte de tools\n'
             '3. Ex.: MCP do CRM -> o agente consulta clientes reais\n'
             '""")\n'
             'print("MCP = ferramentas padronizadas, interoperáveis entre LLMs.")'),
        pratica("UI rápida (Streamlit)",
            "Faça um chat simples que chama o agente."),
        code('# Chat Streamlit (roda no Databricks Apps, Semana 16)\n'
             'import streamlit as st\n'
             'st.title("Agente de Vendas")\n'
             'pergunta = st.chat_input("Pergunte sobre vendas...")\n'
             'if pergunta:\n'
             '    st.write(agente_final.invoke({"input": pergunta})["output"])\n'
             'print("Código do app Streamlit pronto (publicar na Semana 16).")'),
        dica_prova("Agentes/MCP: MCP padroniza ferramentas entre LLMs (protocolo aberto). "
                   "Pergunta: 'como integrar um agente a sistemas externos?' → MCP ou "
                   "API do serving endpoint."),
        exercicios([
            "Liste 3 ferramentas MCP úteis para um agente de vendas.",
            "O que `return_traces` faz na chamada do agente?",
            "Qual a diferença entre servir via endpoint e rodar no notebook?",
        ]),
        gabarito([
            ("MCP tools",
             "CRM (clientes), calendário (eventos), pagamentos (transações) — integrações "
             "prontas via protocolo."),
            ("return_traces",
             "Retorna os traces da chamada — auditoria e debug da resposta."),
            ("Endpoint vs notebook",
             "Endpoint: REST, escala, governança, monitoramento; notebook: manual, sem "
             "escala, não é produção."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana15_dia5_seguranca_agentes_sandbox",
    [
        header(
            "15", "5", "Segurança empresarial: sandbox, PII e guardrails avançados",
            "Proteger o agente em produção: sandbox de execução isolado, proteção de PII, "
            "guardrails avançados e auditoria total.",
            "GenAI Engineer Associate", "Política de segurança do agente",
            "✅ Free Edition (conceito) + 🔑 (avançado)",
        ),
        teoria(
            "As camadas de segurança de um agente",
            "1. **Entrada**: guardrails (tópicos, prompt injection)\n"
            "2. **Ferramentas**: permissões UC + SELECT only\n"
            "3. **Execução**: **sandbox Python isolado** — código gerado roda sem acessar "
            "o resto do workspace\n"
            "4. **Saída**: PII masking, filtro de conteúdo\n"
            "5. **Auditoria**: tudo logado",
        ),
        pratica("Sandbox e permissões",
            "Código do agente (UDF/ferramentas) roda isolado — conceito e prática na Free."),
        code('# Ferramentas com escopo mínimo (princípio do menor privilégio)\n'
             '# A tool SÓ lê a tabela Ouro — nunca acessa o workspace inteiro\n'
             'def tool_segura(pais: str) -> str:\n'
             '    """Consulta receita de um país (somente leitura)."""\n'
             '    return spark.sql(f"SELECT receita_total FROM workspace.ouro.receita_por_pais WHERE UPPER(Country) = UPPER(\'{pais}\')").collect()[0][0]\n'
             'print("Tool com escopo mínimo: só leitura do Ouro.")'),
        code('# Guardrails avançados (entrada + saída)\n'
             'def guardrail_avancado(pergunta, resposta):\n'
             '    # Entrada: bloqueia prompt injection\n'
             '    sinais = ["ignore previous", "ignore as instruções", "reveal your prompt"]\n'
             '    if any(s in pergunta.lower() for s in sinais):\n'
             '        return False, "Bloqueado: possível prompt injection."\n'
             '    # Saída: bloqueia PII\n'
             '    if detecta_pii(resposta)["email"] or detecta_pii(resposta)["cpf"]:\n'
             '        return False, "Bloqueado: resposta com PII."\n'
             '    return True, resposta\n'
             'print("Guardrail duplo (entrada + saída) implementado.")'),
        pratica("Auditoria total",
            "Registre cada decisão do guardrail, cada tool chamada e cada resposta."),
        code('# Auditoria enriquecida\n'
             'def registrar_auditoria(pergunta, resposta, tools_usadas, ok, motivo=""):\n'
             '    spark.createDataFrame([(\n'
             '        "now", pergunta, resposta, str(tools_usadas), ok, motivo\n'
             '    )], ["ts", "pergunta", "resposta", "tools", "ok", "motivo"])\\\n'
             '        .withColumn("ts", current_timestamp())\\\n'
             '        .write.mode("append").saveAsTable("workspace.audit.log_agente_completo")\n'
             'print("Auditoria completa: workspace.audit.log_agente_completo")'),
        dica_prova("Segurança de agentes: sandbox (execução isolada), PII (saída), "
                   "guardrails (entrada/saída), menor privilégio (tools). Pergunta: 'como "
                   "isolar a execução de código do agente?' → sandbox."),
        exercicios([
            "O que o sandbox Python isola?",
            "Por que o guardrail de saída é obrigatório?",
            "Monte a política de segurança do agente (documento).",
        ]),
        gabarito([
            ("Sandbox",
             "Executa código (UDF/tools) num ambiente isolado sem acesso ao workspace/"
             "credenciais — evita exfiltração."),
            ("Saída obrigatória",
             "O LLM pode vazar PII vinda do contexto — filtrar a resposta é a última "
             "linha antes do usuário."),
            ("Política",
             "Documente: quem pode usar, quais tools, o que é bloqueado, retenção de "
             "logs, processo de incidente."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana15_dia6_entregavel_multi_agente_simulado",
    [
        header(
            "15", "6", "Entregável: multi-agente avaliado + simulado GenAI",
            "Fechar a fase de agentes: multi-agente com segurança e deploy, e simulado "
            "final GenAI (domínios 2026).",
            "GenAI Engineer Associate (simulado)", "Multi-agente + simulado ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "O que a Semana 15 entregou",
            "- Reflexion e Multi-agente (LangGraph)\n"
            "- Mosaic AI Agent Framework + Agent Bricks\n"
            "- Genie Ontology (métricas oficiais)\n"
            "- Deploy: endpoint + MCP + UI\n"
            "- Segurança: sandbox, PII, guardrails, auditoria",
        ),
        pratica("Simulado final GenAI (14 questões)",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** Reflexion adiciona ao ReAct:
- A) mais tools  B) avaliação/crítica e correção  C) GPU  D) cache

**2.** Multi-agente usa:
- A) um LLM gigante  B) coordenador + especialistas  C) só SQL  D) nada

**3.** Agent Bricks (2026) oferece:
- A) avaliação + guardrails + deploy  B) só UI  C) só SQL  D) cache

**4.** Para métricas sem erro de conta:
- A) prompt maior  B) Genie Ontology  C) fine-tuning  D) cache

**5.** MCP é:
- A) um modelo  B) protocolo de ferramentas  C) um banco  D) um job

**6.** Sandbox Python:
- A) executa código isolado  B) instala libs  C) acelera  D) nada

**7.** Guardrail de saída protege contra:
- A) prompts ruins  B) PII na resposta  C) custo  D) latência

**8.** Para auditar um agente:
- A) logar turnos em Delta  B) cache  C) DABs  D) nada

**9.** Tool correctness mede:
- A) se a tool certa foi chamada  B) velocidade  C) custo  D) tokens

**10.** O config.yaml do agente declara:
- A) modelo + tools + avaliação  B) só modelo  C) só nome  D) GPU

**11.** O endpoint do agente retorna:
- A) resposta + traces  B) só texto  C) SQL  D) nada

**12.** Omnigent (DAIS 2026):
- A) orquestra múltiplos agentes  B) novo LLM  C) banco  D) cache

**13.** Menor privilégio nas tools:
- A) tool só lê o necessário  B) tool com acesso total  C) sem tools  D) nada

**14.** Para servir o agente a um app:
- A) Model Serving endpoint  B) notebook  C) dbutils  D) nada
"""),
        teoria(
            "Gabarito",
            "**1-B** · **2-B** · **3-A** · **4-B** · **5-B** · **6-A** · **7-B** · "
            "**8-A** · **9-A** · **10-A** · **11-A** · **12-A** · **13-A** · **14-A**. "
            "≥ 10/14 = pronto para as aplicações (Semanas 16–18).",
        ),
        pratica("Entregável final da fase",
            "Integre tudo e documente."),
        code('# Checklist do agente empresarial\n'
             'print("""\n'
             '- [x] Multi-agente (coordenador + especialistas)\n'
             '- [x] Avaliação (golden set + traces)\n'
             '- [x] Ontologia de métricas\n'
             '- [x] Deploy: endpoint + UI + MCP (trial)\n'
             '- [x] Segurança: sandbox, PII, guardrails, auditoria\n'
             '""")\n'
             'print("Fase de agentes concluída — próximo: Databricks Apps (Semana 16).")'),
        dica_prova("Revisão agentes: ReAct (loop), Reflexion (crítica), Multi-agente "
                   "(delegação), Agent Bricks (padrão), Ontologia (métricas), MCP "
                   "(integração), sandbox (segurança). Sete palavras-chave da prova."),
        exercicios([
            "Documente a arquitetura do agente final no README (diagrama).",
            "Quais 5 termos de agentes você explicaria em inglês numa entrevista?",
        ]),
        gabarito([
            ("README",
             "Diagrama: entrada → guardrails → coordenador → especialistas (tools UC) → "
             "auditoria → resposta; com avaliação e deploy."),
            ("5 termos",
             "ReAct, tool calling, guardrails, MCP, sandbox — com exemplos do seu agente."),
        ]),
        footer([
            "Implementei Reflexion e multi-agente.",
            "Usei Agent Bricks para avaliação.",
            "Defini ontologia de métricas.",
            "Segurança e auditoria completas.",
        ]),
    ],
))
