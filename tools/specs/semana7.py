"""Semana 7 — Governança Unity Catalog completa (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana7_dia1_uc_profundo_managed_external_volumes",
    [
        header(
            "7", "1", "Unity Catalog profundo: managed, external e Volumes",
            "Aprofundar o Unity Catalog: managed vs external tables, storage credentials e "
            "external locations, e Volumes para arquivos.",
            "DEA (UC ~30%), DEP", "Volumes + tabelas gerenciadas criadas",
            "✅ Free Edition (managed/volumes) + 🔑 external (trial)",
        ),
        teoria(
            "O UC como camada única de governança",
            "O Unity Catalog centraliza: catálogos, schemas, tabelas, views, volumes, "
            "funções, modelos ML, permissões, linhagem e auditoria. Tudo em um namespace de "
            "3 níveis — a resposta do Databricks ao 'quem tem acesso ao quê'.",
        ),
        teoria(
            "Managed vs External",
            "**Managed table**: o UC gerencia o storage e o ciclo de vida. `DROP TABLE` "
            "apaga os dados. Criada com `CREATE TABLE` (sem LOCATION).\n\n"
            "**External table**: aponta para um storage **fora do UC** via **external "
            "location** (credencial de nuvem). `DROP TABLE` não apaga os arquivos.\n\n"
            "**Storage credential**: credencial de nuvem (IAM/service principal) que "
            "autoriza o Databricks a acessar seu bucket. **External location** = "
            "credencial + caminho (ex.: `s3://meu-bucket/lake`).\n\n"
            "> ⚠️ A Free Edition **não tem** external locations — estude o conceito e "
            "valide no trial pago (Semana 7, dia com 🔑).",
        ),
        teoria(
            "Volumes",
            "**Volumes** são diretórios governados do UC para arquivos (não tabelas): "
            "modelos, parquets de staging, imagens, dados brutos. Caminho: "
            "`/Volumes/catalog/schema/volume/...`. Na Free Edition funcionam normalmente.",
        ),
        pratica("Managed + Volumes na prática",
            "Crie tabelas gerenciadas e um volume; veja a diferença de ciclo de vida."),
        sql('-- Managed table\n'
            'CREATE SCHEMA IF NOT EXISTS workspace.prata;\n'
            'CREATE OR REPLACE TABLE workspace.prata.teste_managed (id INT, nome STRING) USING DELTA;\n'
            'INSERT INTO workspace.prata.teste_managed VALUES (1, \'a\'), (2, \'b\');\n'
            'SELECT * FROM workspace.prata.teste_managed;'),
        sql('-- Volume gerenciado\n'
            'CREATE VOLUME IF NOT EXISTS workspace.prata.vol_modelos;\n'
            'SHOW VOLUMES IN workspace.prata;'),
        code('# Acessar o volume via caminho\n'
             'path = "/Volumes/workspace/prata/vol_modelos"\n'
             'spark.createDataFrame([("m1", 0.95)], ["modelo", "acuracia"]) \\\n'
             '    .write.mode("overwrite").parquet(f"{path}/resultado.parquet")\n'
             'display(spark.read.parquet(f"{path}/resultado.parquet"))'),
        dica_prova("DEA 2026: UC vale ~30%! Memorize: managed = UC gerencia + DROP apaga; "
                   "external = LOCATION + DROP preserva; Volumes = arquivos governados; "
                   "external location = credencial + caminho."),
        exercicios([
            "Qual a diferença de DROP entre managed e external table?",
            "Onde um arquivo de modelo ML deve ficar?",
            "O que compõe um external location?",
        ]),
        gabarito([
            ("DROP",
             "Managed: apaga dados. External: apaga metadados, preserva arquivos no storage."),
            ("Modelo",
             "Volume do UC (ex.: workspace.prata.vol_modelos) — governado, versionável e "
             "acessível por qualquer compute."),
            ("External location",
             "Storage credential (credencial de nuvem) + caminho de storage (ex.: "
             "s3://bucket/lake)."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana7_dia2_seguranca_rls_column_masking",
    [
        header(
            "7", "2", "Segurança: GRANT, RLS e Column Masking",
            "Implementar controle de acesso fino: permissões por grupo, dynamic views, "
            "Row-Level Security (RLS) e Column Masking de PII.",
            "DEA (UC), DEP (governança)", "RLS + masking aplicados no Ouro",
            "✅ Free Edition",
        ),
        teoria(
            "O modelo de permissões do UC",
            "Permissões são concedidas em qualquer nível: catálogo, schema, tabela/view, "
            "coluna, volume, função.\n\n"
            "```sql\nGRANT SELECT ON TABLE workspace.ouro.vendas_por_dia TO analistas;\nGRANT USAGE ON SCHEMA workspace.ouro TO analistas;\nREVOKE ...\n```\n\n"
            "Grupos (analistas, engenheiros, admins) centralizam o acesso — nunca conceda "
            "por usuário direto.",
        ),
        teoria(
            "RLS e Column Masking",
            "**Row-Level Security (RLS)**: filtra **linhas** por usuário — um vendedor vê só "
            "as vendas da sua região.\n"
            "**Column Masking**: mascara **colunas** — CPF/email aparecem mascarados para "
            "quem não tem permissão.\n\n"
            "Implementação: **dynamic view** (view com `current_user()` no WHERE) ou "
            "**functions de masking** declaradas no UC.",
        ),
        pratica("Dynamic view com RLS",
            "Crie uma view que filtra linhas por usuário — na Free Edition, o padrão para "
            "proteger o Ouro."),
        code('# Função auxiliar: mapear usuário -> país permitido\n'
             'spark.sql("""\n'
             'CREATE OR REPLACE FUNCTION workspace.ouro.pais_do_usuario()\n'
             'RETURNS STRING\n'
             'RETURN CASE WHEN current_user() = \'ana@empresa.com\' THEN \'United Kingdom\'\n'
             '            WHEN current_user() = \'joao@empresa.com\' THEN \'BRAZIL\'\n'
             '            ELSE \'*\' END\n'
             '""")\n'
             'print("Função de mapeamento usuário->país criada.")'),
        code('# Dynamic view com RLS (linhas) + masking (coluna)\n'
             'spark.sql("""\n'
             'CREATE OR REPLACE VIEW workspace.ouro.vendas_rls_vw AS\n'
             'SELECT InvoiceNo,\n'
             '       CASE WHEN current_user() IN (\'admin@empresa.com\') THEN CustomerID\n'
             '            ELSE concat(substring(CustomerID, 1, 2), \'***\') END AS CustomerID,\n'
             '       Country, Quantity, UnitPrice, Quantity * UnitPrice AS receita\n'
             'FROM workspace.bronze.vendas_bronze\n'
             'WHERE \'*\' = (SELECT pais_do_usuario())\n'
             '   OR UPPER(Country) = (SELECT pais_do_usuario())\n'
             '""")\n'
             'print("Dynamic view com RLS + masking criada.")'),
        code('# Testar como o usuário atual\n'
             'display(spark.sql("SELECT * FROM workspace.ouro.vendas_rls_vw LIMIT 10"))\n'
             'print("Se você não é admin, o CustomerID vem mascarado e o filtro de país aplica.")'),
        pratica("Permissões na prática",
            "Conceda e revogue acesso — e teste o efeito."),
        sql('GRANT USAGE ON SCHEMA workspace.ouro TO `account users`;\n'
            'GRANT SELECT ON TABLE workspace.ouro.vendas_rls_vw TO `account users`;\n'
            'SHOW GRANTS ON TABLE workspace.ouro.vendas_rls_vw;'),
        dica_prova("DEA/DEP cobram: GRANT/REVOKE por nível, dynamic views com current_user "
                   "para RLS/masking, e a diferença entre line-level e column-level "
                   "security. Memize os exemplos."),
        exercicios([
            "Crie uma dynamic view que mascara o e-mail do cliente (ex.: ana@ → a***@).",
            "Como aplicar RLS por grupo e não por usuário?",
            "O que acontece se um usuário sem SELECT consultar a view?",
        ]),
        gabarito([
            ("Masking de e-mail",
             "```sql\nCASE WHEN current_user() = 'admin' THEN email\n     ELSE concat(substring(email,1,1),'***@',split(email,'@')[1]) END\n```"),
            ("Por grupo",
             "Use `is_account_group_member('grupo')` no CASE/WHERE — a dynamic view avalia o "
             "grupo em vez do usuário individual."),
            ("Sem SELECT",
             "Falha de permissão (erro). A view exige privilégios próprios + os dos objetos "
             "de baixo — o UC exige GRANT explícito."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana7_dia3_linhagem_tags_auditoria_system_tables",
    [
        header(
            "7", "3", "Linhagem, tags e auditoria com system tables",
            "Usar linhagem de dados (column-level), tags de classificação e auditoria via "
            "system tables para governança e compliance.",
            "DEP (governança)", "Linhagem documentada + query de auditoria",
            "✅ Free Edition (parcial)",
        ),
        teoria(
            "Linhagem de dados",
            "A **linhagem** mostra de onde veio cada coluna/tabela (origem → transformação → "
            "destino). No Databricks: **Catalog → tabela → Lineage**. Ajuda em: impacto de "
            "mudança, auditoria, confiança nos dados.\n\n"
            "**Tags** classificam objetos (ex.: `PII`, `LGPD`, `região`).",
        ),
        teoria(
            "Auditoria e system tables",
            "O **system tables** (`system.access.audit`) registra quem acessou o quê, "
            "quando e de onde. Em produção (paga), fica no catálogo `system.*`:\n\n"
            "```sql\nSELECT * FROM system.access.audit\nWHERE action_name = 'QUERY' AND event_date = current_date()\n```\n\n"
            "Na Free Edition, o acesso ao `system.*` é limitado — estude a estrutura e use "
            "a linhagem da UI.",
        ),
        pratica("Tags e comentários",
            "Classifique os objetos do projeto."),
        sql('-- Tags de classificação\n'
            'ALTER TABLE workspace.bronze.vendas_bronze SET TAGS (\'PII\' = \'true\', \'LGPD\' = \'true\');\n'
            'ALTER TABLE workspace.ouro.vendas_por_dia SET TAGS (\'BI\' = \'true\');\n'
            'SHOW TAGS ON TABLE workspace.bronze.vendas_bronze;'),
        sql('-- Comentários (documentação viva)\n'
            'COMMENT ON TABLE workspace.bronze.vendas_bronze IS \'Bronze de vendas — dataset Online Retail (UCI / Databricks samples)\';\n'
            'DESCRIBE TABLE EXTENDED workspace.bronze.vendas_bronze;'),
        pratica("Linhagem pela UI",
            "1. **Catalog → workspace.bronze.vendas_bronze → tab Lineage**.\n"
            "2. Veja: vendas_bronze → fato_vendas → vendas_por_dia.\n"
            "3. Clique numa coluna: linhagem em nível de coluna.",
        ),
        code('# Exemplo de query de auditoria (produção paga)\n'
             'query_auditoria = """\n'
             'SELECT user_identity.email, action_name, request_params.path,\n'
             '       event_time\n'
             'FROM system.access.audit\n'
             'WHERE event_date >= current_date() - INTERVAL 7 DAY\n'
             'ORDER BY event_time DESC\n'
             'LIMIT 20\n'
             '"""\n'
             'print(query_auditoria)\n'
             'print("Na Free, use a UI (Audit logs não expostos por completo).")'),
        dica_prova("Pergunta DEP: 'como descobrir quem acessou uma tabela?' → system.access."
                   "audit. 'De onde veio essa coluna?' → linhagem. 'O que é esse dado?' → "
                   "tags/comentários."),
        exercicios([
            "Classifique 3 tabelas do seu projeto com tags.",
            "Use a linhagem da UI para desenhar o fluxo de vendas_bronze → Ouro.",
            "Escreva a query de auditoria que lista os últimos 10 acessos a uma tabela.",
        ]),
        gabarito([
            ("Tags",
             "`ALTER TABLE ... SET TAGS ('PII'='true')` — classificação para governança e "
             "busca."),
            ("Linhagem",
             "Catalog → tabela → Lineage: veja upstream (bronze) e downstream (prata/ouro)."),
            ("Auditoria",
             "`SELECT user_identity.email, action_name, event_time FROM system.access.audit "
             "WHERE request_params.path LIKE '%vendas%' ORDER BY event_time DESC LIMIT 10`."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana7_dia4_federation_delta_sharing",
    [
        header(
            "7", "4", "Lakehouse Federation e Delta Sharing",
            "Consultar dados fora do Databricks (Lakehouse Federation) e compartilhar dados "
            "com terceiros (Delta Sharing) — as pontes de dados empresariais.",
            "DEP (plataforma)", "Federated query + share criado",
            "🔑 Lakehouse Federation (trial) + ✅ Delta Sharing (conceito)",
        ),
        teoria(
            "Lakehouse Federation",
            "O **Lakehouse Federation** permite consultar dados que vivem **fora** do "
            "Databricks (Postgres, Snowflake, BigQuery, MySQL...) como se fossem tabelas do "
            "UC, via **connections** — sem copiar dados.\n\n"
            "Casos: migração gradual, dados operacionais, eliminar ETL de cópia.\n\n"
            "> ⚠️ Federation exige conta paga (connections a fontes externas não existem "
            "na Free Edition).",
        ),
        teoria(
            "Delta Sharing",
            "O **Delta Sharing** é o protocolo aberto de compartilhamento de dados: você "
            "compartilha tabelas com outras organizações (Databricks ou não) via **shares** "
            "e **recipients**, com controle de acesso, sem copiar dados.\n\n"
            "Na Free Edition, você pode **receber** shares (se o provedor te adicionar) e "
            "entender o protocolo; criar shares como provedor é recurso de conta completa.",
        ),
        pratica("Federation (trial pago)",
            "No workspace pago:"),
        code('# 1) Criar connection via UI\n'
             'print("""\n'
             'Catalog > Add > Connection\n'
             'Escolha o tipo (Postgres/MySQL/Snowflake/...)\n'
             'Preencha host, porta, banco, usuário e senha (via secret scope!)\n'
             '""")\n'
             'print("Depois: CREATE FOREIGN CATALOG postgres FROM CONNECTION minha_conn;")'),
        code('# 2) Consultar dados federados\n'
             'query = """\n'
             '-- A tabela remota vira catalog.schema.table normalmente\n'
             'CREATE FOREIGN CATALOG meus_dados FROM CONNECTION conn_postgres;\n'
             'SELECT * FROM meus_dados.public.clientes LIMIT 10;\n'
             '"""\n'
             'print(query)\n'
             'print("Consultas federadas usam a mesma sintaxe — o UC faz a ponte.")'),
        pratica("Delta Sharing (conceito + receber)",
            "Como **provedor** (paga): Catalog → Delta Sharing → Create Share → add tables "
            "→ Create Recipient (nome + token) → enviar token ao parceiro."),
        code('# Como RECEPTOR (Free pode receber)\n'
             'print("""\n'
             '1. O provedor te envia o token (share credential)\n'
             '2. Catalog > Delta Sharing > Open shared data\n'
             '3. Cole o token -> a tabela compartilhada aparece\n'
             '4. Consulte como tabela normal (somente leitura)\n'
             '""")\n'
             'print("Delta Sharing usa o protocolo aberto — qualquer engine Delta lê.")'),
        dica_prova("DEP 2026: Federation (connections → foreign catalogs) e Delta Sharing "
                   "(shares/recipients, protocolo aberto) são perguntas recorrentes. "
                   "Memorize a diferença: Federation = LER dados externos; Sharing = "
                   "COMPARTILHAR dados com outros."),
        exercicios([
            "Diferença entre Federation e Delta Sharing?",
            "Quais dados você compartilharia com um parceiro no seu projeto?",
            "Por que Delta Sharing não copia dados?",
        ]),
        gabarito([
            ("Federation vs Sharing",
             "Federation: consultar dados de fora (inbound, read). Sharing: expor seus dados "
             "a outros (outbound, com controle). São duas direções da mesma ponte."),
            ("Compartilhamento",
             "Ex.: Ouro de vendas agregadas por país (KPIs) para um parceiro de BI — sem "
             "enviar PII do Bronze."),
            ("Sem cópia",
             "O receptor lê os arquivos Delta diretamente do storage via token — o provedor "
             "só gerencia o acesso, sem duplicar dados."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana7_dia5_lgpd_gdpr_ttl_retention",
    [
        header(
            "7", "5", "LGPD/GDPR: direito ao esquecimento e retenção",
            "Implementar os requisitos de privacidade (LGPD/GDPR): anonimização, TTL "
            "nativo do Delta, retenção legal e apagamento.",
            "DEP (governança)", "Política de privacidade documentada",
            "✅ Free Edition (parcial) + 🔑 TTL avançado",
        ),
        teoria(
            "Privacidade no Lakehouse",
            "Leis (LGPD/GDPR) exigem: consentimento, minimização, direito ao "
            "esquecimento, retenção limitada e auditoria. No Databricks:\n"
            "- **Apagar**: `DELETE`, `DROP` (managed), ou reescrita com masking\n"
            "- **TTL nativo** (DAIS 2026): expiração automática de dados por política\n"
            "- **Retenção legal**: reter mínimo necessário (ex.: notas fiscais por 5 anos)\n"
            "- **Anonimização**: substituir PII por pseudônimos na Prata/Ouro",
        ),
        teoria(
            "Padrão: pseudonimização na Prata",
            "O **Bronze** guarda o PII cru (append-only, auditoria). A **Prata** usa "
            "pseudônimos (IDs). O **Ouro** agrega sem PII. Quem precisa de PII acessa "
            "somente o Bronze com permissão e auditoria.",
        ),
        pratica("Pseudonimização",
            "Crie uma versão da Prata sem PII (CustomerID → hash)."),
        code('# Pseudonimizar CustomerID (SHA-256) para a Prata\n'
             'from pyspark.sql.functions import sha2, col\n'
             'df = (spark.table("workspace.prata.fato_vendas")\n'
             '    .withColumn("cliente_anon", sha2(col("CustomerID"), 256)))\n'
             'df.select("cliente_anon").show(5, truncate=False)\n'
             'print("Prata sem PII cru: apenas hash — reversível somente com a chave.")'),
        pratica("Apagamento e retenção",
            "Aplique TTL/delete para o direito ao esquecimento."),
        sql('-- Direito ao esquecimento: apagar registros de um cliente\n'
            'DELETE FROM workspace.bronze.vendas_bronze WHERE CustomerID = \'12345\';\n'
            '-- (em produção, logar a solicitação e reter a evidência)\n'
            'SELECT COUNT(*) AS restantes FROM workspace.bronze.vendas_bronze;'),
        code('# TTL nativo (DAIS 2026) — expiração automática (recurso novo)\n'
             'ttl_sql = """\n'
             '-- Exemplo conceitual (conta paga):\n'
             'ALTER TABLE workspace.bronze.vendas_bronze\n'
             '  SET TBLPROPERTIES (\'delta.dataTTL\' = \'interval 5 years\');\n'
             '"""\n'
             'print(ttl_sql)\n'
             'print("TTL expira dados automaticamente após o período — compliance sem job manual.")'),
        dica_prova("Pergunta DEP/entrevista: 'como cumprir direito ao esquecimento com "
                   "Delta?' → DELETE + VACUUM (apagar físico) ou reescrita com masking; "
                   "TTL para retenção; pseudonimização na Prata. Na Free, DELETE e masking "
                   "funcionam; TTL é pago."),
        exercicios([
            "Por que manter PII no Bronze e pseudônimo na Prata?",
            "Qual a diferença entre DELETE (lógico) e VACUUM (físico)?",
            "Desenhe sua política de retenção: o que reter, por quanto tempo, e como apagar.",
        ]),
        gabarito([
            ("PII Bronze vs Prata",
             "Bronze preserva a fonte (auditoria, reprocessamento); Prata distribui somente "
             "pseudônimo — minimização de PII em consumo."),
            ("DELETE vs VACUUM",
             "DELETE marca a linha como removida (lógica, reversível via Time Travel); "
             "VACUUM remove o arquivo físico (irreversível)."),
            ("Política",
             "Ex.: Bronze retém 5 anos (auditoria fiscal) com TTL; Prata retém 2 anos; Ouro "
             "sem PII retém indefinido. Apagamento = DELETE + VACUUM + log da solicitação."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana7_dia6_revisao_governanca_exercicios",
    [
        header(
            "7", "6", "Revisão de governança + exercícios de prova",
            "Consolidar a Semana 7 com exercícios no formato da prova sobre UC, RLS, "
            "masking, auditoria e privacidade.",
            "DEA (UC), DEP", "Exercícios resolvidos + checklist",
            "✅ Free Edition",
        ),
        teoria(
            "Mapa mental da governança",
            "```\nUnity Catalog\n ├─ 3 níveis (catalog.schema.object)\n ├─ managed (DROP apaga) vs external (DROP preserva)\n ├─ Volumes (arquivos)\n ├─ Permissões (GRANT/REVOKE por nível)\n ├─ RLS (linhas) + Column Masking (colunas)\n ├─ Dynamic views (current_user)\n ├─ Linhagem + tags + auditoria (system tables)\n ├─ Federation (ler externo) + Sharing (compartilhar)\n └─ LGPD/GDPR (pseudonimização, TTL, apagamento)\n```",
        ),
        pratica("Exercícios estilo prova",
            "Marque antes do gabarito."),
        md("""### Questões

**1.** Para um usuário ver só as vendas do seu país:
- A) GRANT por tabela  B) RLS via dynamic view  C) column masking  D) tags

**2.** Para mascarar CPF em coluna:
- A) RLS  B) column masking (CASE + current_user)  C) tag PII  D) volume

**3.** `system.access.audit` serve para:
- A) otimizar  B) auditar acessos  C) versionar  D) compartilhar

**4.** Managed table: `DROP TABLE` ...
- A) preserva arquivos  B) apaga dados  C) exige LOCATION  D) nada

**5.** Para consultar dados de um Postgres externo:
- A) Delta Sharing  B) Lakehouse Federation  C) volumes  D) DABs

**6.** Para compartilhar uma tabela com um parceiro externo:
- A) Federation  B) Delta Sharing  C) merge  D) external table

**7.** Pseudonimização deve ocorrer:
- A) no Bronze  B) na Prata (saída)  C) no Ouro  D) nunca

**8.** TTL de dados (DAIS 2026) serve para:
- A) otimizar consultas  B) expirar dados automaticamente  C) backup  D) linhagem

**9.** GRANT SELECT no nível correto para uma view:
- A) volume  B) view/tabela + USAGE do schema  C) catálogo inteiro  D) cluster

**10.** A Free Edition NÃO suporta:
- A) dynamic views  B) external locations  C) RLS  D) tags
"""),
        teoria(
            "Gabarito",
            "**1-B** · **2-B** · **3-B** · **4-B** · **5-B** · **6-B** · **7-B** · "
            "**8-B** · **9-B** · **10-B**.",
        ),
        dica_prova("Quase tudo de governança responde com 'Unity Catalog'. Quando a pergunta "
                   "for sobre acesso/dados externos, desconfie de alternativas com "
                   "Federation/Sharing — o nome certo decide a questão."),
        exercicios([
            "Reexplique RLS para um colega em 1 minuto.",
            "Liste 3 diferenças entre managed e external table.",
        ]),
        gabarito([
            ("RLS em 1 min",
             "É uma view que filtra linhas conforme o usuário (current_user) — cada um vê "
             "só o que tem direito, sem criar cópias."),
            ("Managed vs external",
             "Storage (UC vs próprio), DROP (apaga vs preserva), criação (sem vs com "
             "LOCATION)."),
        ]),
        footer([
            "Criei dynamic views com RLS e masking.",
            "Usei tags, comentários e linhagem.",
            "Documentei a política LGPD/GDPR do projeto.",
            "Fiz os exercícios de prova e revisei erros.",
        ]),
    ],
))
