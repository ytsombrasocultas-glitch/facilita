# -*- coding: utf-8 -*-
"""Monta o dashboard final injetando os dados e o indice FIPE no template."""
import json

data = json.load(open("dados.json", encoding="utf-8"))
idx = json.load(open("fipe_index.json", encoding="utf-8"))
tpl = open("template_dashboard.html", encoding="utf-8").read()

out = tpl.replace("/*__DADOS__*/[]", json.dumps(data, ensure_ascii=False))
out = out.replace("/*__FIPE_INDEX__*/[]", json.dumps(idx, ensure_ascii=False, separators=(",", ":")))

open("dashboard.html", "w", encoding="utf-8").write(out)

assert "/*__DADOS__*/" not in out and "/*__FIPE_INDEX__*/" not in out, "placeholder nao substituido!"
print(f"OK -> dashboard.html | {len(data)} veiculos | {len(idx)} modelos FIPE")
