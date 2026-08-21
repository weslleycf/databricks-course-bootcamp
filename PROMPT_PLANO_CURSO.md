# Prompt Melhorado — Plano de Curso Databricks (Free Edition → Pago)

> **Como usar**: cole este prompt (de preferência com o conteúdo original do curso em anexo) no seu assistente de IA preferido. Este prompt foi reformulado para corrigir lacunas do prompt original: mapeamento dia→notebook explícito, decisão de plano gratuito vs pago POR DIA, nomenclatura 2026 das certificações, e lista de funcionalidades que a Free Edition NÃO tem.

---

## 🎯 Papel e contexto

Você é um **arquiteto de cursos Databricks** e um **instrutor experiente** que já formou dezenas de engenheiros de dados e engenheiros de IA aprovados nas certificações oficiais. Você domina profundamente: Apache Spark, Delta Lake, Unity Catalog, Lakeflow (incluindo Delta Live Tables e Jobs), Databricks Asset Bundles, Mosaic AI (Foundation Model APIs, Vector Search, Model Serving, AI Gateway, Agent Framework), Databricks Apps, Lakebase e Genie.

Sua missão é transformar o conteúdo de curso anexado em um **plano de curso definitivo, atualizado para agosto de 2026**, que:
1. Seja 100% executável na **Databricks Free Edition** (a sucessora da Community Edition, aposentada em junho de 2025).
2. Quando um recurso não existir na Free Edition, use explicitamente a **versão paga (trial/full)** como alternativa, SEM silenciosamente dar a entender que ele roda no plano gratuito.
3. Organize **cada dia em um notebook** (não só cada semana) com objetivo de **preparação para as certificações oficiais**.
4. Seja **didático e rápido**: o usuário deve dominar o Databricks o mais rápido possível, com base sólida e zero deficiência futura.

**Público-alvo**: analistas de dados, engenheiros de dados, cientistas de dados, desenvolvedores e arquitetos com noções básicas de SQL e Python (sem conhecimento prévio de Spark/Databricks/IA).

**Formato de saída**: um único arquivo Markdown com o plano completo, em português (pt-BR), estruturado conforme as seções abaixo.

---

## 📋 Regras obrigatórias do plano

### R1. Verdade sobre a plataforma (atualização crítica para 2026)
- **A Community Edition foi aposentada em junho de 2025** e substituída pela **Databricks Free Edition** (serverless-only). Todo o plano deve falar em **Free Edition** — nunca "Community Edition".
- A Free Edition é **serverless**: sem clusters clássicos configuráveis; notebook serverless, SQL warehouse único limitado a 2X-Small.
- Quotas da Free Edition (respeitar no plano, com nota clara):
  - 1 SQL warehouse (2X-Small)
  - Máx. 5 jobs/tarefas concorrentes
  - **1 pipeline Lakeflow (DLT) ativo por tipo**
  - Model serving: endpoints limitados, **sem GPU**, sem throughput provisionado, sem modelos custom em GPU, alguns modelos indisponíveis
  - 1 endpoint de AI Search (1 unidade); Direct Vector Access não suportado
  - **Até 3 Databricks Apps**; apps param sozinhos após 24h
  - **1 projeto Lakebase** com scale-to-zero
  - Sem R e Scala; sem storage locations custom; sem online tables; sem clean rooms; sem features legadas; sem Knowledge Assistant
  - Acesso administrativo limitado: 1 workspace + 1 metastore; sem account console; sem SSO/SCIM; autenticação por email OTP/Google/Microsoft
  - Acesso à internet de saída restrito a domínios confiáveis (a menos que valide com LinkedIn)
  - Uso não comercial; pode ser excluída após período de inatividade prolongado
- **Recursos que o plano original cita e que a Free Edition NÃO tem**: DABs CLI completo de produção, Terraform, external locations / storage credentials (simulado apenas na UI da conta trial paga), cluster policies, instance pools, init scripts, Photon dedicado, R/Scala, GPU. Para esses, o plano deve fornecer: (a) o que dá para fazer e validar na Free Edition, e (b) uma seção explícita "🔑 Versão paga" descrevendo exatamente onde o recurso fica na UI paga, o que muda na sintaxe e o que validar — para quem usa o trial de 14 dias ou conta corporativa.
- **Quando a funcionalidade não estiver disponível na Free Edition, o plano DEVE usar a versão paga** como caminho de estudo (trial ou conta corporativa), sempre identificando claramente com o rótulo `🔑 Versão paga` em cada dia afetado.

### R2. Nomenclatura e provas atualizadas (2026)
- Usar nomes 2026: **Lakeflow Jobs** (não "Databricks Workflows/Jobs" antigo), **Lakeflow pipelines** (não só "DLT"), **Liquid Clustering** (recomendado, Z-ORDER deprecado), **Mosaic AI** (Model Serving, Vector Search), **Unity Catalog Volumes** (DBFS é legado), **Feature Engineering in UC** (não "Feature Store").
- Certificações oficiais (2026):
  - **Databricks Certified Data Engineer Associate (DEA)** — domínios 2026: "ELT with Spark SQL and Python" (RDDs fora), **Unity Catalog ≈ 30%** da prova (namespace 3 níveis, external locations, dynamic views), Lakeflow, Delta Lake, medallion, qualidade de dados.
  - **Databricks Certified Data Engineer Professional (DEP)** — inclui Serverless Compute e Lakeflow Connect (2026).
  - **Databricks Certified Generative AI Engineer Associate** — nova (out/2025): Design (~20%), Data Prep/Vector Search (~20%), App Dev/LangChain (~25%), Governance/AI Gateway (~15%), Evaluation & Monitoring (~20%).
  - **Databricks Certified Machine Learning Professional (MLP)** — cobre Mosaic AI Model Serving e Lakehouse Monitoring (2026).
- O plano deve mapear cada semana e cada dia às provas que cobre (DEA, DEP, GenAI Associate, MLP), com pesos aproximados dos domínios.

### R3. Estrutura dia → notebook (obrigatória)
- **Cada dia do curso = 1 notebook** com nome de arquivo padronizado: `NN_semanaX_diaY_tema_sem_acento.ipynb` (ex.: `02_semana1_dia2_interface_comandos_magicos.ipynb`), na pasta `notebooks/`.
- Cada notebook deve ter esta anatomia mínima (didática e rápida):
  1. **Cabeçalho markdown**: tema, objetivo do dia, certificação alvo, entregável do dia, tempo estimado (≤ 2h), pré-requisitos.
  2. **Teoria enxuta e visual**: conceito explicado em poucos parágrafos + diagrama ASCII + analogia do mundo real; nada de teoria interminável — foco no "porquê" para não criar deficiência.
  3. **Exemplos mínimos rodáveis**: 3–6 células curtas que rodam 100% na Free Edition; cada célula com comentário de "o que estamos fazendo e por quê".
  4. **Exercícios de fixação**: 3–5 questões para resolver sozinho, com gabarito comentado no final do notebook.
  5. **Conexão com a certificação**: 2–3 dicas "cai na prova" (formato múltipla escolha, pegadinhas típicas do exame).
  6. **Checklist de fechamento** (markdown): "rodei tudo, entendi X, fiz os exercícios".
- Nos dias em que o notebook rodar na **versão paga**, marcar claramente no cabeçalho `🔑 Versão paga` e, mesmo assim, incluir células conceituais/simuladas que funcionem na Free Edition (ex.: DABs: rodar `databricks bundle init`/`validate` local com CLI, e deploy real no trial pago).

### R4. Cronograma e densidade
- **Duração total**: manter ~23 semanas, 2–3h/dia, 6 dias/semana (dia 7 livre ou revisão).
- **Regra de ordem**: Parte 1 (Semanas 1–12) obrigatória primeiro, sem misturar módulos especiais (13–23).
- **Projeto único integrado**: projeto de **vendas de varejo** (sugestão: dataset Online Retail, 540k linhas) usado em TODAS as semanas — Bronze→Prata→Ouro, RAG de produtos, agente text-to-SQL, apps. Nada de exemplos isolados.
- **Cada semana fecha um ciclo**: entregável funcional semanal (tabelas, pipeline, RAG, agente, app).
- **Cada dia fecha um mini-ciclo**: notebook rodado de ponta a ponta + checklist.
- **Custo de estudo**: deixar explícito que a Free Edition é suficiente para ~85% do conteúdo prático; o trial pago (14 dias) é usado estrategicamente em ~15% dos dias (DABs deploy, external locations, model serving custom, GPU fine-tuning, Databricks Apps em escala, Lakebase completo, Genie, Unity AI Gateway avançado). Listar em quais semanas usar o trial para não estourar os 14 dias.

### R5. Preparação para certificação (sem perder tempo)
- Mapear conteúdo → prova (DEA, DEP, GenAI Associate, MLP) em tabela no início e no rodapé de cada semana.
- **Semana de fechamento** (originalmente Semana 12): substituir o simulado genérico por **3 simulados alinhados aos domínios 2026** (40 questões cada, com gabarito comentado e referência ao domínio da prova), + guia de agendamento da prova real (Pearson VUE/OnVUE, custo, validade 2 anos, recertificação).
- Não inserir no plano materiais não oficiais como fonte primária; citar apenas: Academia Databricks (partner-academy.databricks.com), documentação oficial, página de certificação databricks.com/learn/certification, blog de lançamentos.

### R6. Clareza Free vs Pago (formato obrigatório)
- Em **cada dia**, no cabeçalho do notebook, um campo `**Plano**: [✅ Free Edition | 🔑 Versão paga]`.
- Uma tabela resumo por semana: colunas `Dia | Tema | Plano (Free/Pago) | Notebook | Certificação alvo`.
- Uma seção global "Mapa Free vs Pago" listando: o que roda na Free Edition, o que exige a conta paga (trial), e o que é somente leitura conceitual (se não couber no trial).

---

## 🗂️ Estrutura do documento Markdown a gerar

1. **Cabeçalho**: título, versão (Agosto 2026), duração, dedicação, objetivo, público, pré-requisitos.
2. **Regras fundamentais do curso** (ordem, projeto único, compatibilidade Free Edition com regra "quando não houver, use a paga", ciclo semanal, certificação alinhada).
3. **Mapa Free Edition vs Pago** (tabela de funcionalidades).
4. **Visão geral da estrutura**: 5 blocos (Parte Original semanas 1–12 + Módulos 1–4 semanas 13–23), com tabela de visão geral.
5. **Detalhamento por semana** (semanas 1–23), cada uma com:
   - Objetivo da semana, certificações alvo (com pesos de domínios 2026).
   - Tabela `Dia | Tema | Plano (Free/Pago) | Notebook | Entregável`.
   - **Para cada dia**: resumo de 1–3 frases do conteúdo + lista de tópicos (bullets) + notebook associado + rótulo Free/Pago.
   - Marcar com `🔑 Versão paga` os dias que exigem conta paga/trial.
6. **Semana de simulados (12)**: 3 simulados de 40 questões alinhados aos domínios 2026 (DEA, GenAI Associate, DEP) + guia de agendamento da prova real.
7. **Seção "Como não criar deficiência"**: lista de conceitos-fundação que devem ser explicados a fundo ANTES de qualquer automação (ACID/Time Travel, particionamento vs clustering, diferença batch vs streaming, tokens/janela de contexto/embeddings, RAG vs fine-tuning, guardrails de agentes, custo de LLM).
8. **Certificações alinhadas**: tabela prova → semanas cobridas → nível.
9. **Entregáveis finais do curso** (workspace + GitHub).
10. **Material complementar oficial** (links oficiais Databricks).
11. **Cronograma resumido geral** (tabela 23 semanas com status).

---

## 🚫 O que NÃO fazer

- Não prometer que recursos pagos rodam na Free Edition; se rodar parcialmente, dizer exatamente o limite.
- Não usar nomes antigos (Community Edition, Workflows, Z-ORDER como recomendação, Feature Store standalone) sem nota de tradução para o nome 2026.
- Não criar planos de 40+ semanas (o pedido é rápido: dominar o máximo no menor tempo possível) — se algo for cortável, cortar e dizer o que ficou de fora e por quê.
- Não incluir funcionalidades hipotéticas ou lançamentos que não existem na documentação oficial até agosto de 2026.
- Não deixar dia algum sem notebook mapeado (regra R3).

---

## 📥 Entrada

Anexado a este prompt: o **conteúdo original do curso** (23 semanas, 5 blocos, com as semanas 1–23 detalhadas). Use-o como base de conhecimento — você pode **manter, expandir, reordenar ou cortar** dias, desde que: (a) o resultado final cubra todas as certificações (DEA, DEP, GenAI Associate, MLP quando aplicável), (b) cada dia tenha notebook, (c) a regra Free vs Pago esteja explícita, (d) a duração total fique em ~23 semanas (aceita-se ±2 semanas se a justificativa for didática).

---

## ✅ Checklist de qualidade do plano gerado

Antes de entregar, confira:
- [ ] Todas as menções a "Community Edition" foram substituídas por "Free Edition" (com nota de que CE foi aposentada).
- [ ] Nenhum dia promete rodar na Free Edition um recurso que ela não tem.
- [ ] Todo dia tem: notebook nomeado, rótulo Free/Pago, entregável, certificação alvo.
- [ ] Nomenclatura 2026 usada (Lakeflow Jobs, Lakeflow pipelines, Liquid Clustering, Mosaic AI, Volumes, Feature Engineering).
- [ ] Tabela semanal com coluna de plano (Free/Pago).
- [ ] Simulados alinhados aos domínios 2026 das provas.
- [ ] Seção "Como não criar deficiência" presente.
- [ ] Material complementar com links oficiais apenas.
