# -*- coding: utf-8 -*-
"""
Gerador de dados simulados para uma revenda de veiculos.
Cria o arquivo vendas_veiculos.csv com registros realistas.
"""
import csv
import json
import random
from datetime import date, timedelta

random.seed(42)

# -------------------------------------------------------------------
# Catalogo de veiculos: marca -> [(modelo, categoria, faixa_preco_base)]
# faixa_preco_base = valor de referencia FIPE aproximado (R$) p/ um modelo recente
# -------------------------------------------------------------------
CATALOGO = {
    "Volkswagen": [
        ("Gol", "Hatch", 55000), ("Polo", "Hatch", 85000), ("T-Cross", "SUV", 130000),
        ("Nivus", "SUV", 125000), ("Virtus", "Sedan", 95000), ("Saveiro", "Picape", 90000),
    ],
    "Chevrolet": [
        ("Onix", "Hatch", 80000), ("Onix Plus", "Sedan", 88000), ("Tracker", "SUV", 130000),
        ("S10", "Picape", 220000), ("Spin", "Minivan", 110000), ("Cruze", "Sedan", 120000),
    ],
    "Fiat": [
        ("Mobi", "Hatch", 65000), ("Argo", "Hatch", 78000), ("Cronos", "Sedan", 85000),
        ("Toro", "Picape", 160000), ("Strada", "Picape", 110000), ("Pulse", "SUV", 115000),
    ],
    "Toyota": [
        ("Corolla", "Sedan", 160000), ("Corolla Cross", "SUV", 195000), ("Hilux", "Picape", 280000),
        ("Yaris", "Hatch", 95000), ("Etios", "Sedan", 60000),
    ],
    "Hyundai": [
        ("HB20", "Hatch", 80000), ("HB20S", "Sedan", 88000), ("Creta", "SUV", 140000),
        ("Tucson", "SUV", 180000),
    ],
    "Honda": [
        ("Civic", "Sedan", 170000), ("City", "Sedan", 110000), ("HR-V", "SUV", 160000),
        ("Fit", "Hatch", 85000),
    ],
    "Renault": [
        ("Kwid", "Hatch", 60000), ("Sandero", "Hatch", 72000), ("Duster", "SUV", 120000),
        ("Logan", "Sedan", 75000), ("Oroch", "Picape", 115000),
    ],
    "Jeep": [
        ("Renegade", "SUV", 130000), ("Compass", "SUV", 180000), ("Commander", "SUV", 230000),
    ],
    "Nissan": [
        ("Kicks", "SUV", 125000), ("Versa", "Sedan", 100000), ("Frontier", "Picape", 250000),
    ],
    "Ford": [
        ("Ka", "Hatch", 55000), ("EcoSport", "SUV", 95000), ("Ranger", "Picape", 240000),
    ],
}

CORES = ["Branco", "Prata", "Preto", "Cinza", "Vermelho", "Azul", "Prata"]  # branco/prata mais comuns
COMBUSTIVEIS = ["Flex", "Flex", "Flex", "Diesel", "Gasolina"]
CAMBIOS = ["Manual", "Automatico", "Automatico"]
FORMAS_PAGAMENTO = ["Financiamento", "Financiamento", "A vista", "Consorcio", "Troca + Financiamento"]

VENDEDORES = [
    "Carlos Eduardo", "Fernanda Lima", "Roberto Alves", "Juliana Souza",
    "Marcos Pereira", "Patricia Gomes",
]
# peso de performance por vendedor (uns vendem mais que outros)
PESO_VENDEDOR = [0.24, 0.22, 0.18, 0.15, 0.13, 0.08]

CIDADES = [
    "Curitiba", "Sao Jose dos Pinhais", "Pinhais", "Colombo", "Araucaria",
    "Ponta Grossa", "Maringa", "Londrina", "Cascavel", "Guarapuava",
]

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Eduardo", "Fabiana", "Gustavo", "Helena",
         "Igor", "Joana", "Lucas", "Mariana", "Nelson", "Olivia", "Paulo", "Rafaela",
         "Sergio", "Tatiana", "Vinicius", "Wesley"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida",
              "Costa", "Carvalho", "Ribeiro", "Martins", "Rocha", "Barbosa", "Teixeira"]

ANO_ATUAL = 2026

def cliente_aleatorio():
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"

def gerar_placa():
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return (random.choice(letras) + random.choice(letras) + random.choice(letras)
            + str(random.randint(0, 9)) + random.choice(letras)
            + str(random.randint(0, 9)) + str(random.randint(0, 9)))

def escolher_modelo():
    marca = random.choice(list(CATALOGO.keys()))
    modelo, categoria, base = random.choice(CATALOGO[marca])
    return marca, modelo, categoria, base

# -------------------------------------------------------------------
# Geracao dos registros
# -------------------------------------------------------------------
registros = []
total = 260
inicio_periodo = date(2025, 1, 1)
hoje = date(2026, 6, 21)

vid = 1
for _ in range(total):
    marca, modelo, categoria, base = escolher_modelo()

    ano_modelo = random.choices(
        [ANO_ATUAL, 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018],
        weights=[3, 8, 12, 14, 14, 12, 10, 7, 5],
    )[0]
    ano_fab = ano_modelo if random.random() > 0.3 else ano_modelo - 1
    idade = ANO_ATUAL - ano_modelo

    # depreciacao: ~9% ao ano sobre a base
    valor_mercado = base * (0.91 ** idade)
    km = int(max(0, random.gauss(idade * 12000 + 5000, 8000)))

    # valor de compra: revenda compra abaixo do mercado (margem de negociacao)
    valor_compra = valor_mercado * random.uniform(0.82, 0.92)
    valor_compra = round(valor_compra / 100) * 100  # arredonda p/ centena

    # despesas de preparacao (revisao, pneu, funilaria, documentacao...)
    despesas = max(300, random.gauss(2000, 1200))
    despesas = round(despesas / 100) * 100
    total_investido = valor_compra + despesas

    # valor de referencia FIPE/mercado p/ aquele carro (simulado nesta demo)
    valor_fipe = round(valor_mercado * random.uniform(0.97, 1.05) / 100) * 100

    # data de entrada no estoque
    data_compra = inicio_periodo + timedelta(days=random.randint(0, 520))

    # decide se ja foi vendido
    # carros mais antigos no estoque tem mais chance de ja terem vendido
    prob_vendido = 0.80
    vendido = random.random() < prob_vendido

    if vendido:
        dias_estoque = max(3, int(random.gauss(45, 30)))
        data_venda = data_compra + timedelta(days=dias_estoque)
        if data_venda > hoje:
            # ainda nao vendeu de fato
            vendido = False

    if vendido:
        # vende perto do valor de mercado (FIPE), com pequena variacao de negociacao
        valor_venda = valor_fipe * random.uniform(0.95, 1.03)
        valor_venda = round(valor_venda / 100) * 100
        # lucro REAL: desconta a compra E as despesas de preparacao
        lucro = valor_venda - total_investido
        vendedor = random.choices(VENDEDORES, weights=PESO_VENDEDOR)[0]
        cliente = cliente_aleatorio()
        cidade = random.choice(CIDADES)
        forma = random.choice(FORMAS_PAGAMENTO)
        status = "Vendido"
        data_venda_str = data_venda.isoformat()
        dias_em_estoque = (data_venda - data_compra).days
    else:
        valor_venda = ""
        lucro = ""
        vendedor = ""
        cliente = ""
        cidade = ""
        forma = ""
        status = "Em estoque"
        data_venda_str = ""
        dias_em_estoque = (hoje - data_compra).days

    registros.append({
        "id_venda": vid,
        "marca": marca,
        "modelo": modelo,
        "categoria": categoria,
        "ano_fabricacao": ano_fab,
        "ano_modelo": ano_modelo,
        "cor": random.choice(CORES),
        "combustivel": random.choice(COMBUSTIVEIS),
        "cambio": random.choice(CAMBIOS),
        "quilometragem": km,
        "placa": gerar_placa(),
        "data_compra": data_compra.isoformat(),
        "valor_compra": int(valor_compra),
        "despesas": int(despesas),
        "total_investido": int(total_investido),
        "valor_fipe": int(valor_fipe),
        "data_venda": data_venda_str,
        "valor_venda": int(valor_venda) if valor_venda != "" else "",
        "lucro": int(lucro) if lucro != "" else "",
        "dias_em_estoque": dias_em_estoque,
        "forma_pagamento": forma,
        "vendedor": vendedor,
        "cliente": cliente,
        "cidade_cliente": cidade,
        "status": status,
    })
    vid += 1

# ordena por data de compra
registros.sort(key=lambda r: r["data_compra"])
for i, r in enumerate(registros, 1):
    r["id_venda"] = i

# -------------------------------------------------------------------
# Escreve CSV
# -------------------------------------------------------------------
campos = list(registros[0].keys())
with open("vendas_veiculos.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=campos, delimiter=";")
    w.writeheader()
    w.writerows(registros)

# -------------------------------------------------------------------
# Escreve JSON (usado pelo dashboard, evita problema de CORS no file://)
# -------------------------------------------------------------------
with open("dados.json", "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False)

vendidos = [r for r in registros if r["status"] == "Vendido"]
print(f"Gerados {len(registros)} veiculos | {len(vendidos)} vendidos | {len(registros)-len(vendidos)} em estoque")
print("Arquivos: vendas_veiculos.csv  e  dados.json")
