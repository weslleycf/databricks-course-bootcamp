# -*- coding: utf-8 -*-
"""Troca o catalogo main.* por workspace.* nos specs (curso Free Edition)."""
import glob
import io
import sys

PADROES = [
    ("main.bronze.", "workspace.bronze."),
    ("main.prata.", "workspace.prata."),
    ("main.ouro.", "workspace.ouro."),
    ("main.app.", "workspace.app."),
    ("main.audit.", "workspace.audit."),
    ("/Volumes/main/", "/Volumes/workspace/"),
    ("IN main", "IN workspace"),
    ("main_dev", "workspace_dev"),
    ("main_prod", "workspace_prod"),
    ("`main`", "`workspace`"),
    ("catalogo main", "catalogo workspace"),
    ("catálogo main", "catálogo workspace"),
    ("SHOW SCHEMAS IN main", "SHOW SCHEMAS IN workspace"),
    ("CREATE SCHEMA IF NOT EXISTS main.", "CREATE SCHEMA IF NOT EXISTS workspace."),
    ("SCHEMA main.", "SCHEMA workspace."),
    ("schema: `main.", "schema: `workspace."),
    ("`main.bronze`", "`workspace.bronze`"),
]

total = 0
ARQS_DOCS = [
    "README.md",
    "FONTES_DATASET.md",
    "PLANO_CURSO_RESTRUTURADO.md",
    "PROMPT_PLANO_CURSO.md",
]
for f in sorted(glob.glob("tools/specs/*.py")) + ARQS_DOCS:
    with io.open(f, "r", encoding="utf-8") as fh:
        s = fh.read()
    antes = s
    for a, b in PADROES:
        s = s.replace(a, b)
    if s != antes:
        with io.open(f, "w", encoding="utf-8", newline="") as fh:
            fh.write(s)
        n = sum(antes.count(a) for a, _ in PADROES)
        total += n
        sys.stdout.write(f"{f}: {n} substituicoes\n")
sys.stdout.write(f"TOTAL: {total}\n")
