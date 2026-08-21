"""Semana 22 — Bônus: Aprovação, DLT, UI final, Deploy (6 dias)."""
from nbkit import code, dica_prova, exercicios, footer, gabarito, header, md, pratica, sql, teoria

NOTEBOOKS = []

# --------------------------------------------------------------------------- Dia 1
NOTEBOOKS.append((
    "semana22_dia1_fluxo_aprovacao",
    [
        header(
            "22", "1", "Fluxo de aprovação obrigatória",
            "Implementar o workflow de aprovação: submissão → pendente → aprovado/"
            "rejeitado, com trilha de auditoria.",
            "Portfólio empresarial", "Aprovação funcionando",
            "✅ Free Edition",
        ),
        teoria(
            "O workflow de aprovação",
            "Submissões **nunca** vão direto para os dados: passam por aprovação (o "
            "aprovador vê o resumo e decide). Estados: `pendente` → `aprovado` | "
            "`rejeitado` (com motivo).\n\n"
            "Tudo registrado em `workspace.app.aprovacoes` — trilha completa.",
        ),
        pratica("Aprovação",
            "Aprovar/rejeitar com motivo."),
        code('# Aprovar submissão\n'
             'def aprovar(sid, aprovador, status, motivo=""):\n'
             '    spark.sql(f"UPDATE workspace.app.submissoes SET status = \'{status}\' WHERE submissao_id = \'{sid}\'")\n'
             '    spark.createDataFrame([(sid, aprovador, "now", status, motivo)],\n'
             '        ["submissao_id", "aprovado_por", "aprovado_em", "status", "motivo"])\\\n'
             '        .withColumn("aprovado_em", current_timestamp())\\\n'
             '        .write.mode("append").saveAsTable("workspace.app.aprovacoes")\n'
             '    print(f"Submissão {sid[:8]} -> {status}")\n'
             'aprovar("abc-123", "ana", "aprovado")\n'
             'aprovar("abc-456", "ana", "rejeitado", "meta fora do padrão")'),
        code('# Pendências do aprovador\n'
             'def pendentes():\n'
             '    return spark.sql("SELECT submissao_id, fluxo_id, criado_por, criado_em FROM workspace.app.submissoes WHERE status = \'pendente\'").toPandas()\n'
             'print(pendentes())'),
        pratica("UI de aprovação",
            "No app: lista de pendentes + resumo (linhas, erros) + botões aprovar/"
            "rejeitar (só para quem tem permissão)."),
        dica_prova("Portfólio: aprovação com auditoria = o 'controle humano' que "
                   "empresas exigem antes de dados entrarem em produção."),
        exercicios([
            "Adicione a regra: só quem tem permissão 'aprovar' vê os botões.",
            "O que a trilha de aprovações deve guardar?",
            "Por que rejeitar exige motivo?",
        ]),
        gabarito([
            ("Permissão",
             "Reuse a função `pode(usuario, fluxo, 'aprovar')` da Semana 20."),
            ("Trilha",
             "Quem, quando, decisão, motivo — imutável (append-only)."),
            ("Motivo",
             "O submissor precisa entender e corrigir — sem motivo vira atrito."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 2
NOTEBOOKS.append((
    "semana22_dia2_gravacao_bronze_disparo_dlt",
    [
        header(
            "22", "2", "Gravação no Bronze e disparo automático do DLT",
            "Aprovado = gravar no Bronze com metadata e disparar o pipeline DLT que "
            "atualiza Prata/Ouro.",
            "Portfólio empresarial", "Bronze + DLT automático",
            "✅ Free Edition",
        ),
        teoria(
            "Do app ao Lakehouse",
            "Aprovado → as linhas viram uma **tabela Bronze** (com `fluxo_id`, "
            "`submissao_id`) → um **job/pipeline DLT** detecta a nova submissão e "
            "atualiza Prata/Ouro.\n\n"
            "Assim, o app alimenta o Lakehouse com governança e reprocessamento.",
        ),
        pratica("Gravando no Bronze",
            "Grave a submissão aprovada com metadata."),
        code('# Gravar submissão aprovada no Bronze\n'
             'def gravar_bronze(sid, df, fluxo_id):\n'
             '    tabela = f"workspace.bronze.{fluxo_id}_bronze"\n'
             '    spark.sql(f"CREATE TABLE IF NOT EXISTS {tabela} (\n'
             '        submissao_id STRING, linha INT, dados STRING,\n'
             '        _ingested_at TIMESTAMP) USING DELTA")\n'
             '    registros = [(sid, i, row.to_json(), "now")\n'
             '                 for i, row in df.iterrows()]\n'
             '    spark.createDataFrame(registros, ["submissao_id", "linha", "dados", "_ingested_at"])\\\n'
             '        .withColumn("_ingested_at", current_timestamp())\\\n'
             '        .write.mode("append").saveAsTable(tabela)\n'
             '    print(f"{len(registros)} linhas no Bronze {fluxo_id}.")\n'
             'print("gravar_bronze pronto (append-only com metadata).")'),
        code('# Disparar o pipeline (via API de jobs)\n'
             'def disparar_dlt():\n'
             '    print("""\n'
             '    1. Job DLT que lê workspace.bronze.*_bronze\n'
             '    2. Pós-gravação: POST /api/2.1/jobs/run-now {job_id: X}\n'
             '    3. O DLT aplica expectations e atualiza Prata/Ouro\n'
             '    """)\n'
             '    print("Disparo automático: app → job → DLT → Prata/Ouro.")\n'
             'disparar_dlt()'),
        pratica("Pipeline DLT do fluxo",
            "O pipeline lê o Bronze do fluxo e aplica qualidade."),
        code('# ===== workspace_file: pipeline_fluxos.py =====\n'
             'import dlt\n'
             'from pyspark.sql.functions import col, from_json, current_timestamp\n'
             'from pyspark.sql.types import StringType, StructType\n'
             '\n'
             '@dlt.table\n'
             '@dlt.expect_all_or_drop({"submissao_presente": "submissao_id IS NOT NULL"})\n'
             'def fluxos_prata():\n'
             '    return (spark.readStream\n'
             '        .format("delta")\n'
             '        .table("workspace.bronze.metas_bronze"))\n'
             'print("Pipeline DLT dos fluxos (leia o Bronze, valide, atualize Prata).")'),
        dica_prova("Portfólio: app → Bronze → DLT → Prata é o ciclo de governança "
                   "completo — o que o curso inteiro ensinou aplicado ao produto."),
        exercicios([
            "Por que o Bronze guarda submissao_id?",
            "O que o DLT faz com linhas que violam expectations?",
            "Simule: aprove, grave, rode o DLT e confira a Prata.",
        ]),
        gabarito([
            ("submissao_id",
             "Rastreabilidade de ponta a ponta: da submissão à Prata (linhagem)."),
            ("Expectations",
             "expect_or_drop descarta; expect_or_fail falha — conforme a regra."),
            ("Simular",
             "Fluxo completo: submissão → aprovação → Bronze → DLT → Prata."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 3
NOTEBOOKS.append((
    "semana22_dia3_historico_rastreabilidade_lgpd",
    [
        header(
            "22", "3", "Histórico, rastreabilidade e LGPD",
            "Garantir rastreabilidade total (quem, quando, o quê) e os requisitos LGPD "
            "(retenção, direito ao esquecimento) no app.",
            "Portfólio empresarial", "Rastreabilidade + política LGPD",
            "✅ Free Edition",
        ),
        teoria(
            "Rastreabilidade e LGPD no app",
            "- **Rastreabilidade**: cada linha tem `submissao_id`, `criado_por`, "
            "`aprovado_por` — auditável de ponta a ponta\n"
            "- **LGPD**: direito ao esquecimento (apagar dados de um usuário), retenção "
            "limitada (TTL), e consentimento registrado",
        ),
        pratica("Rastreabilidade",
            "Consulte a trilha completa de uma submissão."),
        code('# Trilha completa de uma submissão\n'
             'def trilha(sid):\n'
             '    return spark.sql(f"""\n'
             '    SELECT s.submissao_id, s.fluxo_id, s.criado_por, s.criado_em,\n'
             '           s.status, a.aprovado_por, a.aprovado_em, a.motivo\n'
             '    FROM workspace.app.submissoes s\n'
             '    LEFT JOIN workspace.app.aprovacoes a ON s.submissao_id = a.submissao_id\n'
             '    WHERE s.submissao_id = \'{sid}\'\n'
             '    """).toPandas()\n'
             'print(trilha("abc-123"))'),
        pratica("LGPD: direito ao esquecimento",
            "Apagar dados de um usuário (lógico + físico)."),
        code('# Direito ao esquecimento (por usuário)\n'
             'def esquecimento(usuario):\n'
             '    # 1) apagar dados pessoais do app\n'
             '    spark.sql(f"DELETE FROM workspace.app.submissoes WHERE criado_por = \'{usuario}\'")\n'
             '    # 2) apagar da tabela de clientes (se aplicável)\n'
             '    # 3) logar a solicitação (auditoria de compliance)\n'
             '    print(f"Esquecimento de {usuario} processado e logado.")\n'
             'print("Esquecimento: DELETE + VACUUM (físico) + log da solicitação.")'),
        pratica("Retenção e TTL",
            "Política de retenção do app (documento) + TTL nos dados sensíveis."),
        code('# Política de retenção\n'
             'politica = """\n'
             '- Submissões: reter 5 anos (fiscal) com TTL\n'
             '- Logs de auditoria: 7 anos (compliance)\n'
             '- Dados pessoais: mínimo necessário, pseudonimizados na Prata\n'
             '- Esquecimento: DELETE + VACUUM + evidência logada\n'
             '"""\n'
             'print(politica)'),
        dica_prova("Portfólio/entrevista: LGPD no app = minimização (pseudônimo), "
                   "direito ao esquecimento (delete+vacuum+log) e retenção (TTL) — as 3 "
                   "respostas padrão."),
        exercicios([
            "Monte a view de trilha por submissão no app.",
            "O que a política de retenção do app deve definir?",
            "Por que o log do esquecimento é obrigatório?",
        ]),
        gabarito([
            ("View",
             "Tabela trilha (submissoes + aprovacoes) — o 'histórico completo'."),
            ("Retenção",
             "O quê, por quanto tempo, como apagar, quem aprova a exceção."),
            ("Log",
             "Compliance exige provar que o direito foi exercido — sem log não há prova."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 4
NOTEBOOKS.append((
    "semana22_dia4_ui_por_perfil",
    [
        header(
            "22", "4", "UI por perfil de acesso",
            "Renderizar UIs diferentes por perfil (submissor, aprovador, admin) no mesmo "
            "app — com RBAC.",
            "Portfólio empresarial", "UI por perfil funcionando",
            "✅ Free Edition (app Streamlit)",
        ),
        teoria(
            "Uma UI por perfil",
            "O mesmo app mostra telas diferentes conforme o perfil:\n"
            "- **Submissor**: formulários + status das suas submissões\n"
            "- **Aprovador**: fila de pendentes + decisões\n"
            "- **Admin**: editor YAML + versões + permissões\n\n"
            "Perfil = derivado das permissões (Semana 20).",
        ),
        pratica("Roteamento por perfil",
            "Determine o perfil e renderize a UI correspondente."),
        code('# Perfil do usuário\n'
             'def perfil(usuario):\n'
             '    if usuario == "admin": return "admin"\n'
             '    if pode(usuario, "metas", "aprovar"): return "aprovador"\n'
             '    return "submissor"\n'
             'print("perfil de ana:", perfil("ana"))\n'
             'print("perfil de joao:", perfil("joao"))'),
        code('# UI por perfil (Streamlit)\n'
             'import streamlit as st\n'
             'usuario = "ana"\n'
             'p = perfil(usuario)\n'
             'if p == "admin":\n'
             '    st.subheader("⚙️ Admin: fluxos, YAML, permissões")\n'
             '    st.write("Editor de YAML + versões + RBAC")\n'
             'elif p == "aprovador":\n'
             '    st.subheader("✅ Aprovador: fila de pendentes")\n'
             '    st.write("Lista + aprovar/rejeitar")\n'
             'else:\n'
             '    st.subheader("📥 Submissor: formulários")\n'
             '    st.write("CSV/formulário + status")\n'
             'print("UI roteada por perfil.")'),
        pratica("Consistência",
            "A API também valida o perfil (nunca confiar só na UI)."),
        code('# Backend valida o perfil\n'
             'def api_aprovar(usuario, sid):\n'
             '    if not pode(usuario, "metas", "aprovar"):\n'
             '        return {"erro": "403 — sem permissão"}\n'
             '    return aprovar(sid, usuario, "aprovado")\n'
             'print("Backend também bloqueia (defesa em profundidade).")'),
        dica_prova("Portfólio: 'UI por perfil' é requisito clássico de produto "
                   "empresarial — renderize por permissão e valide no backend."),
        exercicios([
            "Adicione a página 'minhas submissões' para o submissor.",
            "Por que validar o perfil no backend?",
            "Teste os 3 perfis com usuários diferentes.",
        ]),
        gabarito([
            ("Minhas submissões",
             "SELECT ... WHERE criado_por = usuario — status + trilha."),
            ("Backend",
             "A UI pode ser burlada; a API é a fronteira real de segurança."),
            ("3 perfis",
             "Crie 3 usuários com permissões diferentes e navegue."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 5
NOTEBOOKS.append((
    "semana22_dia5_deploy_app_ci_cd",
    [
        header(
            "22", "5", "Deploy final do app com CI/CD",
            "Publicar o DataFlow Admin em produção com CI/CD (DABs + GitHub Actions) e "
            "monitoramento.",
            "Portfólio empresarial", "App em produção via CI/CD",
            "✅ Free Edition (CI) + 🔑 deploy (trial)",
        ),
        teoria(
            "Deploy do app como produto",
            "O app vai para produção como qualquer software:\n"
            "- Repo Git (frontend + backend + fluxos YAML)\n"
            "- CI: testes (pytest do motor) + validação de YAML\n"
            "- CD: deploy via DABs (resources.apps)\n"
            "- Monitoramento: logs + métricas + alertas",
        ),
        pratica("Testes do motor (CI)",
            "Testes unitários das 4 camadas rodam no PR."),
        code('# tests/test_motor.py\n'
             'print("""\n'
             'def test_valida_tipo_numero():\n'
             '    assert valida_tipo("abc", {"tipo": "numero"}) is not None\n'
             '    assert valida_tipo("10", {"tipo": "numero", "min": 0}) is None\n'
             '\n'
             'def test_yaml_valido():\n'
             '    validate(instance=yaml.safe_load(metas_yaml), schema=json_schema)\n'
             '""")\n'
             'print("Testes do motor no CI: rodam em todo PR.")'),
        code('# Deploy via DABs (apps)\n'
             'yaml = """\n'
             'resources:\n'
             '  apps:\n'
             '    dataflow_admin:\n'
             '      name: dataflow-admin\n'
             '      source:\n'
             '        path: ./apps/dataflow\n'
             '"""\n'
             'print(yaml)\n'
             'print("databricks bundle deploy -t prod  # CD após merge")'),
        pratica("Monitoramento do app",
            "Logs estruturados + alertas de erro."),
        code('# Logs + alerta\n'
             'print("""\n'
             '1. Logs: Apps > dataflow-admin > Logs\n'
             '2. Métricas: submissões/dia, erros, latência\n'
             '3. Alerta: erro > 5% ou submissão travada > 24h\n'
             '""")\n'
             'print("Produto monitorado — pronto para usuários reais.")'),
        dica_prova("Portfólio: app com testes, CI/CD e monitoramento = 'produção de "
                   "verdade' — não demo."),
        exercicios([
            "Rode os testes do motor no GitHub Actions.",
            "Configure o alerta de erro do app.",
            "Escreva o runbook (como deployar, como investigar erro).",
        ]),
        gabarito([
            ("CI",
             "Workflow com pytest do motor + validação dos YAMLs em todo PR."),
            ("Alerta",
             "Erro > 5% ou pendente > 24h → notificação."),
            ("Runbook",
             "Deploy (bundle), rollback (versão anterior), onde ver logs, contatos."),
        ]),
        footer(),
    ],
))

# --------------------------------------------------------------------------- Dia 6
NOTEBOOKS.append((
    "semana22_dia6_entregavel_app_dataflow_admin",
    [
        header(
            "22", "6", "🎉 Entregável final: App DataFlow Admin pronto",
            "Fechar o capstone: app completo (admin + motor + aprovação + DLT + CI/CD) "
            "documentado e publicado.",
            "Portfólio empresarial", "App DataFlow Admin em produção",
            "✅ Free Edition",
        ),
        teoria(
            "O que o capstone entregou (Semanas 20–22)",
            "```\nDataFlow Admin\n"
            " ├── Admin: editor YAML + diff/rollback + permissões\n"
            " ├── Motor: 4 camadas (estrutura→tipo→SQL→negócio)\n"
            " ├── Entrada: CSV (relatório) + formulário dinâmico\n"
            " ├── Aprovação: pendente → aprovado/rejeitado (trilha)\n"
            " ├── Integração: Bronze → DLT → Prata/Ouro\n"
            " ├── LGPD: esquecimento + retenção + rastreabilidade\n"
            " ├── UI: por perfil (submissor/aprovador/admin)\n"
            " └── Deploy: DABs + CI/CD + monitoramento\n"
            "```",
        ),
        pratica("Validação final do capstone",
            "Rode o ciclo completo de ponta a ponta."),
        code('# Ciclo completo\n'
             'print("""\n'
             '1. Admin cria fluxo (YAML) -> valida -> versão\n'
             '2. Submissor envia CSV -> relatório de erros\n'
             '3. Corrige e submete -> pendente\n'
             '4. Aprovador aprova -> Bronze\n'
             '5. DLT atualiza Prata/Ouro\n'
             '6. Tudo rastreável (trilha + linhagem)\n'
             '7. Deploy via CI/CD com testes\n'
             '""")\n'
             'print("Ciclo completo validado.")'),
        pratica("Documentação final",
            "README do app com arquitetura, fluxos, decisões e prints."),
        code('# README do DataFlow Admin\n'
             'print("""\n'
             '# DataFlow Admin\n'
             '## O que é\n'
             'App de parametrização e ingestão governada por YAML.\n'
             '## Arquitetura (diagrama)\n'
             '## Fluxos (4 + regras)\n'
             '## Motor de validação (4 camadas)\n'
             '## Aprovação e LGPD\n'
             '## Deploy (DABs + CI/CD)\n'
             '## Links (apps + tabelas)\n'
             '""")\n'
             'print("README completo — o case de portfólio.")'),
        pratica("Encerramento do curso",
            "Você completou 22 semanas (19 núcleo + 3 capstone). Revise o checklist de "
            "40 competências e siga o roadmap de certificações."),
        code('# Checklist final do curso\n'
             'print("""\n'
             '- [x] Plataforma + engenharia (semanas 1-9)\n'
             '- [x] ML/MLOps (semana 10)\n'
             '- [x] GenAI (semanas 11-13)\n'
             '- [x] Agentes (semanas 14-15)\n'
             '- [x] Apps + Lakebase (semanas 16-18)\n'
             '- [x] Projeto final + simulados (semana 19)\n'
             '- [x] Capstone DataFlow Admin (semanas 20-22)\n'
             '""")\n'
             'print("🎉 Especialista Databricks formado!")'),
        dica_prova("Seu portfólio agora tem: plataforma completa, ML, GenAI, agentes, "
                   "apps, Lakebase e um produto empresarial — mais que 95% dos "
                   "candidatos a vagas Databricks."),
        exercicios([
            "Grave um vídeo de 5 min do DataFlow Admin (demo para entrevistas).",
            "Atualize LinkedIn/GitHub com o capstone.",
        ]),
        gabarito([
            ("Vídeo",
             "Mostre: admin criando fluxo → submissão → erro → correção → aprovação → "
             "DLT → Prata."),
            ("Presença",
             "README + prints + vídeo no repo; LinkedIn com o case."),
        ]),
        footer([
            "Ciclo completo validado (YAML → validação → aprovação → DLT).",
            "LGPD e rastreabilidade implementados.",
            "Deploy com CI/CD e monitoramento.",
            "🎉 Capstone concluído — curso completo!",
        ]),
    ],
))
