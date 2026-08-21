"""Gera todos os notebooks .ipynb a partir das especificações em tools/specs/.

Rode a partir da raiz do projeto:  python tools/nbgen.py
Numeração automática: NN_semanaX_diaY_tema.ipynb em ordem global.
"""
import importlib
import json
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(TOOLS, "specs")
ROOT = os.path.dirname(TOOLS)
OUT = os.path.join(ROOT, "notebooks")


def main():
    sys.path.insert(0, TOOLS)
    os.makedirs(OUT, exist_ok=True)
    total = 0
    counter = 0
    files = sorted(f for f in os.listdir(SPECS) if f.endswith(".py") and f != "__init__.py")
    for fn in files:
        mod = importlib.import_module(f"specs.{fn[:-3]}")
        for name, cells in mod.NOTEBOOKS:
            counter += 1
            name = f"{counter:03d}_{name}"
            if not name.endswith(".ipynb"):
                name = name + ".ipynb"
            nb = {
                "cells": cells,
                "metadata": {
                    "language_info": {"name": "python"},
                    "notebook_format": {"name": "databricks"},
                },
                "nbformat": 4,
                "nbformat_minor": 5,
            }
            path = os.path.join(OUT, name)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(nb, f, ensure_ascii=False, indent=1)
            total += 1
            print(f"Gerado: {name} ({len(cells)} células)")
    print(f"\nTotal: {total} notebooks em {OUT}")


if __name__ == "__main__":
    main()
