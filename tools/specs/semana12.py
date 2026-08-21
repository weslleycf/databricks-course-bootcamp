"""Semana 12 — RAG avançado, avaliação e LangGraph (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana12_dia1_avaliacao_rag_mlflow_evaluate",
    [
        header(
            "12", "1", "Avaliação de RAG com mlflow.evaluate (LLM-as-judge)",
            "Medir a qualidade do RAG com as 4 métricas de ouro: faithfulness, answer "
            "relevance, context precision e context recall.",
            "GenAI Engineer Associate (Evaluation ~20%)", "Métricas ≥ alvo do RAG",
            "✅ Free Edition",
        ),
        teoria(
            "As 4 métricas de ouro do RAG",
            "| Métrica | Mede | Significado |\n|---|---|---|\n"
            "| **Faithfulness** | resposta segue o contexto? | 1 = sem alucinação |\n"
            "| **Answer relevance** | resposta responde a pergunta? | 1 = relevante |\n"
            "| **Context precision** | chunks relevantes vêm primeiro? | ordem do retrieval |\n"
            "| **Context recall** | o contexto tinha tudo que precisava? | cobertura |\n\n"
            "**LLM-as-judge**: um LLM avalia as respostas do seu RAG (usando FMA) — "
            "escalável e barato. O `mlflow.evaluate` automatiza tudo.",
        ),
        pratica("Preparando o dataset de avaliação",
            "Crie um dataset com perguntas e respostas esperadas (golden set)."),
        code('# Golden set (perguntas + resposta de referência)\n'
             'import pandas as pd\n'
             'eval_df = pd.DataFrame({\n'
             '    "question": [\n'
             '        "Quais produtos são de vidro?",\n'
             '        "Qual o produto mais vendido?",\n'
             '        "Existe item para cozinha?"\n'
             '    ],\n'
             '    "answer": [\n'
             '        "Não informado ainda.",\n'
             '        "Preciso consultar os dados.",\n'
             '        "Há itens de cozinha no catálogo."\n'
             '    ]\n'
             '})\n'
             'print(eval_df)'),
        code('# Gerar respostas do RAG para o dataset\n'
             'respostas = []\n'
             'for q in eval_df["question"]:\n'
             '    r = rag.invoke({"input": q})\n'
             '    respostas.append(r["answer"])\n'
             'eval_df["response"] = respostas\n'
             'eval_df["retrieved_context"] = eval_df["question"].apply(\n'
             '    lambda q: [d.page_content for d in rag.invoke({"input": q})["context"]])\n'
             'print(eval_df[["question", "response"]])'),
        pratica("Rodando a avaliação",
            "Avalie com mlflow.evaluate usando LLM-as-judge."),
        code('# Avaliação com métricas de RAG\n'
             'import mlflow\n'
             'with mlflow.start_run(run_name="avaliacao_rag_v1"):\n'
             '    resultado = mlflow.evaluate(\n'
             '        data=eval_df[["question", "response", "retrieved_context"]],\n'
             '        targets=eval_df["answer"],\n'
             '        model_type="databricks-agent",\n'
             '        extra_metrics=[mlflow.metrics.genai.faithfulness(),\n'
             '                       mlflow.metrics.genai.answer_relevance(),\n'
             '                       mlflow.metrics.genai.context_precision(),\n'
             '                       mlflow.metrics.genai.context_recall()])\n'
             '    print("Métricas:", {k: round(v, 3) for k, v in resultado.metrics.items() if isinstance(v, float)})'),
        code('# Interpretar\n'
             'print("""\n'
             'Alvo: faithfulness >= 0.9 (pouca alucinação)\n'
             '      answer relevance >= 0.8\n'
             '      context recall/precision >= 0.8\n'
             'Se algo caiu, revise chunking, prompt ou rerank (Semana 12.3).\n'
             '""")\n'
             'print("Cada métrica tem feedback do juiz na run do MLflow.")'),
        dica_prova("GenAI Assoc (Evaluation & Monitoring ~20%): as 4 métricas de ouro e o "
                   "LLM-as-judge são perguntas garantidas. Memorize o que cada uma mede."),
        exercicios([
            "O que indica faithfulness baixa?",
            "Crie mais 5 perguntas no golden set e reavalie.",
            "Por que usar um golden set (respostas de referência)?",
        ]),
        gabarito([
            ("Faithfulness baixa",
             "O modelo está alucinando — resposta fora do contexto. Mitigue com prompt "
             "mais restritivo e melhor retrieval."),
            ("Golden set",
             "Quanto maior o golden set, mais confiável a métrica (20–50 perguntas é um "
             "bom começo)."),
            ("Referência",
             "Permite medir answer relevance/recall contra o esperado — sem ele, só "
             "medimos consistência."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana12_dia2_mlflow_tracing_debug",
    [
        header(
            "12", "2", "MLflow Tracing: debugar o pipeline RAG",
            "Usar o MLflow Tracing (spans) para ver passo a passo o que o RAG fez — "
            "retrieval, prompt final, tokens e latência.",
            "GenAI Engineer Associate", "Trace analisado com spans",
            "✅ Free Edition",
        ),
        teoria(
            "O que é tracing",
            "O **MLflow Tracing** registra **spans** (etapas) de uma chamada: retrieval, "
            "montagem do prompt, chamada do LLM, resposta. Permite **debugar** onde o RAG "
            "errou (contexto ruim? prompt errado? LLM?).",
        ),
        pratica("Habilitando tracing",
            "Ative o tracing para LangChain e FMA."),
        code('# Habilitar tracing\n'
             'import mlflow\n'
             'mlflow.langchain.autolog()\n'
             'print("Tracing do LangChain habilitado.")'),
        code('# Executar e gerar trace\n'
             'resp = rag.invoke({"input": "Quais produtos de vidro para bebidas?"})\n'
             'print("Resposta:", resp["answer"][:200])'),
        pratica("Analisando o trace",
            "1. **Experiments → run mais recente → Traces**.\n"
            "2. Veja os spans: retriever (chunks + scores), prompt final, LLM (tokens).\n"
            "3. Identifique: o contexto recuperado era relevante? O prompt estava certo?",
        ),
        code('# Ver traces via API\n'
             'traces = mlflow.search_traces(experiment_names=[mlflow.get_experiment().name])\n'
             'for t in traces:\n'
             '    print("Trace:", t.info.trace_id)\n'
             '    for span in t.data.spans:\n'
             '        print(f"  span: {span.name} | inputs: {str(span.inputs)[:80]}")'),
        dica_prova("GenAI Assoc: tracing (spans) é a ferramenta de debug padrão — "
                   "'onde o RAG falhou?' → veja os spans. `mlflow.langchain.autolog()` "
                   "captura automaticamente."),
        exercicios([
            "Rode 3 perguntas e inspecione os spans de cada uma.",
            "O que um span de retriever mostra?",
            "Como o tracing ajuda a achar alucinação?",
        ]),
        gabarito([
            ("Spans",
             "Chunks recuperados, scores de similaridade, colunas retornadas — dá para ver "
             "se o contexto era relevante."),
            ("Retriever span",
             "A consulta de busca, os chunks e os scores."),
            ("Alucinação",
             "Se a resposta cita algo que não está nos spans de contexto → o LLM inventou; "
             "aperte o prompt."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana12_dia3_busca_hibrida_reranking",
    [
        header(
            "12", "3", "Busca híbrida (BM25 + semântica) com RRF e reranking",
            "Melhorar o retrieval combinando busca lexical e semântica (híbrida) com RRF e "
            "reranking cross-encoder.",
            "GenAI Engineer Associate", "Recall@5 melhorado com híbrido + rerank",
            "✅ Free Edition (conceito) + 🔑 rerank (trial)",
        ),
        teoria(
            "Por que híbrido?",
            "A busca semântica erra nomes próprios/códigos (ex.: '85123A'); a busca "
            "lexical (BM25) erra sinônimos. A **busca híbrida** combina as duas e funde "
            "com **RRF (Reciprocal Rank Fusion)**:\n\n"
            "```\nscore RRF = Σ 1/(k + posição_do_item)\n```\n\n"
            "O **reranking** reordena os top-N com um cross-encoder (modelo que compara "
            "pergunta×chunk de uma vez) — qualidade bem melhor, custo de latência.",
        ),
        pratica("Busca híbrida",
            "Combine resultados do Vector Search com BM25."),
        code('# BM25 (lexical) — usando a própria tabela como fonte de texto\n'
             'from pyspark.sql.functions import col, lower\n'
             'from pyspark.ml.feature import Tokenizer\n'
             'df = spark.table("workspace.prata.produtos_rag")\n'
             'df_lex = df.withColumn("texto_lower", lower(col("texto")))\n'
             'print("Base lexical pronta (busca por palavras exatas).")'),
        code('# Busca semântica (vector)\n'
             'from databricks.vector_search.client import VectorSearchClient\n'
             'vsc = VectorSearchClient()\n'
             'sem = vsc.similarity_search(index_name="workspace.prata.produtos_rag_index",\n'
             '                            query_text="copo de vidro",\n'
             '                            columns=["StockCode"], num_results=10)\n'
             'print("Semântica:", [r[0] for r in sem["result"]["data_array"]])'),
        code('# Fusão RRF (implementação didática)\n'
             'def rrf(*listas, k=60):\n'
             '    scores = {}\n'
             '    for lst in listas:\n'
             '        for pos, item in enumerate(lst, start=1):\n'
             '            scores[item] = scores.get(item, 0) + 1 / (k + pos)\n'
             '    return sorted(scores, key=scores.get, reverse=True)\n'
             'sem_lista = [r[0] for r in sem["result"]["data_array"]]\n'
             'lex_lista = ["85123A", "71053", "22423"]  # resultados BM25 (exemplo)\n'
             'print("Fusão RRF:", rrf(sem_lista, lex_lista)[:5])'),
        pratica("Reranking",
            "Na Free Edition, o rerank via cross-encoder é conceitual (🔑 no trial). "
            "O padrão: endpoint de rerank do Databricks recebe pergunta + chunks e "
            "retorna scores."),
        code('# Rerank (conceito; 🔑 no trial)\n'
             'print("""\n'
             '1. Endpoint de rerank (Mosaic AI Reranker, 🔑)\n'
             '2. Entrada: query + lista de chunks (top-10)\n'
             '3. Saída: mesma lista reordenada por relevância\n'
             '4. Use os top-3 reordenados como contexto final\n'
             '""")\n'
             'print("Rerank melhora Recall@5 em ~10-25% — teste no trial.")'),
        dica_prova("GenAI Assoc: RRF (fórmula 1/(k+rank)), híbrido = lexical + semântico, "
                   "rerank = cross-encoder no top-N. Pergunta: 'como combinar BM25 e "
                   "vetores?' → RRF."),
        exercicios([
            "Explique a fórmula do RRF com um exemplo de 2 listas.",
            "Quando o BM25 vence a busca semântica?",
            "Por que rerank só no top-N e não em tudo?",
        ]),
        gabarito([
            ("RRF",
             "Se um item está em posição 1 nas duas listas: 1/61 + 1/61 = 0.033 — itens "
             "bem rankeados nas duas vencem."),
            ("BM25 vence",
             "Códigos, IDs, nomes exatos e siglas — onde o 'som' importa mais que o "
             "significado."),
            ("Top-N",
             "Cross-encoder é caro (compara par a par); aplicá-lo em 10–20 candidatos "
             "dá o ganho com latência aceitável."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana12_dia4_rag_multimodal_chunking_avancado",
    [
        header(
            "12", "4", "RAG multimodal (PDF/Excel/Word) e chunking avançado",
            "Processar documentos empresariais (PDF, Excel, Word) e aplicar chunking "
            "hierárquico/semântico com metadata.",
            "GenAI Engineer Associate (Data Prep)", "Pipeline de documentos funcionando",
            "✅ Free Edition (parcial)",
        ),
        teoria(
            "Documentos empresariais no RAG",
            "PDFs, planilhas e Docs são o caso mais comum de RAG. O fluxo:\n\n"
            "1. **Parse**: extrair texto/tabelas (pypdf, python-docx, openpyxl)\n"
            "2. **Chunking**: dividir preservando estrutura (por seção/tabela)\n"
            "3. **Metadata**: título, página, data — para filtro e citação\n"
            "4. **Embed + indexar**: igual ao pipeline de texto",
        ),
        teoria(
            "Chunking hierárquico e semântico",
            "- **Hierárquico**: chunks pequenos com referência ao documento/contexto pai — "
            "melhor para documentos longos\n"
            "- **Semântico**: junta frases até quebrar por similaridade — chunks "
            "'coesos' por assunto",
        ),
        pratica("Parse de PDF (exemplo)",
            "Extraia texto de um PDF e crie chunks com metadata."),
        code('# Parse de PDF (instale pypdf se necessário)\n'
             'try:\n'
             '    from pypdf import PdfReader\n'
             '    leitor = PdfReader("/Volumes/workspace/prata/vol_modelos/exemplo.pdf")\n'
             '    paginas = [p.extract_text() for p in leitor.pages]\n'
             '    print("Páginas extraídas:", len(paginas))\n'
             'except Exception as e:\n'
             '    print("Coloque um PDF no volume primeiro. Dica:", str(e)[:80])'),
        code('# Chunking por página + metadata\n'
             'chunks = []\n'
             'for i, txt in enumerate(paginas[:10] if "paginas" in dir() else []):\n'
             '    if txt:\n'
             '        chunks.append({"id": i, "pagina": i+1, "texto": txt[:800],\n'
             '                       "fonte": "exemplo.pdf"})\n'
             'print("Chunks:", len(chunks))\n'
             'for c in chunks[:2]:\n'
             '    print(c["pagina"], "|", c["texto"][:80])'),
        pratica("Pipeline de documentos no projeto",
            "Crie um volume para documentos e o pipeline de ingestão (parse → chunk → "
            "embed → índice)."),
        code('# Estrutura do pipeline de documentos\n'
             'print("""\n'
             '1. Volume: /Volumes/workspace/prata/vol_documentos/\n'
             '2. Job diário: parse (pypdf/docx/openpyxl)\n'
             '3. Chunking com metadata (fonte, página)\n'
             '4. Embed + DELTA_SYNC no Vector Search\n'
             '5. O RAG filtra por fonte/página na resposta (citação)\n'
             '""")\n'
             'print("Documentos viram cidadãos de primeira classe no RAG.")'),
        dica_prova("GenAI Assoc (Data Prep ~20%): parse → chunk → metadata → embed é o "
                   "fluxo. Pergunta: 'como garantir citação de fonte?' → metadata de "
                   "chunk + prompt exigindo a fonte."),
        exercicios([
            "Por que metadata importa no RAG de documentos?",
            "O que o chunking hierárquico resolve?",
            "Processe um arquivo .docx e gere 5 chunks.",
        ]),
        gabarito([
            ("Metadata",
             "Permite filtro (por data/autoria), citação (fonte+página) e debugging — "
             "sem metadata o RAG é uma caixa preta."),
            ("Hierárquico",
             "Chunks pequenos mantêm contexto do documento pai — evita chunk sem contexto "
             "em docs longos."),
            ("Docx",
             "`from docx import Document; doc = Document(path)` → iterar parágrafos e "
             "gerar chunks por seção."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana12_dia5_langchain_langgraph_primeiro_grafo",
    [
        header(
            "12", "5", "LangChain → LangGraph: primeiro grafo com estado",
            "Evoluir de chains lineares para grafos com estado (nodes/edges) — a base "
            "dos agentes da Semana 14.",
            "GenAI Engineer Associate", "Primeiro fluxo LangGraph funcionando",
            "✅ Free Edition",
        ),
        teoria(
            "Chain vs Graph",
            "Uma **chain** é uma sequência fixa (retrieve → generate). Um **grafo "
            "(LangGraph)** tem **nós** (funções), **arestas** (transições) e **estado** "
            "(memória entre nós) — e pode **decidir** o próximo passo:\n\n"
            "```\ninício → nó_1 (rota) → nó_A ou nó_B → fim\n```",
        ),
        teoria(
            "Componentes do LangGraph",
            "- **State**: dict tipado que flui entre nós\n"
            "- **Node**: função que recebe estado e retorna updates\n"
            "- **Edge**: ligação entre nós; `conditional_edge` decide o caminho\n"
            "- **Graph**: compila e executa (`graph.invoke`)",
        ),
        pratica("Primeiro grafo",
            "Crie um grafo com rota condicional (pergunta de vendas vs geral)."),
        code('# Dependências\n'
             'from langgraph.graph import StateGraph, END\n'
             'from typing import TypedDict\n'
             '\n'
             'class Estado(TypedDict):\n'
             '    pergunta: str\n'
             '    resposta: str'),
        code('# Nós\n'
             'def rotear(estado):\n'
             '    p = estado["pergunta"].lower()\n'
             '    if any(k in p for k in ["venda", "receita", "produto", "país"]):\n'
             '        return {"destino": "vendas"}\n'
             '    return {"destino": "geral"}\n'
             '\n'
             'def responder_vendas(estado):\n'
             '    return {"resposta": "[RAG de vendas] " + estado["pergunta"]}\n'
             '\n'
             'def responder_geral(estado):\n'
             '    return {"resposta": "[Assistente geral] " + estado["pergunta"]}\n'
             '\n'
             'print("Nós definidos: rotear, responder_vendas, responder_geral")'),
        code('# Montar o grafo com aresta condicional\n'
             'g = StateGraph(Estado)\n'
             'g.add_node("rotear", rotear)\n'
             'g.add_node("vendas", responder_vendas)\n'
             'g.add_node("geral", responder_geral)\n'
             'g.set_entry_point("rotear")\n'
             'g.add_conditional_edges("rotear",\n'
             '    lambda e: "vendas" if e.get("destino") == "vendas" else "geral")\n'
             'g.add_edge("vendas", END)\n'
             'g.add_edge("geral", END)\n'
             'app = g.compile()\n'
             'print("Grafo compilado.")'),
        code('# Executar\n'
             'r1 = app.invoke({"pergunta": "Qual a receita de novembro?"})\n'
             'r2 = app.invoke({"pergunta": "Oi, tudo bem?"})\n'
             'print("1:", r1["resposta"])\n'
             'print("2:", r2["resposta"])'),
        pratica("Conectando o RAG como nó",
            "Troque `responder_vendas` pela chain RAG da Semana 11 — o agente de dados "
            "começa a nascer."),
        code('# Nó de vendas usando o RAG\n'
             'def responder_vendas_rag(estado):\n'
             '    r = rag.invoke({"input": estado["pergunta"]})\n'
             '    return {"resposta": r["answer"]}\n'
             'print("Substitua responder_vendas por esta função no grafo.")'),
        dica_prova("GenAI Assoc/agentes: nodes + edges + state + conditional_edge são o "
                   "vocabulário do LangGraph. Pergunta: 'como fazer o agente escolher a "
                   "ferramenta?' → conditional edge / tool calling."),
        exercicios([
            "Adicione um terceiro nó de rota (ex.: 'estoque').",
            "Qual a diferença entre edge normal e conditional_edge?",
            "O que o estado carrega entre os nós?",
        ]),
        gabarito([
            ("Terceiro nó",
             "Adicione `estoque` ao rotear e uma aresta condicional para ele."),
            ("Edges",
             "Normal: sempre segue. Conditional: função decide qual nó vem — base do "
             "raciocínio de agentes."),
            ("Estado",
             "Tudo que os nós precisam compartilhar: pergunta, contexto, histórico, "
             "resposta parcial — definido no TypedDict."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana12_dia6_entregavel_rag_avaliado",
    [
        header(
            "12", "6", "Entregável: RAG avaliado e documentado",
            "Fechar a Semana 12: RAG com avaliação quantificada, busca híbrida e "
            "documentação do pipeline.",
            "GenAI Engineer Associate", "RAG avaliado + gráfico de evolução",
            "✅ Free Edition",
        ),
        teoria(
            "O que a Semana 12 entregou",
            "- Avaliação LLM-as-judge (4 métricas de ouro)\n"
            "- Tracing (spans) para debug\n"
            "- Busca híbrida com RRF + reranking\n"
            "- RAG multimodal com metadata\n"
            "- LangGraph: grafos com estado (base dos agentes)",
        ),
        pratica("Entregável integrado",
            "Rode o fluxo completo e registre os resultados."),
        code('# 1) Avaliação final do RAG\n'
             'import mlflow\n'
             'with mlflow.start_run(run_name="avaliacao_rag_final"):\n'
             '    resultado = mlflow.evaluate(\n'
             '        data=eval_df[["question", "response", "retrieved_context"]],\n'
             '        targets=eval_df["answer"],\n'
             '        model_type="databricks-agent",\n'
             '        extra_metrics=[mlflow.metrics.genai.faithfulness(),\n'
             '                       mlflow.metrics.genai.answer_relevance(),\n'
             '                       mlflow.metrics.genai.context_precision(),\n'
             '                       mlflow.metrics.genai.context_recall()])\n'
             '    print("RAG final avaliado.")'),
        code('# 2) Evolução das métricas (registre no README)\n'
             'print("""\n'
             'Versão v1 (Semana 11): baseline\n'
             'Versão v2 (híbrido+rerank): context recall/precision melhorou\n'
             'Versão v3 (prompt + metadata): faithfulness subiu\n'
             'Documente os números de cada versão — é o seu portfólio GenAI.\n'
             '""")\n'
             'print("Gráfico de evolução: Experiments > runs > compare.")'),
        pratica("Documentação",
            "Atualize o README do projeto com o diagrama do RAG e as métricas."),
        code('# Diagrama do RAG (para o README)\n'
             'print("""\n'
             'pergunta → Vector Search (híbrido + RRF) → top-N → rerank\n'
             '        → prompt (contexto + few-shot) → FMA → resposta + fonte\n'
             '        → mlflow.evaluate (LLM-as-judge) + tracing\n'
             '""")\n'
             'print("Documente também o golden set (perguntas/esperado).")'),
        dica_prova("Na prova GenAI, saber MEDIR (métricas) e MELHORAR (híbrido/rerank/"
                   "prompt) vale mais que decorar API. Pense sempre em ciclo: medir → "
                   "diagnosticar → ajustar."),
        exercicios([
            "Registre as métricas v1 vs v2 vs v3 no README.",
            "Quais 2 ajustes mais melhoraram seu RAG?",
        ]),
        gabarito([
            ("README",
             "Tabela com faithfulness/relevance/precision/recall por versão + o que mudou "
             "entre elas."),
            ("Ajustes",
             "Ex.: rerank (recall) e prompt restritivo (faithfulness) — os dois pontos "
             "que mais importam em RAG."),
        ]),
        footer([
            "Avaliei o RAG com as 4 métricas de ouro.",
            "Usei tracing para debugar.",
            "Apliquei busca híbrida + RRF.",
            "Criei o primeiro grafo LangGraph.",
        ]),
    ],
))
