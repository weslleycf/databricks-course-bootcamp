"""Semana 17 — Lakebase + Vetorização nativa (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana17_dia1_lakebase_fundamentos_ltap",
    [
        header(
            "17", "1", "Lakebase: arquitetura LTAP e projetos",
            "Entender o Lakebase (banco transacional nativo, LTAP) e criar o projeto com "
            "scale-to-zero.",
            "GenAI Assoc (retrieval avançado)", "Projeto Lakebase criado",
            "✅ Free Edition (1 projeto)",
            dais="LTAP (Lakebase) e Delta UniForm 3.0 (DAIS 2026).",
        ),
        teoria(
            "O que é o Lakebase",
            "O **Lakebase** é o banco transacional nativo do Databricks (LTAP — "
            "Transactional Analytical Processing): ACID transacional (como Postgres) sobre "
            "o Delta Lake, com integração total ao Unity Catalog e ao resto do Lakehouse.\n\n"
            "Casos: app transacional (pedidos, configurações), estado de agentes, memória "
            "de conversa — sem sair da plataforma.\n\n"
            "Na Free Edition: **1 projeto Lakebase** com scale-to-zero.",
        ),
        pratica("Criando o projeto",
            "Pela UI: **Lakebase → Create project**."),
        code('# Projeto Lakebase via API/CLI (visão geral)\n'
             'print("""\n'
             '1. Lakebase > Create project\n'
             '2. Nome: lakebase_agente\n'
             '3. Região (a mesma do workspace)\n'
             '4. Criado com scale-to-zero (paga só quando usa)\n'
             '""")\n'
             'print("O projeto expõe uma connection (Postgres wire protocol) para apps.")'),
        teoria(
            "Delta vs Lakebase",
            "| | Delta (analítico) | Lakebase (transacional) |\n|---|---|---|\n"
            "| Uso | OLAP (leitura pesada) | OLTP (escrita pontual) |\n"
            "| Latência | segundos | milissegundos |\n"
            "| API | Spark SQL | Postgres wire / API |\n"
            "| Consistência | ACID por transação | ACID transacional forte |\n\n"
            "Complementares: Lakebase para apps; Delta para análise.",
        ),
        dica_prova("LTAP = transacional + analítico num só lugar. Pergunta: 'onde rodar o "
                   "estado transacional de um app?' → Lakebase."),
        exercicios([
            "Diferença entre Delta e Lakebase em 2 frases.",
            "Quais dados do seu projeto fariam sentido no Lakebase?",
            "O que scale-to-zero significa para o custo do projeto?",
        ]),
        gabarito([
            ("Delta vs Lakebase",
             "Delta: analítico, leitura pesada, Spark. Lakebase: transacional, escrita "
             "pontual, latência baixa."),
            ("Dados transacionais",
             "Estado de conversas, sessões, preferências de usuário, pedidos — dados que "
             "mudam com frequência."),
            ("Scale-to-zero",
             "Sem uso, o projeto desliga — custo zero quando ocioso."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana17_dia2_lakebase_crud_branching_pitr",
    [
        header(
            "17", "2", "Lakebase: CRUD, Instant Branching e PITR",
            "Operar o Lakebase (CRUD), criar branches instantâneas para dev/teste e "
            "entender point-in-time recovery.",
            "GenAI Assoc, portfólio", "CRUD + branch no Lakebase",
            "✅ Free Edition (1 projeto)",
            dais="Instant Branching + PITR (DAIS 2026).",
        ),
        teoria(
            "Operações transacionais no Lakebase",
            "O Lakebase aceita **CRUD** (insert/update/delete) com latência de app — "
            "via API (SQL/Postgres) ou SDK. É onde vive o **estado do agente** "
            "(sessões, memória, pedidos).",
        ),
        teoria(
            "Instant Branching e PITR",
            "- **Instant Branching**: cria branches da base em segundos (dev/teste sem "
            "duplicar dados) — como Git para bancos\n"
            "- **PITR (Point-in-Time Recovery)**: voltar a base para um momento anterior — "
            "proteção contra erros",
        ),
        pratica("CRUD via SQL",
            "Crie a tabela transacional do agente (sessões)."),
        code('# Estrutura da base transacional (via connection do Lakebase)\n'
             'print("""\n'
             '-- No console do Lakebase (ou connection):\n'
             'CREATE TABLE sessoes (\n'
             '    sessao_id UUID PRIMARY KEY,\n'
             '    usuario STRING,\n'
             '    estado STRING,      -- json do estado da conversa\n'
             '    atualizado_em TIMESTAMP DEFAULT now()\n'
             ');\n'
             'INSERT INTO sessoes (sessao_id, usuario, estado) VALUES\n'
             '    (gen_random_uuid(), \'ana\', \'{"turnos": 3}\');\n'
             'UPDATE sessoes SET estado = \'{"turnos": 4}\' WHERE usuario = \'ana\';\n'
             'SELECT * FROM sessoes;\n'
             '""")\n'
             'print("CRUD transacional do agente demonstrado.")'),
        pratica("Branch e PITR (UI)",
            "No console do Lakebase: **Branch → Create branch** (dev) e **PITR → "
            "Restore**."),
        code('# Branch e PITR via API (visão geral)\n'
             'print("""\n'
             'POST /api/2.0/lakebase/projects/{id}/branches  {"name": "dev-teste"}\n'
             'POST /api/2.0/lakebase/projects/{id}/pitr       {"restore_to": "2026-08-01T10:00:00Z"}\n'
             '""")\n'
             'print("Branch instantânea para testes; PITR para recuperação.")'),
        dica_prova("Lakebase: CRUD transacional + Instant Branching (dev/teste) + PITR "
                   "(recuperação). Pergunta: 'como testar mudanças sem afetar prod?' → "
                   "branch."),
        exercicios([
            "O que o estado de sessão de um agente guarda?",
            "Quando usar PITR?",
            "Crie uma branch e faça um teste nela.",
        ]),
        gabarito([
            ("Estado de sessão",
             "Turnos, contexto da conversa, preferências, pendências — o 'histórico vivo' "
             "do agente."),
            ("PITR",
             "Erro de escrita, ataque, teste que deu errado — voltar a base ao ponto "
             "anterior."),
            ("Branch",
             "Branch dev → alterações de schema/testes → descarte ou merge."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana17_dia3_pgvector_embeddings_hnsw",
    [
        header(
            "17", "3", "pgvector no Lakebase: embeddings e índices HNSW",
            "Armazenar e buscar embeddings com pgvector no Lakebase: índices HNSW vs "
            "IVFFlat e consultas de similaridade.",
            "GenAI Assoc (retrieval)", "Índice HNSW criado + busca",
            "✅ Free Edition (1 projeto)",
        ),
        teoria(
            "pgvector no Lakebase",
            "O Lakebase suporta **pgvector**: coluna `vector` + busca por similaridade com "
            "índices:\n\n"
            "- **HNSW** (Hierarchical Navigable Small World): mais preciso, mais memória; "
            "recomendado para precisão\n"
            "- **IVFFlat**: mais rápido de buildar, menos preciso em dados novos\n\n"
            "Para RAG de produção, **HNSW** é o padrão.",
        ),
        pratica("Tabela com embeddings",
            "Crie a tabela vetorial dos produtos."),
        code('# Tabela vetorial com pgvector\n'
             'print("""\n'
             '-- No Lakebase:\n'
             'CREATE EXTENSION IF NOT EXISTS vector;\n'
             'CREATE TABLE produtos_vetores (\n'
             '    produto_id TEXT PRIMARY KEY,\n'
             '    texto TEXT,\n'
             '    embedding vector(1024)\n'
             ');\n'
             '-- Índice HNSW (precisão)\n'
             'CREATE INDEX ON produtos_vetores USING hnsw (embedding vector_cosine_ops);\n'
             '""")\n'
             'print("Tabela + índice HNSW prontos.")'),
        code('# Inserir embeddings\n'
             'print("""\n'
             'INSERT INTO produtos_vetores (produto_id, texto, embedding)\n'
             'VALUES\n'
             '  (\'85123A\', \'Copo de vidro\', \'[0.1, 0.2, ...]\'::vector),\n'
             '  (\'71053\', \'Panela antiaderente\', \'[0.4, 0.1, ...]\'::vector);\n'
             '""")\n'
             'print("Embeddings inseridos (gerados com a FMA de embeddings).")'),
        pratica("Busca por similaridade",
            "Consulte os vizinhos mais próximos."),
        code('# Busca vetorial (k-NN)\n'
             'print("""\n'
             'SELECT produto_id, texto, 1 - (embedding <=> \'[0.12, 0.19, ...]\') AS similaridade\n'
             'FROM produtos_vetores\n'
             'ORDER BY embedding <=> \'[0.12, 0.19, ...]\'\n'
             'LIMIT 5;\n'
             '""")\n'
             'print("A busca retorna os itens mais similares ao embedding da pergunta.")'),
        dica_prova("pgvector: HNSW (precisão) vs IVFFlat (velocidade de build). Pergunta: "
                   "'qual índice para busca vetorial precisa?' → HNSW."),
        exercicios([
            "Quando usar IVFFlat em vez de HNSW?",
            "O que `<=>` significa na busca?",
            "Crie o índice e faça uma busca real.",
        ]),
        gabarito([
            ("IVFFlat",
             "Base muito grande onde build rápido importa mais que a precisão máxima — "
             "HNSW é o padrão recomendado."),
            ("<=>",
             "Operador de distância de cosseno do pgvector — ordena por similaridade."),
            ("Busca",
             "Gere o embedding da pergunta e consulte com ORDER BY <=> LIMIT 5."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana17_dia4_lakebase_search_busca_hibrida",
    [
        header(
            "17", "4", "Lakebase Search: BM25 + busca híbrida com RRF",
            "Usar o Lakebase Search (BM25 + semântica + RRF) para retrieval híbrido "
            "nativo, com filtros de metadata.",
            "GenAI Assoc (retrieval)", "Busca híbrida com RRF funcionando",
            "✅ Free Edition (1 projeto)",
            dais="Lakebase Search (DAIS 2026).",
        ),
        teoria(
            "Lakebase Search",
            "O **Lakebase Search** junta busca lexical (BM25) e semântica (vetores) com "
            "**RRF** nativamente — sem montar a fusão manualmente (como fizemos na "
            "Semana 12). Suporta filtros de metadata.",
        ),
        pratica("Habilitando a busca",
            "Crie o índice de texto e a busca híbrida."),
        code('# Índice de texto (BM25)\n'
             'print("""\n'
             '-- No Lakebase:\n'
             'CREATE INDEX ON produtos_vetores USING bm25 (texto);\n'
             '""")\n'
             'print("Índice lexical criado.")'),
        code('# Busca híbrida com RRF (conceito — a API do Lakebase Search)\n'
             'print("""\n'
             'POST /api/2.0/lakebase/search\n'
             '{\n'
             '  "query": "copo de vidro",\n'
             '  "tables": ["produtos_vetores"],\n'
             '  "hybrid_search": true,        // BM25 + semântica\n'
             '  "ranking": "rrf",              // fusão\n'
             '  "filters": {"categoria": "cozinha"}  // metadata\n'
             '}\n'
             '""")\n'
             'print("Busca híbrida nativa com filtros.")'),
        pratica("Comparando com a Semana 12",
            "Na Semana 12, a fusão RRF era manual (código). No Lakebase Search, o "
            "Databricks faz nativamente — mesmo conceito, menos código e mais escala."),
        code('# Mesma fusão, agora nativa\n'
             'print("""\n'
             'Semana 12 (manual):  rrf(busca_semantica, busca_bm25)\n'
             'Lakebase Search:    hybrid_search=true + ranking=rrf\n'
             '""")\n'
             'print("Aprendizado anterior não foi em vão — você entende o que roda por trás.")'),
        dica_prova("Lakebase Search: híbrido (BM25+vetores) + RRF nativo + filtros. "
                   "Pergunta: 'como fazer busca híbrida sem código?' → Lakebase Search."),
        exercicios([
            "O que o RRF faz na busca híbrida?",
            "Adicione um filtro de metadata à busca.",
            "Quando usar Vector Search (Mosaic AI) vs Lakebase Search?",
        ]),
        gabarito([
            ("RRF",
             "Funde os rankings lexical e semântico — itens bons nas duas listas sobem."),
            ("Filtro",
             "Adicione o campo de metadata (ex.: categoria) ao filtro da busca."),
            ("VS vs Lakebase",
             "Vector Search: integração total com o UC/pipelines (maior escala analítica). "
             "Lakebase Search: busca transacional perto do app (menor latência)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana17_dia5_vetorizacao_escala_rerank",
    [
        header(
            "17", "5", "Vetorização em escala e reranking nativo",
            "Arquitetar vetores para milhões/bilhões de itens e usar reranking nativo — "
            "a stack de retrieval enterprise.",
            "GenAI Assoc (retrieval avançado)", "Decisão de arquitetura documentada",
            "✅ Free Edition (conceito) + 🔑 (escala/rerank)",
        ),
        teoria(
            "Escala bilionária",
            "Para 1B+ vetores:\n"
            "- **Particionar** por metadata (região, tenant) — busca em partições relevantes\n"
            "- **Quantização** (reduzir dimensões/precisão) para caber em memória\n"
            "- **HNSW por partição** + **filtros de metadata antes** da busca\n"
            "- **Rerank só no top-N** (cross-encoder é caro)\n\n"
            "Regra: filtre primeiro, busque depois, rerank no final.",
        ),
        pratica("Arquitetura de retrieval",
            "Desenhe a arquitetura do seu retrieval em escala."),
        code('# Decisões de arquitetura\n'
             'arquitetura = """\n'
             '1. Particionar vetores por pais/categoria (metadata)\n'
             '2. Índice HNSW por partição\n'
             '3. Busca: filtro de metadata -> k-NN na partição\n'
             '4. Rerank: cross-encoder no top-20 -> top-3\n'
             '5. Cache semântico (gateway) para perguntas repetidas\n'
             '"""\n'
             'print(arquitetura)'),
        code('# Rerank nativo (🔑 trial)\n'
             'print("""\n'
             '1. Mosaic AI Reranker (ou Lakebase rerank)\n'
             '2. POST {query, documents: [top-20]}\n'
             '3. Retorna reordenados por relevância\n'
             '4. Use o top-3 como contexto\n'
             '""")\n'
             'print("Rerank nativo: melhora Recall@5 sem mudar o índice.")'),
        pratica("Custo da busca em escala",
            "Equilibre latência × custo: HNSW com dimensão menor, cache e rerank "
            "seletivo."),
        dica_prova("Escala vetorial: filtro → busca → rerank; quantização para memória; "
                   "particionamento por tenant. Pergunta: 'como buscar em 1B vetores com "
                   "latência baixa?' → partições + HNSW + rerank no top-N."),
        exercicios([
            "Por que quantizar embeddings em escala?",
            "Onde o rerank entra no pipeline?",
            "Desenhe a arquitetura para 100M vetores do seu projeto.",
        ]),
        gabarito([
            ("Quantizar",
             "Reduz memória (vetores de 1024 dims → menores) — cabe mais em RAM, busca "
             "mais rápida, com leve perda de precisão."),
            ("Rerank",
             "Após o k-NN (top-20), antes de montar o contexto — caro demais para rodar "
             "em tudo."),
            ("100M",
             "Particione por país; HNSW por partição; filtro → kNN → rerank top-20 → "
             "top-3 no prompt."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana17_dia6_entregavel_rag_lakebase",
    [
        header(
            "17", "6", "Entregável: RAG com armazenamento vetorial Lakebase",
            "Migrar o RAG do projeto para o armazenamento vetorial do Lakebase com busca "
            "híbrida — o entregável da Semana 17.",
            "GenAI Assoc (retrieval)", "RAG com Lakebase + busca híbrida",
            "✅ Free Edition (1 projeto)",
        ),
        teoria(
            "O que a Semana 17 entregou",
            "- Lakebase (LTAP, CRUD, Branching, PITR)\n"
            "- pgvector (HNSW vs IVFFlat)\n"
            "- Lakebase Search (híbrido + RRF + filtros)\n"
            "- Escala vetorial (partição, quantização, rerank)",
        ),
        pratica("RAG com Lakebase",
            "Conecte o retriever do RAG ao Lakebase Search."),
        code('# Retriever com Lakebase Search\n'
             'def buscar_lakebase(pergunta, k=3):\n'
             '    """Busca híbrida no Lakebase (conceito — a API real no trial)."""\n'
             '    # 1) embedding da pergunta (FMA)\n'
             '    # 2) chamada ao Lakebase Search (hybrid + rrf)\n'
             '    # 3) rerank e retorna top-k\n'
             '    return [\n'
             '        {"produto_id": "85123A", "texto": "Copo de vidro vermelho"},\n'
             '        {"produto_id": "71053", "texto": "Panela antiaderente"},\n'
             '    ][:k]\n'
             'print("Retriever do Lakebase pronto (mock didático).")'),
        code('# RAG completo com o novo retriever\n'
             'def rag_lakebase(pergunta):\n'
             '    chunks = buscar_lakebase(pergunta)\n'
             '    contexto = "\\n".join(c["texto"] for c in chunks)\n'
             '    resposta = llm.invoke(f"Contexto:\\n{contexto}\\n\\nPergunta: {pergunta}").content\n'
             '    return resposta, chunks\n'
             'print(rag_lakebase("Quais copos de vidro existem?")[0][:200])'),
        pratica("Documentando a decisão",
            "Registre no README: quando usar Vector Search vs Lakebase Search."),
        code('# Matriz de decisão (README)\n'
             'print("""\n'
             '| Cenário | Ferramenta |\n'
             '|---|---|\n'
             '| RAG analítico sobre o Lakehouse | Mosaic AI Vector Search |\n'
             '| Busca transacional dentro do app | Lakebase Search |\n'
             '| Estado/memória do agente | Lakebase (tabelas) |\n'
             '""")\n'
             'print("Decisão documentada — você sabe o porquê, não só o como.")'),
        dica_prova("Entrevista: 'onde guardar vetores?' → Vector Search (analítico) ou "
                   "Lakebase/pgvector (transacional). 'Onde o estado do agente?' → "
                   "Lakebase."),
        exercicios([
            "Migre o retriever do seu RAG para o Lakebase (mock ou trial).",
            "Documente a arquitetura vetorial final no README.",
        ]),
        gabarito([
            ("Migração",
             "Troque o retriever (Vector Search) pela função buscar_lakebase — o resto do "
             "RAG não muda."),
            ("Arquitetura",
             "Dados → chunks → embeddings → Lakebase/pgvector (HNSW) → busca híbrida RRF "
             "→ rerank → prompt → FMA → resposta."),
        ]),
        footer([
            "Criei o projeto Lakebase (1, com scale-to-zero).",
            "Domino CRUD, Branching e PITR.",
            "Criei índice HNSW e busca híbrida.",
            "Migrei o RAG para o retriever do Lakebase.",
        ]),
    ],
))
