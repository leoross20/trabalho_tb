import pandas as pd


colunas_leakage = [
    "SITUA_ENCE",
    "DT_ENCERRA",
    "DT_MUDANCA",
    "SITUA_9_M",
    "SITUA_12_M",
    "TRATSUP_AT",
    "DOENCA_TRA"
]


def separar_entrada_alvo(base: pd.DataFrame):
    base = base.copy()

    entrada = base.drop(columns=["ltfu"])
    alvo = base["ltfu"]

    entrada = entrada.drop(columns=colunas_leakage, errors="ignore")

    colunas_texto = entrada.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    for coluna in colunas_texto:
        entrada[coluna] = entrada[coluna].astype(str)

    colunas_numericas = [
        coluna for coluna in entrada.columns
        if coluna not in colunas_texto
    ]

    return entrada, alvo, colunas_numericas, colunas_texto