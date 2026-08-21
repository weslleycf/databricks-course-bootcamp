"""Semana 11 — GenAI: fundamentos + primeiro RAG (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana11_dia1_llm_tokens_foundation_model_apis",
    [
        header(
            "11", "1", "LLMs: tokens, contexto e Foundation Model APIs",
            "Entender o que é um LLM (tokens, janela de contexto, temperature) e usar as "
            "Foundation Model APIs do Databricks.",
            "GenAI Engineer Associate", "Primeira chamada a um LLM via FMA",
            "✅ Free Edition (FMA com quota)",
        ),
        teoria(
            "O que é um LLM",
            "Um **LLM (Large Language Model)** prevê o próximo token de uma sequência. "
            "Conceitos-base:\n\n"
            "- **Token**: unidade de texto (palavra/pedaço). 1 token ≈ 0,75 palavra em inglês.\n"
            "- **Janela de contexto**: nº máximo de tokens que o modelo 'enxerga' por chamada "
            "(ex.: 8k, 128k). Passou disso = truncamento.\n"
            "- **Temperature**: aleatoriedade da saída (0 = determinístico; 1 = criativo).\n"
            "- **System prompt**: instruções permanentes; **user prompt**: pedido da vez.\n\n"
            "> 🎯 **Dica de prova (GenAI Assoc)**: 'o que é a janela de contexto?' → limite "
            "de tokens de entrada+saída por chamada. Custo ≈ tokens processados.",
        ),
        teoria(
            "Foundation Model APIs (FMA)",
            "As **Foundation Model APIs** do Databricks dão acesso a modelos (Llama, "
            "Mistral, GPT via gateway) com **um endpoint único** e **Unity Catalog "
            "governance**: `serving_endpoint` apontando para `databricks-llama-3-1-70b`, "
            "por exemplo.\n\n"
            "Na Free Edition, as FMAs existem **com quota de uso** (limite diário) — "
            "suficiente para o curso.",
        ),
        pratica("Primeira chamada via FMA",
            "Use o MLflow Deployments para chamar um endpoint de FMA."),
        code('# Listar endpoints de FMA disponíveis\n'
             'from mlflow.deployments import get_deploy_client\n'
             'client = get_deploy_client("databricks")\n'
             'endpoints = client.list_endpoints()\n'
             'print([e.name for e in endpoints])'),
        code('# Chamada a um LLM via FMA (ajuste o nome ao endpoint disponível)\n'
             'endpoint = "databricks-llama-3-1-70b"\n'
             'resp = client.predict(\n'
             '    endpoint=endpoint,\n'
             '    inputs={"messages": [\n'
             '        {"role": "system", "content": "Você é um assistente de dados."},\n'
             '        {"role": "user", "content": "Explique em 1 frase o que é o Lakehouse."}\n'
             '    ], "temperature": 0.2})\n'
             'print(resp["choices"][0]["message"]["content"])'),
        code('# Playground (exploratório)\n'
             'print("""\n'
             '1. AI > Playground\n'
             '2. Escolha o modelo (ex.: Llama 3.1 70B)\n'
             '3. Teste: temperature 0 vs 1, system prompts diferentes\n'
             '4. Veja a contagem de tokens\n'
             '""")\n'
             'print("O Playground é o melhor laboratório para entender temperature.")'),
        dica_prova("GenAI Assoc: FMA = Foundation Model APIs, acessadas via MLflow "
                   "Deployments com governance do UC. Pergunta: 'como chamar um modelo "
                   "hospedado no Databricks?' → FMA/serving endpoint."),
        exercicios([
            "O que acontece se o prompt passar da janela de contexto?",
            "Teste a MESMA pergunta com temperature 0 e 1 — o que muda?",
            "Quantos tokens tem aproximadamente a frase 'Databricks é uma plataforma de dados'?",
        ]),
        gabarito([
            ("Janela excedida",
             "O conteúdo é truncado (entrada cortada) ou a chamada falha — por isso RAG "
             "envia só trechos relevantes, não o documento inteiro."),
            ("Temperature",
             "0 → respostas quase idênticas e determinísticas; 1 → variadas e criativas. "
             "Para SQL/JSON, use ~0."),
            ("Tokens",
             "~5–8 tokens (português usa ~1,3–1,8 token/palavra)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana11_dia2_prompt_engineering_profissional",
    [
        header(
            "11", "2", "Engenharia de prompts profissional",
            "Dominar a estrutura de prompts em 6 partes, few-shot, Chain-of-Thought e JSON "
            "mode — a base de todo aplicativo GenAI.",
            "GenAI Engineer Associate", "Promptbook do projeto criado",
            "✅ Free Edition",
        ),
        teoria(
            "A estrutura de 6 partes de um prompt profissional",
            "1. **Papel** (role): 'Você é um analista de dados sênior'\n"
            "2. **Tarefa** (task): o que fazer, verbo claro\n"
            "3. **Contexto**: dados/tabelas disponíveis\n"
            "4. **Restrições**: formato, tom, o que NÃO fazer\n"
            "5. **Formato de saída**: JSON, markdown, tabela\n"
            "6. **Exemplo** (few-shot): 1–3 exemplos\n\n"
            "Quanto mais específico, menos alucinação.",
        ),
        teoria(
            "Few-shot, Chain-of-Thought e JSON",
            "- **Few-shot**: dar exemplos no prompt ensina o padrão (ótimo p/ SQL)\n"
            "- **Chain-of-Thought (CoT)**: pedir 'pense passo a passo' melhora raciocínio "
            "— mas cuidado com custo/tokens\n"
            "- **JSON mode**: instruir saída JSON válida (parse automático)",
        ),
        pratica("Prompt estruturado",
            "Monte o prompt profissional para o assistente de vendas."),
        code('# Prompt estruturado em 6 partes\n'
             'system_prompt = """\n'
             'Você é um analista de dados sênior de uma rede de varejo.\n'
             'Tarefa: responder perguntas sobre vendas usando as tabelas abaixo.\n'
             'Tabelas disponíveis:\n'
             '- workspace.ouro.vendas_por_dia (data_venda, receita_total, n_vendas, n_notas)\n'
             '- workspace.ouro.receita_por_pais (Country, receita_total, n_vendas)\n'
             '- workspace.ouro.top_produtos (sk_produto, StockCode, Description, receita_total)\n'
             'Regras:\n'
             '- Receita = Quantity * UnitPrice.\n'
             '- Se não souber, diga que não sabe (nunca invente).\n'
             '- Responda em português.\n'
             'Formato: resposta curta + SQL usado (bloco de código).\n'
             'Exemplo:\n'
             'P: qual o país com mais receita?\n'
             'R: O país com mais receita é o United Kingdom.\n'
             '```sql\\nSELECT Country FROM workspace.ouro.receita_por_pais ORDER BY receita_total DESC LIMIT 1;\\n```\n'
             '"""\n'
             'print(system_prompt)'),
        code('# Testar o prompt via FMA\n'
             'from mlflow.deployments import get_deploy_client\n'
             'client = get_deploy_client("databricks")\n'
             'resp = client.predict(\n'
             '    endpoint="databricks-llama-3-1-70b",\n'
             '    inputs={"messages": [\n'
             '        {"role": "system", "content": system_prompt},\n'
             '        {"role": "user", "content": "Qual a receita de novembro?"}\n'
             '    ], "temperature": 0})\n'
             'print(resp["choices"][0]["message"]["content"])'),
        pratica("JSON mode",
            "Force a saída em JSON para parse programático."),
        code('# Prompt pedindo JSON (parse fácil)\n'
             'prompt_json = system_prompt + "\\nSempre responda com JSON: {\\"resposta\\": ..., \\"sql\\": ...}"\n'
             'print("Adicione o pedido de JSON ao final do system prompt.")\n'
             'print("No código, parse com json.loads(texto_entre_marcadores).")'),
        dica_prova("GenAI Assoc: domínio Application Dev (~25%) cobra prompt design: "
                   "system vs user, few-shot, CoT, JSON mode. Monte um promptbook para "
                   "reuso — é o que empresas pedem."),
        exercicios([
            "Escreva um prompt few-shot com 2 exemplos para gerar SQL de agregação.",
            "Quando NÃO usar Chain-of-Thought?",
            "Crie seu promptbook (arquivo .md) com os prompts do projeto.",
        ]),
        gabarito([
            ("Few-shot SQL",
             "Dê 2 pares (pergunta, SQL) antes da pergunta real — o modelo imita o padrão."),
            ("Sem CoT",
             "Em tarefas simples (classificação, extração) CoT gasta tokens sem ganho; use "
             "apenas em raciocínio multi-etapa."),
            ("Promptbook",
             "Crie `prompts/` no repo com system prompts versionados — igual a código."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana11_dia3_embeddings_chunking",
    [
        header(
            "11", "3", "Embeddings e chunking de documentos",
            "Entender embeddings (vetores semânticos), similaridade e as estratégias de "
            "chunking — o coração do RAG.",
            "GenAI Engineer Associate", "Pipeline de chunking + embeddings rodando",
            "✅ Free Edition",
        ),
        teoria(
            "Embeddings",
            "Um **embedding** é a representação numérica (vetor de N dimensões) do "
            "significado de um texto. Textos similares ficam **próximos** no espaço "
            "vetorial — a busca semântica usa essa distância.\n\n"
            "- Modelos de embedding: BGE, GTE, OpenAI text-embedding (via FMA)\n"
            "- Similaridade: cosseno (1 = idêntico; 0 = ortogonal)\n"
            "- **Chunking**: dividir documentos grandes em blocos (chunks) de ~200–800 "
            "tokens com overlap — o modelo só vê o contexto da janela.",
        ),
        teoria(
            "Estratégias de chunking",
            "| Estratégia | Como | Quando |\n|---|---|---|\n"
            "| **Fixo** | N tokens com overlap | docs simples |\n"
            "| **Por estrutura** | por parágrafo/seção | docs com markdown/títulos |\n"
            "| **Semântico** | junta frases similares | docs longos e heterogêneos |\n\n"
            "Regra: chunk pequeno demais = sem contexto; grande demais = ruído. "
            "Teste tamanho/overlap com as métricas de avaliação (Semana 12).",
        ),
        pratica("Chunking na prática",
            "Crie o pipeline de chunking dos produtos do catálogo."),
        code('# Documentos do projeto: descrições de produtos\n'
             'docs = spark.sql("SELECT StockCode, Description FROM workspace.prata.dim_produto WHERE Description IS NOT NULL")\\\n'
             '    .limit(500).toPandas()\n'
             'print("Documentos:", len(docs))'),
        code('# Chunking por estrutura simples (cada produto = 1 doc)\n'
             'from pyspark.sql.functions import concat, lit, col\n'
             'docs_spark = spark.table("workspace.prata.dim_produto")\\\n'
             '    .filter(col("Description").isNotNull())\\\n'
             '    .limit(500)\\\n'
             '    .withColumn("doc", concat(lit("Produto: "), col("Description"),\n'
             '                                lit(" | Código: "), col("StockCode")))\n'
             'print("Docs prontos para embedding:", docs_spark.count())'),
        code('# Texto de exemplo para embedding\n'
             'textos = ["copo de vidro vermelho", "taça para vinho", "teclado mecânico"]\n'
             'print(textos)'),
        pratica("Gerando embeddings",
            "Use a FMA de embeddings (ajuste ao endpoint disponível) e meça similaridade."),
        code('# Embeddings via FMA\n'
             'from mlflow.deployments import get_deploy_client\n'
             'client = get_deploy_client("databricks")\n'
             'resp = client.predict(\n'
             '    endpoint="databricks-bge-large-en",\n'
             '    inputs={"input": textos})\n'
             'vetores = resp["data"]\n'
             'print("Dimensão do embedding:", len(vetores[0]["embedding"]))\n'
             'print("Nº de vetores:", len(vetores))'),
        code('# Similaridade por cosseno (sem numpy, puro Python)\n'
             'import math\n'
             'def cosseno(a, b):\n'
             '    dot = sum(x*y for x, y in zip(a, b))\n'
             '    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(y*y for y in b))\n'
             '    return dot / (na * nb)\n'
             'v = [d["embedding"] for d in vetores]\n'
             'print("copo x taça (semelhantes):", round(cosseno(v[0], v[1]), 3))\n'
             'print("copo x teclado (diferentes):", round(cosseno(v[0], v[2]), 3))'),
        dica_prova("GenAI Assoc (Data Prep ~20%): chunking e embeddings são o coração. "
                   "Pergunta típica: 'por que dividir documentos em chunks?' → janela de "
                   "contexto + relevância do trecho."),
        exercicios([
            "Por que o tamanho do chunk importa para a qualidade da resposta?",
            "O que significa similaridade de cosseno = 1? E = 0?",
            "Teste 2 tamanhos de chunk e anote qual parece melhor.",
        ]),
        gabarito([
            ("Chunk",
             "Pequeno = contexto insuficiente; grande = ruído e tokens demais. O sweet "
             "spot (~200-800 tokens) depende do documento."),
            ("Cosseno",
             "1 = mesma direção (muito similares); 0 = ortogonais (sem relação); negativo = "
             "opostos."),
            ("Teste",
             "Compare respostas para a mesma pergunta com chunks de 100 vs 500 tokens — a "
             "avaliação da Semana 12 quantifica."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana11_dia4_mosaic_ai_vector_search",
    [
        header(
            "11", "4", "Mosaic AI Vector Search",
            "Criar o índice vetorial com Delta Sync e o endpoint de busca — o componente "
            "de retrieval do RAG.",
            "GenAI Engineer Associate", "Índice vetorial + endpoint funcionando",
            "✅ Free Edition (1 endpoint)",
        ),
        teoria(
            "Mosaic AI Vector Search",
            "O **Mosaic AI Vector Search** (ex-Databricks Vector Search) guarda embeddings "
            "e faz busca por similaridade em escala, integrado ao UC.\n\n"
            "Componentes:\n"
            "- **Index**: `DELTA_SYNC` (sincroniza automaticamente com a tabela Delta) ou "
            "`MANAGED` (API)\n"
            "- **Endpoint**: compute da busca (1 na Free Edition)\n"
            "- **Filtros de metadata**: refinar por colunas (ex.: categoria)\n\n"
            "O índice fica em `workspace.catalog.schema` — governado como qualquer tabela.",
        ),
        pratica("Preparando a tabela com embeddings",
            "Crie a tabela Delta com a coluna de embedding."),
        code('# Tabela com embeddings (chunk por produto)\n'
             'from pyspark.sql.functions import concat, lit, col\n'
             'df = (spark.table("workspace.prata.dim_produto")\n'
             '    .filter(col("Description").isNotNull())\n'
             '    .limit(500)\n'
             '    .withColumn("texto", concat(lit("Produto: "), col("Description"),\n'
             '                                lit(" | Código: "), col("StockCode")))\n'
             '    .select("StockCode", "texto"))\n'
             'df.write.mode("overwrite").saveAsTable("workspace.prata.produtos_rag")\n'
             'print("Tabela produtos_rag criada:", df.count(), "documentos")'),
        code('# Gerar embeddings e salvar (use a FMA disponível)\n'
             'from mlflow.deployments import get_deploy_client\n'
             'from pyspark.sql.functions import udf, array\n'
             'from pyspark.sql.types import ArrayType, DoubleType\n'
             'client = get_deploy_client("databricks")\n'
             'def embed(textos):\n'
             '    r = client.predict(endpoint="databricks-bge-large-en", inputs={"input": textos})\n'
             '    return [d["embedding"] for d in r["data"]]\n'
             '# Em produção, use o SDK de embeddings em batch; aqui demonstramos a chamada\n'
             'print("Função de embedding pronta (usada no job de indexação).")'),
        pratica("Criando o índice",
            "Pela UI: **AI → Vector Search → Create Index** (DELTA_SYNC, fonte "
            "`workspace.prata.produtos_rag`, coluna de embedding `embedding`)."),
        code('# Criar índice via SQL (onde suportado)\n'
             'sql_index = """\n'
             'CREATE OR REPLACE VECTOR INDEX workspace.prata.produtos_rag_index\n'
             'ON TABLE workspace.prata.produtos_rag\n'
             'INDEX COLUMNS (texto)\n'
             'SYNC (AUTO)\n'
             '"""\n'
             'print(sql_index)\n'
             'print("Na Free, crie pela UI: AI > Vector Search > Create Index.")'),
        pratica("Buscando",
            "Consulte o índice com a query de exemplo."),
        code('# Busca vetorial via SDK\n'
             'from databricks.vector_search.client import VectorSearchClient\n'
             'vsc = VectorSearchClient()\n'
             'resultado = vsc.similarity_search(\n'
             '    index_name="workspace.prata.produtos_rag_index",\n'
             '    query_text="copo de vidro",\n'
             '    columns=["StockCode", "texto"],\n'
             '    num_results=3)\n'
             'for r in resultado.get("result", {}).get("data_array", []):\n'
             '    print(r)'),
        dica_prova("GenAI Assoc: Vector Search com DELTA_SYNC (sincroniza com a tabela "
                   "Delta) vs MANAGED (API) é pergunta clássica. Na Free: 1 endpoint."),
        exercicios([
            "Diferença entre índice DELTA_SYNC e MANAGED?",
            "Como adicionar filtro por categoria na busca?",
            "O que acontece quando a tabela Delta muda com DELTA_SYNC?",
        ]),
        gabarito([
            ("Tipos",
             "DELTA_SYNC: espelha automaticamente a tabela Delta (recomendado). MANAGED: "
             "você gerencia os vetores via API."),
            ("Filtro",
             "Passe `filters_json` com a coluna de metadata na similarity_search."),
            ("Delta muda",
             "O índice sincroniza automaticamente (SYNC AUTO) — novos/chunks alterados "
             "aparecem sem reprocessar tudo."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana11_dia5_primeiro_rag_langchain",
    [
        header(
            "11", "5", "Primeiro RAG completo com LangChain",
            "Montar o pipeline Retrieval → Augmentation → Generation usando LangChain, o "
            "índice vetorial e a FMA.",
            "GenAI Engineer Associate", "RAG de produtos respondendo perguntas",
            "✅ Free Edition",
        ),
        teoria(
            "O padrão RAG",
            "**RAG (Retrieval-Augmented Generation)** = recuperar + gerar:\n\n"
            "```\npergunta → retrieve (índice vetorial) → contexto\n         → generate (LLM + contexto) → resposta com fonte\n```\n\n"
            "Vantagens: respostas baseadas nos SEUS dados, sem fine-tuning, com citação "
            "de fonte. É o padrão #1 em GenAI empresarial.",
        ),
        teoria(
            "LangChain",
            "O **LangChain** é o framework de orquestração de LLMs: chains, retrievers, "
            "tools e agents. No Databricks, integra-se com Vector Search e FMA nativamente.",
        ),
        pratica("Montando o RAG",
            "Conecte o retriever (Vector Search) ao LLM (FMA)."),
        code('# 1) Retriever via Vector Search\n'
             'from databricks.vector_search.client import VectorSearchClient\n'
             'from langchain_community.retrievers import DatabricksVectorSearch\n'
             'vsc = VectorSearchClient()\n'
             'retriever = DatabricksVectorSearch(\n'
             '    vsc.get_index("workspace.prata.produtos_rag_index"),\n'
             '    columns=["StockCode", "texto"])\n'
             'print("Retriever criado.")'),
        code('# 2) LLM via FMA\n'
             'from langchain_community.chat_models import ChatDatabricks\n'
             'llm = ChatDatabricks(endpoint="databricks-llama-3-1-70b", temperature=0.1)\n'
             'print("LLM conectado.")'),
        code('# 3) Chain RAG: recupera contexto e gera resposta\n'
             'from langchain.chains import create_retrieval_chain\n'
             'from langchain.chains.combine_documents import create_stuff_documents_chain\n'
             'from langchain_core.prompts import ChatPromptTemplate\n'
             '\n'
             'prompt = ChatPromptTemplate.from_messages([\n'
             '    ("system", "Responda com base SOMENTE no contexto. Cite o código do produto.\\n\\nContexto:\\n{context}"),\n'
             '    ("human", "{input}")])\n'
             'chain_docs = create_stuff_documents_chain(llm, prompt)\n'
             'rag = create_retrieval_chain(retriever, chain_docs)\n'
             'print("Chain RAG montada.")'),
        code('# 4) Perguntar ao RAG\n'
             'resp = rag.invoke({"input": "Quais produtos de vidro existem para servir bebidas?"})\n'
             'print("Resposta:", resp["answer"][:400])\n'
             'print("Fontes:", [d.metadata.get("StockCode") for d in resp["context"]])'),
        pratica("Analisando o resultado",
            "Observe: a resposta veio do contexto recuperado? As fontes citam códigos "
            "reais? Isso é o que a avaliação da Semana 12 vai medir."),
        dica_prova("GenAI Assoc (App Dev ~25%): LangChain + FMA + Vector Search é o trio. "
                   "Pergunta: 'qual framework orquestra retrieval+geração?' → LangChain."),
        exercicios([
            "Faça 5 perguntas ao RAG e anote as respostas.",
            "Por que o RAG não precisa de fine-tuning para responder sobre os dados?",
            "O que acontece se o retriever retorna chunks irrelevantes?",
        ]),
        gabarito([
            ("Perguntas",
             "Ex.: 'produtos para cozinha', 'item mais caro', etc. Avalie se as respostas "
             "usam o contexto."),
            ("Sem fine-tuning",
             "O RAG injeta o contexto no prompt — o modelo não precisa 'decorar' os dados; "
             "o conhecimento vem do retrieval."),
            ("Chunks ruins",
             "A resposta fica com ruído ou alucina — por isso a qualidade do retrieval "
             "(chunking + rerank) domina a qualidade do RAG."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana11_dia6_revisao_genai_fundamentos",
    [
        header(
            "11", "6", "Revisão GenAI + exercícios",
            "Consolidar a Semana 11: mapa mental de LLMs/RAG e exercícios no formato da "
            "prova GenAI Associate.",
            "GenAI Engineer Associate", "Exercícios resolvidos + checklist",
            "✅ Free Edition",
        ),
        teoria(
            "Mapa mental da Semana 11",
            "```\nLLMs: tokens · janela de contexto · temperature · system vs user\nFMA: Foundation Model APIs (endpoint único, UC governance)\nPrompts: 6 partes · few-shot · CoT · JSON mode\nEmbeddings: vetores semânticos · cosseno\nChunking: fixo · estrutura · semântico\nVector Search: DELTA_SYNC vs MANAGED · endpoint\nRAG: retrieve → augment → generate · LangChain\n```",
        ),
        pratica("Exercícios estilo prova (10 questões)",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** A janela de contexto é:
- A) o nº de tokens do modelo por chamada  B) o tamanho do disco
- C) a temperatura  D) o nº de parâmetros

**2.** Para respostas determinísticas, temperature:
- A) 1  B) 0  C) 0.9  D) 2

**3.** RAG significa:
- A) Retrieval-Augmented Generation  B) Random Access Generation
- C) Recurrent AI Graph  D) nada

**4.** Embeddings aproximam:
- A) textos semelhantes  B) números iguais  C) tokens grandes  D) nada

**5.** Similaridade de cosseno = 1 indica:
- A) vetores opostos  B) vetores idênticos em direção  C) erro  D) nulo

**6.** Para que serve o chunking?
- A) economizar disco  B) caber na janela + relevância  C) comprimir  D) criptografar

**7.** Índice que sincroniza com tabela Delta:
- A) MANAGED  B) DELTA_SYNC  C) INDEX_ONLY  D) AUTO

**8.** FMA é:
- A) um banco  B) Foundation Model APIs  C) um cluster  D) um job

**9.** Em um RAG, o LLM recebe:
- A) só a pergunta  B) pergunta + contexto recuperado  C) o banco inteiro  D) nada

**10.** Few-shot é:
- A) treinar com poucos dados  B) dar exemplos no prompt  C) reduzir tokens  D) cache
"""),
        teoria(
            "Gabarito",
            "**1-A** · **2-B** · **3-A** · **4-A** · **5-B** · **6-B** · **7-B** · "
            "**8-B** · **9-B** · **10-B**.",
        ),
        dica_prova("Quase tudo de GenAI se resume a: contexto (janela), qualidade do "
                   "retrieval (chunks/embeddings) e prompt. Se a pergunta for sobre "
                   "resposta errada, suspeite do retrieval."),
        exercicios([
            "Explique RAG para um colega em 2 minutos.",
            "Liste 3 fontes de erro do RAG e como mitigar cada uma.",
        ]),
        gabarito([
            ("RAG em 2 min",
             "Recupera trechos relevantes dos seus dados (vetores) e dá ao LLM como "
             "contexto para responder com fonte — sem fine-tuning."),
            ("Erros e mitigação",
             "1) chunk irrelevante → melhor chunking/rerank; 2) contexto fora da janela → "
             "chunk menor; 3) prompt fraco → few-shot/restrições."),
        ]),
        footer([
            "Chamei FMA e entendi tokens/temperature.",
            "Criei promptbook e pipeline de chunking.",
            "Construí índice Vector Search + primeiro RAG.",
            "Fiz os exercícios e revisei erros.",
        ]),
    ],
))
