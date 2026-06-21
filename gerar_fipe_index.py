# -*- coding: utf-8 -*-
"""
Baixa UMA vez o indice de marcas+modelos da Tabela FIPE (carros) e salva em
fipe_index.json. Esse indice fica embutido no dashboard para a busca por texto
ser instantanea. O valor de cada carro continua sendo consultado ao vivo.
"""
import json, time, urllib.request

API = "https://parallelum.com.br/fipe/api/v1/carros"

def get(url, tentativas=4):
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "facilita-dashboard"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i == tentativas - 1:
                raise
            time.sleep(1.5 * (i + 1))

marcas = get(f"{API}/marcas")
print(f"{len(marcas)} marcas. Baixando modelos...")

indice = []
for n, m in enumerate(marcas, 1):
    try:
        data = get(f"{API}/marcas/{m['codigo']}/modelos")
        for mod in data["modelos"]:
            indice.append({
                "b": m["codigo"],          # codigo marca
                "bn": m["nome"],           # nome marca
                "m": mod["codigo"],        # codigo modelo
                "mn": mod["nome"],         # nome modelo
            })
        print(f"  [{n}/{len(marcas)}] {m['nome']}: {len(data['modelos'])} modelos")
    except Exception as e:
        print(f"  [{n}/{len(marcas)}] {m['nome']}: ERRO ({e})")
    time.sleep(0.15)

with open("fipe_index.json", "w", encoding="utf-8") as f:
    json.dump(indice, f, ensure_ascii=False, separators=(",", ":"))

print(f"\nOK -> fipe_index.json com {len(indice)} modelos")
