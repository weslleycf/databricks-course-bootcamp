# -*- coding: utf-8 -*-
import glob
import io
import sys

total_main = 0
total_ws = 0
total_vol_ws = 0
total_vol_main = 0
for f in glob.glob("notebooks/*.ipynb"):
    with io.open(f, "r", encoding="utf-8") as fh:
        s = fh.read()
    total_main += (
        s.count("main.bronze")
        + s.count("main.prata")
        + s.count("main.ouro")
        + s.count("main.app")
        + s.count("main.audit")
    )
    total_ws += (
        s.count("workspace.bronze")
        + s.count("workspace.prata")
        + s.count("workspace.ouro")
        + s.count("workspace.app")
        + s.count("workspace.audit")
    )
    total_vol_ws += s.count("/Volumes/workspace/")
    total_vol_main += s.count("/Volumes/main/")

out = [
    "main.* catalogo: %d" % total_main,
    "workspace.* catalogo: %d" % total_ws,
    "/Volumes/workspace/: %d" % total_vol_ws,
    "/Volumes/main/: %d" % total_vol_main,
]
sys.stdout.write("\n".join(out) + "\n")
