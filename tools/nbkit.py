"""DSL para construir notebooks Databricks (nbformat 4) a partir de especificações em Python.

Uso: cada arquivo em tools/specs/ define `NOTEBOOKS = [ (nome_sem_enum, [células...]), ... ]`.
O script tools/nbgen.py numera e escreve os arquivos .ipynb em notebooks/.
"""
import uuid


def _cell_id():
    return uuid.uuid4().hex


def md(src):
    """Célula markdown."""
    return {"cell_type": "markdown", "metadata": {}, "source": src, "id": _cell_id()}


def code(src):
    """Célula de código Python (rodada no notebook serverless)."""
    return {
        "cell_type": "code",
        "metadata": {},
        "source": src,
        "execution_count": None,
        "outputs": [],
        "id": _cell_id(),
    }


def sql(src):
    """Célula de código SQL (%sql)."""
    return code("%sql\n" + src)


def header(week, day, title, objetivo, certificacao, entregavel, plano,
           tempo="2h", pre="SQL e Python básicos · notebooks anteriores do curso", dais=None):
    t = f"""# 📓 Semana {week} · Dia {day} — {title}

**Curso**: Especialista Databricks — Engenharia de Dados → GenAI → Agentes

| Campo | Valor |
|---|---|
| **Plano** | {plano} |
| **Tempo estimado** | {tempo} |
| **Certificação alvo** | {certificacao} |
| **Pré-requisitos** | {pre} |
| **Entregável do dia** | {entregavel} |
"""
    if dais:
        t += f"\n> 🎯 **DAIS 2026**: {dais}\n"
    t += "\n---\n"
    return md(t)


def teoria(title, body):
    return md(f"## 📖 Teoria — {title}\n\n{body}\n")


def pratica(title, body):
    return md(f"### 💻 Na prática — {title}\n\n{body}\n")


def dica_prova(texto):
    return md(f"> 🎯 **Dica de prova**: {texto}\n")


def exercicios(itens):
    s = "## 🎯 Exercícios de fixação\n\n"
    for i, it in enumerate(itens, 1):
        s += f"**{i}.** {it}\n\n"
    s += "\n> Tente resolver **antes** de olhar o gabarito no final do notebook.\n"
    return md(s)


def gabarito(itens):
    """itens: lista de (pergunta_curta, resposta_comentada)."""
    s = "## 🗝️ Gabarito comentado\n\n"
    for i, (pergunta, resp) in enumerate(itens, 1):
        s += f"**{i}.** {pergunta}\n\n{resp}\n\n"
    return md(s)


def footer(checklist=None):
    itens = checklist or [
        "Rodei todas as células do notebook do início ao fim sem erros.",
        "Consigo explicar os conceitos de hoje em 3 frases (sem olhar o material).",
        "Fiz os exercícios e conferi o gabarito.",
        "Anotei as dúvidas que preciso revisar.",
    ]
    s = "## ✅ Checklist de fechamento\n\n" + "\n".join(f"- [ ] {i}" for i in itens)
    s += "\n\n---\n*Próximo passo: siga para o notebook seguinte do plano do curso.*"
    return md(s)
