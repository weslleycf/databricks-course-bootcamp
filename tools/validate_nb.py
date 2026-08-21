"""Valida todos os notebooks gerados: JSON válido, nbformat 4, estrutura de células correta.

Rode:  python tools/validate_nb.py
Saída: resumo por arquivo + lista de problemas encontrados.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(ROOT, "notebooks")

PROBLEMS = []


def check_nb(path):
    rel = os.path.relpath(path, ROOT)
    try:
        with open(path, "r", encoding="utf-8") as f:
            nb = json.load(f)
    except Exception as e:
        PROBLEMS.append(f"{rel}: JSON inválido -> {e}")
        return None
    if nb.get("nbformat") != 4:
        PROBLEMS.append(f"{rel}: nbformat != 4")
        return None
    cells = nb.get("cells")
    if not isinstance(cells, list) or not cells:
        PROBLEMS.append(f"{rel}: sem células")
        return None
    ids = set()
    for i, c in enumerate(cells):
        cid = c.get("id", "")
        if not cid or cid in ids:
            PROBLEMS.append(f"{rel}: célula {i} sem id único")
        ids.add(cid)
        ct = c.get("cell_type")
        if ct not in ("markdown", "code"):
            PROBLEMS.append(f"{rel}: célula {i} tipo inválido {ct}")
            continue
        src = c.get("source", "")
        if not isinstance(src, str) or not src.strip():
            PROBLEMS.append(f"{rel}: célula {i} ({ct}) vazia")
        if ct == "code":
            if "outputs" not in c or "execution_count" not in c:
                PROBLEMS.append(f"{rel}: célula code {i} sem outputs/execution_count")
            if "\t" in src:
                PROBLEMS.append(f"{rel}: célula code {i} contém tabulação (usar espaços)")
            for bad in ("TODO", "FIXME", "pass  #", "...  #"):
                if bad in src:
                    PROBLEMS.append(f"{rel}: célula code {i} contém marcador '{bad}'")
    return len(cells)


def main():
    files = sorted(glob.glob(os.path.join(NB_DIR, "*.ipynb")))
    if not files:
        print("Nenhum notebook encontrado em", NB_DIR)
        sys.exit(1)
    total = 0
    for p in files:
        n = check_nb(p)
        if n:
            total += n
            print(f"OK   {os.path.basename(p)} ({n} células)")
        else:
            print(f"ERRO {os.path.basename(p)}")
    print(f"\n{len(files)} notebooks, {total} células")
    if PROBLEMS:
        print("\nProblemas encontrados:")
        for p in PROBLEMS:
            print(" -", p)
        sys.exit(1)
    print("Tudo OK.")


if __name__ == "__main__":
    main()
