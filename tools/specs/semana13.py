"""Semana 13 — GenAI em produção, AI Gateway e Fine-tuning (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana13_dia1_genai_producao_model_serving",
    [
        header(
            "13", "1", "GenAI em produção: os 7 pilares e Model Serving",
            "Entender o que leva IA de protótipo a produção e servir modelos via Mosaic AI "
            "Model Serving.",
            "GenAI Engineer Associate, MLP", "Endpoint de FMA consultado",
            "✅ Free Edition (FMA) + 🔑 custom (trial)",
        ),
        teoria(
            "Os 7 pilares de GenAI em produção",
            "1. **Qualidade mensurável** (avaliação contínua)\n"
            "2. **Custo controlado** (gateway, cache, modelo certo)\n"
            "3. **Latência aceitável** (endpoint, otimização de contexto)\n"
            "4. **Segurança e privacidade** (PII, guardrails, RLS)\n"
            "5. **Governança** (versões, auditoria, permissões)\n"
            "6. **Observabilidade** (traces, métricas, alertas)\n"
            "7. **Escala** (serving, auto-scaling, quota)",
        ),
        teoria(
            "Mosaic AI Model Serving",
            "O **Mosaic AI Model Serving** (2026; ex-Databricks Model Serving) serve: FMA "
            "(hospedados) e **modelos custom** (seus MLmodels/LangChain) via endpoint "
            "REST com auto-scaling.\n\n"
            "Na Free Edition: endpoints de FMA com quota; **sem GPU/provisioned "
            "throughput/custom** — custom é 🔑 trial.",
        ),
        pratica("Servindo FMA",
            "Crie um endpoint de FMA (ou use o já existente) e consulte via REST."),
        code('# Consultar endpoint de FMA via REST (o padrão de produção)\n'
             'import requests, json\n'
             'host = spark.conf.get("spark.databricks.workspaceUrl")\n'
             'token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()\n'
             'resp = requests.post(\n'
             '    f"https://{host}/serving-endpoints/databricks-llama-3-1-70b/invocations",\n'
             '    headers={"Authorization": f"Bearer {token}",\n'
             '             "Content-Type": "application/json"},\n'
             '    json={"messages": [{"role": "user", "content": "Resuma o Lakehouse em 1 frase."}],\n'
             '          "temperature": 0.2})\n'
             'print(resp.json()["choices"][0]["message"]["content"])'),
        code('# Endpoint custom (🔑 trial): modelo MLflow do projeto\n'
             'print("""\n'
             '1. Catalog > modelos > modelo_previsao_receita > Serve this model\n'
             '2. Escolha o compute (serverless)\n'
             '3. Endpoint gerado: /serving-endpoints/modelo_previsao_receita/invocations\n'
             '4. Envie features (dia_semana, mes...) e receba a predição\n'
             '""")\n'
             'print("Model Serving custom = 🔑 (trial ou conta corporativa).")'),
        dica_prova("GenAI Assoc: Model Serving serve FMA e custom via REST; provisioned "
                   "throughput e GPU são recursos pagos (na Free: sem). Pergunta: 'como "
                   "expor um modelo a um app?' → Model Serving endpoint."),
        exercicios([
            "Quais dos 7 pilares você já cobre no seu RAG?",
            "Qual a diferença entre FMA e endpoint custom?",
            "Por que endpoint é melhor que notebook para produção?",
        ]),
        gabarito([
            ("Pilares",
             "Qualidade (avaliação S12), observabilidade (tracing S12), custo (S13.2). "
             "Faltam: escala, segurança fina, governança total — próximos dias."),
            ("FMA vs custom",
             "FMA: modelos hospedados pela Databricks (pay-per-token). Custom: SEU modelo "
             "(MLflow) servido em endpoint."),
            ("Endpoint vs notebook",
             "Endpoint: REST, auto-scaling, SLA, governança de modelo; notebook não é "
             "produção (sessão manual, sem escala)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana13_dia2_unity_ai_gateway",
    [
        header(
            "13", "2", "Unity AI Gateway: roteamento, fallback e cache semântico",
            "Controlar custo e confiabilidade das chamadas de LLM com o Unity AI Gateway: "
            "roteamento, fallback, cache semântico e auditoria.",
            "GenAI Engineer Associate (Governance ~15%)",
            "Gateway configurado no projeto",
            "✅ Free Edition (conceito/FMA) + 🔑 avançado (trial)",
        ),
        teoria(
            "Unity AI Gateway (DAIS 2026)",
            "O **Unity AI Gateway** é a camada de controle entre sua aplicação e os LLMs:\n\n"
            "- **Roteamento**: enviar cada pergunta ao modelo mais barato/adequado\n"
            "- **Fallback**: se o modelo principal falhar, chama o reserva\n"
            "- **Cache semântico**: perguntas similares reutilizam resposta (economia "
            "até ~60% de custo)\n"
            "- **Auditoria**: todas as chamadas logadas (governança)",
        ),
        pratica("Padrão de gateway no código",
            "Implemente o padrão roteamento+fallback no cliente de LLM."),
        code('# Roteamento por tipo de tarefa (padrão gateway)\n'
             'from mlflow.deployments import get_deploy_client\n'
             'client = get_deploy_client("databricks")\n'
             '\n'
             'def chamar_llm(pergunta, tarefa="geral"):\n'
             '    # Roteamento: tarefas simples -> modelo pequeno/barato; complexas -> grande\n'
             '    endpoint = ("databricks-llama-3-1-8b" if tarefa == "simples"\n'
             '                else "databricks-llama-3-1-70b")\n'
             '    try:\n'
             '        resp = client.predict(endpoint=endpoint,\n'
             '                             inputs={"messages": [{"role": "user", "content": pergunta}],\n'
             '                                     "temperature": 0})\n'
             '        return resp["choices"][0]["message"]["content"], endpoint\n'
             '    except Exception as e:\n'
             '        # Fallback: tenta o modelo reserva\n'
             '        resp = client.predict(endpoint="databricks-llama-3-1-8b",\n'
             '                             inputs={"messages": [{"role": "user", "content": pergunta}]})\n'
             '        return resp["choices"][0]["message"]["content"], "fallback"\n'
             'print("Padrão roteamento + fallback implementado.")'),
        code('# Cache semântico (didático — cache por similaridade de embedding)\n'
             'from databricks.vector_search.client import VectorSearchClient\n'
             'cache = {}\n'
             'def com_cache(pergunta):\n'
             '    if pergunta in cache:\n'
             '        print("Cache HIT (resposta reutilizada)")\n'
             '        return cache[pergunta]\n'
             '    resp, ep = chamar_llm(pergunta)\n'
             '    cache[pergunta] = resp\n'
             '    print(f"Cache MISS (gerou com {ep})")\n'
             '    return resp\n'
             'print(com_cache("Qual a receita total?"))\n'
             'print(com_cache("Qual a receita total?"))  # 2a vez: cache'),
        pratica("Gateway gerenciado (trial)",
            "No trial: **AI → Unity AI Gateway → Create provider route** — configure "
            "roteamento/fallback entre modelos e ative cache semântico."),
        code('# Auditoria no gateway\n'
             'print("""\n'
             'Todas as chamadas passam a ter: modelo usado, custo, latência, usuário\n'
             '-> system tables / logs do gateway para auditoria (governança)\n'
             '""")\n'
             'print("Na Free, o padrão didático acima mostra o conceito; o gateway gerenciado é 🔑.")'),
        dica_prova("GenAI Assoc (Governance ~15%): gateway cobre roteamento, fallback, "
                   "cache semântico e auditoria. Pergunta: 'como reduzir custo de LLM?' → "
                   "cache semântico + roteamento para modelo barato."),
        exercicios([
            "Explique cache semântico em 2 frases.",
            "Quando o fallback é acionado?",
            "Por que auditoria de chamadas importa em empresas?",
        ]),
        gabarito([
            ("Cache semântico",
             "Guarda respostas por similaridade de pergunta — perguntas iguais/similares "
             "reutilizam a resposta em vez de chamar o LLM (economia de tokens)."),
            ("Fallback",
             "Quando o modelo principal falha (erro, quota, latência) — o gateway redireciona "
             "para um reserva e mantém o serviço no ar."),
            ("Auditoria",
             "Compliance e custo: saber quem chamou o quê, quanto custou e com qual modelo — "
             "obrigatório em empresas reguladas."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana13_dia3_fine_tuning_lora_qlora",
    [
        header(
            "13", "3", "Fine-tuning: quando vale (e quando NUNCA vale)",
            "Entender a regra de decisão RAG vs fine-tuning, e o fluxo de LoRA/QLoRA com "
            "dataset de treino e avaliação.",
            "GenAI Engineer Associate, MLP", "Regra de decisão + demo de fine-tune",
            "🔑 Versão paga (GPU) — conceito na Free",
        ),
        teoria(
            "A regra de decisão definitiva",
            "| Problema | Solução |\n|---|---|\n"
            "| Modelo não sabe SEUS dados | **RAG** (contexto) |\n"
            "| Modelo não segue formato/estilo/tom | **Fine-tuning** |\n"
            "| Perguntas repetitivas de domínio fechado | Fine-tuning (após RAG) |\n"
            "| Falta de dados/conhecimento novo | RAG primeiro, sempre |\n\n"
            "**Regra de ouro**: comece com RAG + prompts. Fine-tuning só quando o RAG já "
            "está bom e o problema é formato/comportamento. **Fine-tuning NUNCA substitui "
            "o acesso a dados dinâmicos.**",
        ),
        teoria(
            "LoRA e QLoRA",
            "**LoRA**: treina pequenas matrizes de adaptação (menos parâmetros, menos "
            "custo). **QLoRA**: quantiza o modelo base (4-bit) para caber em menos GPU. "
            "Ambos permitem fine-tuning de modelos grandes com GPU modesta.",
        ),
        pratica("Preparando o dataset de treino",
            "Formato chat: mensagens com system/user/assistant."),
        code('# Dataset de fine-tuning (formato chat)\n'
             'dados = [\n'
             '    {"messages": [\n'
             '        {"role": "system", "content": "Você responde sobre vendas."},\n'
             '        {"role": "user", "content": "Qual a receita total?"},\n'
             '        {"role": "assistant", "content": "A receita total é 9.7 milhões."}\n'
             '    ]},\n'
             '    {"messages": [\n'
             '        {"role": "system", "content": "Você responde sobre vendas."},\n'
             '        {"role": "user", "content": "Qual o top país?"},\n'
             '        {"role": "assistant", "content": "O top país é United Kingdom."}\n'
             '    ]}\n'
             ']\n'
             'print("Dataset no formato chat (messages) pronto.")'),
        code('# Fluxo de fine-tuning no Databricks (🔑 trial/GPU)\n'
             'print("""\n'
             '1. AI > Fine-tuning > Create\n'
             '2. Base: Llama 3.1 (via FMA)\n'
             '3. Dataset: tabela Delta com coluna messages\n'
             '4. Método: LoRA (recomendado) ou QLoRA\n'
             '5. Rode (GPU dedicada, 🔑)\n'
             '6. Resultado vira modelo servível via Model Serving\n'
             '7. Avalie: mesmo golden set do RAG — compare antes/depois\n'
             '""")\n'
             'print("Na Free, o fine-tuning real exige trial pago ou verificação LinkedIn (GPU limitada).")'),
        pratica("Avaliando o fine-tune",
            "Nunca fine-tune sem avaliar: rode o mesmo golden set no modelo base vs "
            "fine-tunado."),
        code('# Avaliação comparativa (base vs fine-tuned)\n'
             'print("""\n'
             '1. Chame o endpoint do modelo base e do fine-tunado\n'
             '2. Mesmas 20 perguntas do golden set\n'
             '3. Compare com mlflow.evaluate (faithfulness, answer relevance)\n'
             '4. Se não melhorou: não vale o custo — volte ao RAG/prompt\n'
             '""")\n'
             'print("Avaliação é o que decide: fine-tune só se os números melhorarem.")'),
        dica_prova("GenAI Assoc: 'quando usar RAG vs fine-tuning?' é pergunta garantida. "
                   "Resposta-padrão: RAG para conhecimento/dados; fine-tuning para formato/"
                   "estilo; comece com RAG."),
        exercicios([
            "Dê 2 exemplos em que fine-tuning é a escolha certa.",
            "Dê 2 exemplos em que fine-tuning NÃO resolve.",
            "Qual a vantagem do LoRA sobre fine-tune completo?",
        ]),
        gabarito([
            ("Certo",
             "1) modelo precisa responder sempre em formato JSON específico da empresa; "
             "2) tom/estilo de marca. (Conhecimento de dados → RAG.)"),
            ("Não resolve",
             "1) dados que mudam todo dia (preços); 2) conhecimento novo não visto no "
             "treino — RAG é a resposta."),
            ("LoRA",
             "Treina fração dos parâmetros: custo/latência de treino muito menores e GPU "
             "modesta — com qualidade próxima do full fine-tune."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana13_dia4_mlops_llm_versionamento",
    [
        header(
            "13", "4", "MLOps para LLMs: versionar prompts, dados e modelos",
            "Aplicar MLOps ao pipeline GenAI: versionar prompts/datasets/modelos e "
            "avaliação contínua.",
            "GenAI Engineer Associate", "Registros versionados no MLflow",
            "✅ Free Edition",
        ),
        teoria(
            "Versionar tudo",
            "Em GenAI, o 'modelo' inclui: o LLM base + **prompt** + **chunks/retriever** + "
            "dados de avaliação. Mudou o prompt? É uma nova versão.\n\n"
            "Boas práticas:\n"
            "- Prompt como **código** (Git) + registrado como artifact no MLflow\n"
            "- Golden set versionado (tabela Delta)\n"
            "- Modelo/prompt/avaliação no mesmo run → rastreabilidade completa",
        ),
        pratica("Versionando o prompt",
            "Registre o prompt do RAG como artifact de uma run."),
        code('# Prompt versionado no MLflow\n'
             'import mlflow\n'
             'with mlflow.start_run(run_name="prompt_v3"):\n'
             '    mlflow.log_text(system_prompt, "system_prompt_v3.txt")\n'
             '    mlflow.log_param("versao_prompt", "v3")\n'
             '    mlflow.log_param("chunk_size", 400)\n'
             '    mlflow.log_param("retriever", "hibrido_rrf")\n'
             '    print("Prompt e configuração versionados na run.")'),
        code('# Golden set versionado como tabela\n'
             'import pandas as pd\n'
             'golden = spark.createDataFrame(pd.DataFrame({\n'
             '    "id": [1, 2, 3],\n'
             '    "pergunta": ["P1", "P2", "P3"],\n'
             '    "resposta_esperada": ["R1", "R2", "R3"],\n'
             '    "versao": ["v3"]\n'
             '}))\n'
             'golden.write.mode("overwrite").saveAsTable("workspace.prata.golden_set")\n'
             'print("Golden set versionado: workspace.prata.golden_set")'),
        pratica("Avaliação contínua",
            "Agende a avaliação do RAG: job diário roda golden set e registra métricas no "
            "MLflow — queda de métrica dispara alerta."),
        code('# Job de avaliação contínua (conceito)\n'
             'print("""\n'
             '1. Notebook de avaliação (Semana 12.1) vira job diário\n'
             '2. Lê o golden set da tabela\n'
             '3. Roda o RAG e mlflow.evaluate\n'
             '4. Compara com o baseline registrado\n'
             '5. Alerta se faithfulness caiu > 5%\n'
             '""")\n'
             'print("Monitoramento contínuo = GenAI em produção de verdade.")'),
        dica_prova("GenAI Assoc: 'o que versionar num sistema GenAI?' → modelo, prompt, "
                   "dados de avaliação, retriever. Pergunta: 'como rastrear uma regressão "
                   "de qualidade?' → compare runs/versões no MLflow."),
        exercicios([
            "Registre 2 versões de prompt e compare as métricas.",
            "Por que o golden set deve ser versionado?",
            "O que um alerta de queda de faithfulness indicaria?",
        ]),
        gabarito([
            ("2 versões",
             "Rode a avaliação com prompt v2 e v3; compare faithfulness/relevance nas runs."),
            ("Golden set versionado",
             "Sem versionamento, mudanças no dataset invalidam comparações entre versões."),
            ("Queda de faithfulness",
             "O RAG está alucinando mais — provável mudança no retriever/prompt; investigue "
             "com tracing."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana13_dia5_monitoramento_rag_custo_seguranca",
    [
        header(
            "13", "5", "Monitoramento contínuo de RAG: qualidade, custo e segurança",
            "Monitorar RAG em produção em 4 frentes: qualidade, operacional, custo e "
            "segurança — com alertas.",
            "GenAI Engineer Associate", "Monitor de RAG com 4 frentes",
            "✅ Free Edition",
        ),
        teoria(
            "As 4 frentes de monitoramento",
            "| Frente | Métricas | Ferramenta |\n|---|---|---|\n"
            "| **Qualidade** | faithfulness, relevance, recall | mlflow.evaluate agendado |\n"
            "| **Operacional** | latência, erros, taxa de sucesso | endpoint logs |\n"
            "| **Custo** | tokens, $ por pergunta, cache hit | gateway/billing |\n"
            "| **Segurança** | PII na resposta, prompts maliciosos | guardrails/logs |",
        ),
        pratica("Qualidade contínua",
            "Monte o notebook de avaliação agendada."),
        code('# Avaliação agendada (job diário)\n'
             'import mlflow\n'
             'golden = spark.table("workspace.prata.golden_set").toPandas()\n'
             'respostas = []\n'
             'for q in golden["pergunta"]:\n'
             '    respostas.append(rag.invoke({"input": q})["answer"])\n'
             'golden["response"] = respostas\n'
             'with mlflow.start_run(run_name="avaliacao_diaria"):\n'
             '    mlflow.evaluate(\n'
             '        data=golden[["pergunta", "response"]],\n'
             '        targets=golden["resposta_esperada"],\n'
             '        model_type="databricks-agent",\n'
             '        extra_metrics=[mlflow.metrics.genai.faithfulness(),\n'
             '                       mlflow.metrics.genai.answer_relevance()])\n'
             'print("Avaliação diária registrada (agende como job).")'),
        pratica("Custo por pergunta",
            "Estime o custo por chamada (tokens de entrada/saída)."),
        code('# Estimativa de custo por pergunta\n'
             'def estimar_custo(tokens_in, tokens_out, preco_in=3e-6, preco_out=12e-6):\n'
             '    return round(tokens_in * preco_in + tokens_out * preco_out, 4)\n'
             'print("Custo estimado por pergunta (ex.): $",\n'
             '      estimar_custo(1200, 150))\n'
             'print("Meta: custo < $0.01/pergunta com cache + modelo barato.")'),
        pratica("Segurança",
            "Verifique PII nas respostas e registre prompts sensíveis."),
        code('# Checagem simples de PII na resposta\n'
             'import re\n'
             'def detecta_pii(texto):\n'
             '    email = re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.]+", texto)\n'
             '    cpf = re.findall(r"\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}", texto)\n'
             '    return {"email": email, "cpf": cpf}\n'
             'print(detecta_pii("Contato: ana@empresa.com · CPF 123.456.789-00"))\n'
             'print("Se o RAG vazar PII, aplique masking/guardrails (Semana 15).")'),
        dica_prova("GenAI Assoc (Evaluation & Monitoring ~20%): monitorar 4 frentes é o "
                   "padrão. Pergunta: 'quais métricas monitorar num RAG?' → qualidade, "
                   "custo, latência, segurança."),
        exercicios([
            "Monte um painel com as 4 frentes (queries SQL).",
            "O que um aumento de custo por pergunta indica?",
            "Como detectar vazamento de PII automaticamente?",
        ]),
        gabarito([
            ("Painel",
             "4 queries: métricas do mlflow (qualidade), latência do endpoint (operacional), "
             "tokens/$ (custo), logs com regex PII (segurança)."),
            ("Custo subiu",
             "Contexto maior (chunks), modelo caro, cache miss — revise chunking/roteamento."),
            ("PII",
             "Regex + modelo classificador na resposta; alerta e masking automático (Semana 15)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana13_dia6_entregavel_rag_producao_simulado",
    [
        header(
            "13", "6", "Entregável: RAG em produção + simulado GenAI",
            "Fechar a fase GenAI com o RAG monitorado e um simulado parcial da prova "
            "GenAI Associate.",
            "GenAI Engineer Associate (simulado)", "RAG em produção + simulado ≥ 70%",
            "✅ Free Edition",
        ),
        teoria(
            "O que a Semana 13 entregou",
            "- 7 pilares de GenAI em produção\n"
            "- Model Serving (FMA + custom 🔑)\n"
            "- Unity AI Gateway (roteamento/fallback/cache/auditoria)\n"
            "- Fine-tuning: regra de decisão + LoRA/QLoRA\n"
            "- MLOps para LLMs (versionar tudo)\n"
            "- Monitoramento 4 frentes",
        ),
        pratica("Simulado GenAI parcial (12 questões)",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** Para responder sobre dados que mudam todo dia:
- A) fine-tuning  B) RAG  C) re-treinar  D) cache

**2.** Para o modelo sempre responder em JSON da empresa:
- A) RAG  B) fine-tuning  C) nada  D) cache

**3.** Model Serving serve:
- A) só FMA  B) FMA e custom  C) só GPU  D) notebooks

**4.** Na Free Edition, Model Serving:
- A) completo  B) sem GPU/provisioned/custom  C) ilimitado  D) não existe

**5.** Cache semântico do gateway:
- A) cacheia disk  B) reutiliza respostas similares  C) cacheia SQL  D) nada

**6.** Fallback do gateway:
- A) apaga o modelo  B) usa modelo reserva em falha  C) reduz tokens  D) nada

**7.** LoRA:
- A) treina tudo  B) adaptadores pequenos  C) novo modelo  D) cache

**8.** QLoRA:
- A) quantiza o base (4-bit)  B) dobra o tamanho  C) só texto  D) GPU maior

**9.** Para rastrear regressão de qualidade do RAG:
- A) versionar prompt/dataset/modelo + avaliar  B) cache  C) DABs  D) nada

**10.** Monitoramento de RAG NÃO inclui:
- A) qualidade  B) custo  C) cor da UI  D) segurança

**11.** O que mais reduz custo de LLM?
- A) modelo maior  B) cache semântico + roteamento  C) mais contexto  D) GPU

**12.** Provisioned throughput é:
- A) recurso pago  B) gratuito  C) cache  D) sem uso
"""),
        teoria(
            "Gabarito",
            "**1-B** · **2-B** · **3-B** · **4-B** · **5-B** · **6-B** · **7-B** · "
            "**8-A** · **9-A** · **10-C** · **11-B** · **12-A**. ≥ 9/12 = pronto "
            "para agentes (Semanas 14–15).",
        ),
        pratica("Entregável final da fase",
            "Rode o RAG com todas as peças e documente."),
        code('# Checklist do RAG em produção\n'
             'print("""\n'
             '- [x] Avaliação (4 métricas de ouro)\n'
             '- [x] Tracing habilitado\n'
             '- [x] Busca híbrida + RRF\n'
             '- [x] Gateway (roteamento/fallback/cache)\n'
             '- [x] Prompt e golden set versionados\n'
             '- [x] Monitoramento 4 frentes (job diário)\n'
             '""")\n'
             'print("Fase GenAI concluída — próximo: Agentes (Semana 14).")'),
        dica_prova("Revisão GenAI: RAG = conhecimento; fine-tune = formato; gateway = "
                   "custo/confiabilidade; monitoramento = 4 frentes. Esse é o vocabulário "
                   "da prova e das entrevistas."),
        exercicios([
            "Documente a arquitetura GenAI final no README (diagrama + decisões).",
            "Liste os 5 conceitos GenAI que você explicaria numa entrevista em inglês.",
        ]),
        gabarito([
            ("README",
             "Diagrama: dados → chunks → Vector Search (híbrido) → prompt → FMA/gateway → "
             "resposta → avaliação/monitoramento."),
            ("5 conceitos",
             "RAG, FMA, embeddings/chunking, LLM-as-judge, AI Gateway — com exemplos do "
             "projeto."),
        ]),
        footer([
            "Entendo os 7 pilares e o Model Serving.",
            "Configurei roteamento/fallback/cache no padrão gateway.",
            "Sei a regra de decisão RAG vs fine-tuning.",
            "Fiz o simulado GenAI e revisei erros.",
        ]),
    ],
))
